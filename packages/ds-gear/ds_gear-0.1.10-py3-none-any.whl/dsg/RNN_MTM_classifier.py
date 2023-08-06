import os
import string
import pickle
import time
from typing import List
import numpy as np
from dsg.base import BasePreprocessor, BaseRNN
from dsg.layers import Glove6BEmbedding, FastTextEmbedding
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from sklearn.metrics import classification_report
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model, Input, load_model
from keras.utils import to_categorical
from keras.layers import LSTM, Dense, TimeDistributed, Embedding, Bidirectional, add
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
nltk.download('punkt')
nltk.download('stopwords')


class RNNMTMPreprocessor(BasePreprocessor):
    """
    Utility class performing several data preprocessing steps
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def init_from_config(self, max_sequence_length: int, vocab_size: int, validation_split: float):
        self.max_sequence_length = max_sequence_length
        self.vocab_size = vocab_size
        self.validation_split = validation_split
        self.tokenizer_obj = None
        self.labels_to_idx = None

    def init_from_file(self, preprocessor_file: str):
        """
        Loads preprocessing tools for the model
        Args:
            preprocessor_file: url to saved preprocessing file
        Return:
            preprocessed object
        """
        with open(preprocessor_file, 'rb') as f:
            self.tokenizer_obj = pickle.load(f)
            self.labels_to_idx = pickle.load(f)
            self.max_sequence_length = pickle.load(f)
            self.validation_split = pickle.load(f)
            self.vocab_size = pickle.load(f)

    def clean(self, X: List):
        """
        Performs data cleaning operations such as removing html breaks, lower case,
        remove stopwords ...
        Args:
            X: input reviews to be cleaned
        Returns:
            None
        """
        print("===========> data cleaning")
        review_lines = list()
        for line in X:
            tokens = [w.lower() for w in line]
            table = str.maketrans('', '', string.punctuation)
            stripped = [w.translate(table) for w in tokens]
            words = [word for word in stripped if word.isalpha()]
            # stop_words = set(stopwords.words('english'))
            # words = [word for word in words if word not in stop_words]
            review_lines.append(words)
        print("----> data cleaning finish")
        return review_lines

    def fit(self, X: List, y: List):
        """
        Performs data tokenization into a format that is digestible by the model
        Args:
            X: list of predictors already cleaned
        Returns:
            tokenizer object and tokenized input features
        """
        print("===========> data tokenization")
        # features tokenization
        self.tokenizer_obj = Tokenizer(num_words=self.vocab_size)
        self.tokenizer_obj.fit_on_texts(X)
        self.tokenizer_obj.word_index["pad"] = 0
        flat_list = [item for sublist in y for item in sublist]
        unique_labels = list(set(flat_list))
        self.labels_to_idx = {t: i + 1 for i, t in enumerate(unique_labels)}
        self.labels_to_idx["pad"] = 0
        print("----> data fitting finish")
        print("found %i unique tokens" % len(self.tokenizer_obj.word_index))

    def save(self, file_name_prefix, save_folder):
        """
        Stores the data preprocessor under 'models folder'
        Args:
            file_name_prefix: a file name prefix having the following format 'named_entity_recognition_%Y%m%d_%H%M%S'
            save_folder: folder under which to save the files
        Return:
            None
        """
        file_url = os.path.join(save_folder, file_name_prefix + "_preprocessor.pkl")
        with open(file_url, 'wb') as handle:
            pickle.dump(self.tokenizer_obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.labels_to_idx, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.max_sequence_length, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.validation_split, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.vocab_size, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("----> proprocessor object saved to %s" % file_url)

    def preprocess(self, X, y=None):
        """
        Performs data preprocessing before inference
        Args:
            X: Features
            y: targets
        Return:
            preprocessed data
        """
        lines = list()
        n_tokens_list = list()
        for line in X:
            if not isinstance(line, list):
                line = word_tokenize(line)
            lines.append(line)
            n_tokens_list.append(len(line))
        sequences = self.tokenizer_obj.texts_to_sequences(lines)
        review_pad = pad_sequences(sequences, maxlen=self.max_sequence_length, padding="post",
                                   value=self.tokenizer_obj.word_index["pad"])
        print("features tensor shape ", review_pad.shape)
        tokenized_labels = None
        if y is not None:
            tokenized_labels = [[self.labels_to_idx[word] for word in sublist] for sublist in y]
            tokenized_labels = pad_sequences(tokenized_labels, maxlen=self.max_sequence_length, padding="post",
                                            value=self.labels_to_idx["pad"])
            print("labels tensor shape ", tokenized_labels.shape)
        return review_pad, lines, n_tokens_list, tokenized_labels


class RNNMTM(BaseRNN):
    """
    RNN Many to Many classifier, this architecture serves applications such as Named Entity Recognition, machine translation ...
    """
    def __init__(self, **kwargs):
        self.n_labels = None
        self.labels_to_idx = None
        super().__init__(**kwargs)
    
    def init_from_files(self, h5_file:str, class_file:str):
        """
        Initialize the class from a previously saved model
        Args:
            h5_file: url to a saved class
            class_file: url to a saved class file
        Return:
            None
        """
        self.model = load_model(h5_file, custom_objects={'CRF': CRF,
                                                         'crf_loss': crf_loss,
                                                         'crf_viterbi_accuracy': crf_viterbi_accuracy})
        with open(class_file, 'rb') as f:
            self.use_pretrained_embedding = pickle.load(f)
            self.vocab_size = pickle.load(f)
            self.embedding_dimension = pickle.load(f)
            self.embeddings_path = pickle.load(f)
            self.max_length = pickle.load(f)
            self.word_index = pickle.load(f)

    def init_from_config(self, pre_trained_embedding: bool, vocab_size:int, embedding_dimension:int, embedding_algorithm: str,
                         save_folder: str, n_iter: int, embeddings_path: str, max_sequence_length: int,
                         data_preprocessor: RNNMTMPreprocessor):
        """
        Initializes the class for the first time from a given configuration file and data processor
        Args:
            config: .json configuration reader
            data_preprocessor: preprocessing tool for the training data
        Return:
            None
        """
        self.use_pretrained_embedding = pre_trained_embedding
        self.vocab_size = vocab_size
        self.embedding_dimension = embedding_dimension
        self.embeddings_name = embedding_algorithm
        self.embeddings_path = embeddings_path
        self.max_length = max_sequence_length
        self.n_iter = n_iter
        self.save_folder = save_folder
        self.n_labels = len(data_preprocessor.labels_to_idx)
        self.word_index = data_preprocessor.tokenizer_obj.word_index
        self.embedding_layer = self.build_embedding()
        self.model = self.build_model()

    def build_model(self):
        """
        Builds an RNN model according to fixed architecture
        Return:
            None
        """
        print("===========> build model")
        # Run the function
        input_layer = Input(shape=(self.max_length,), name='input')
        x = self.embedding_layer(input_layer)

        # # archi 1: f1-macro 0.3-fasttext 0.3-no embedding
        # x = Dropout(0.1)(x)
        # x = Bidirectional(LSTM(units=100, return_sequences=True, recurrent_dropout=0.1))(x)
        # x = TimeDistributed(Dense(self.n_labels, activation='softmax'))(x)
        # model = Model(inputs=input_layer, outputs=x)
        # model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['acc'])

        # # archi 2: f1-macro 0.35-fasttext
        # x = Bidirectional(LSTM(units=512, return_sequences=True, recurrent_dropout=0.2, dropout=0.2))(x)
        # x_rnn = Bidirectional(LSTM(units=512, return_sequences=True, recurrent_dropout=0.2, dropout=0.2))(x)
        # x = add([x, x_rnn])  # residual connection to the first biLSTM
        # x = TimeDistributed(Dense(self.n_labels, activation='softmax'))(x)
        # model = Model(inputs=input_layer, outputs=x)
        # model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['acc'])

        # # archi 3: crf layer
        x = Bidirectional(LSTM(units=50, return_sequences=True, recurrent_dropout=0.2, dropout=0.2))(x)
        x_rnn = Bidirectional(LSTM(units=50, return_sequences=True, recurrent_dropout=0.2, dropout=0.2))(x)
        x = add([x, x_rnn])  # residual connection to the first biLSTM
        x = TimeDistributed(Dense(50, activation='relu'))(x)
        crf = CRF(self.n_labels, sparse_target=True)
        x = crf(x)
        model = Model(inputs=input_layer, outputs=x)
        model.compile(loss=crf.loss_function, optimizer='adam', metrics=[crf.accuracy])

        print(model.summary())
        return model

    def fit(self, X_train, y_train, X_test=None, y_test=None, labels_to_idx=None):
        """
        Fits the model object to the data
        Args:
            X_train: numpy array containing encoded training features
            y_train: numpy array containing training targets
            X_test: numpy array containing encoded test features
            y_test: numpy array containing test targets
            labels_to_idx: a dictionary containing the conversion from each class label to its id
        Return:
            list of values related to each datasets and loss function
        """
        wts = 10 * np.ones((y_train.shape[0], y_train.shape[1]))
        classes = np.argmax(y_train, axis=1)
        wts[classes == labels_to_idx["pad"]] = 1
        if (X_test is not None) and (y_test is not None):
            # history = self.model.fit(x=X_train, y=y_train, epochs=self.n_iter, batch_size=64,
            #                        sample_weight=wts, validation_split=0.1, verbose=2)
            y_train = np.expand_dims(y_train,2)            
            history = self.model.fit(X_train, y_train, batch_size=32, epochs=self.n_iter,
                                     verbose=2, validation_split=0.1)
            y_hat = self.predict(X_test, labels_to_idx)
            y = [self.convert_idx_to_labels(sublist, labels_to_idx) for sublist in y_test]
            y_flat = [val for sublist in y for val in sublist]
            y_hat_flat = [val for sublist in y_hat for val in sublist]
            report = classification_report(y_flat, y_hat_flat, output_dict=True)
            df = pd.DataFrame(report).transpose().round(2)
            print(df)
        else:
            report = None
            history = self.model.fit(x=X_train, y=y_train, epochs=self.n_iter, batch_size=64, verbose=2)
        return history, report

    def convert_idx_to_labels(self, classes_vector, labels_to_idx):
        """
        Utility function to convert encoded target idx to original labels
        Args:
            classes_vector: target vector containing indexed classes
            labels_to_idx: a dictionary containing the conversion from each class label to its id
        Return:
            numpy array containing the corresponding labels
        """
        idx_to_labels = {v: k for k, v in labels_to_idx.items()}
        return [idx_to_labels[cl] for cl in classes_vector]

    def predict(self, encoded_text_list, labels_to_idx, n_tokens_list=None):
        """
        Inference method
        Args:
            encoded_text_list: a list of texts to be evaluated. the input is assumed to have been preprocessed
            n_tokens_list: number of tokens in each input string before padding
            labels_to_idx: a dictionary containing the conversion from each class label to its id
        Return:
            numpy array containing the class for token character in the sentence
        """
        probs = self.model.predict(encoded_text_list)
        labels_list = []
        for i in range(len(probs)):
            if n_tokens_list is not None:
                real_probs = probs[i][:n_tokens_list[i]]
            else:
                real_probs = probs[i]
            classes = np.argmax(real_probs, axis=1)
            labels_list.append(self.convert_idx_to_labels(classes, labels_to_idx))
        return labels_list

    def predict_proba(self, encoded_text_list):
        """
        Inference method
        Args:
            encoded_text_list: a list of texts to be evaluated. the input is assumed to have been
            preprocessed
        Return:
            numpy array containing the probabilities of a positive review for each list entry
        """
        probs = self.model.predict(encoded_text_list)
        return [p[0] for p in probs]

    def save(self, file_name_prefix, save_folder):
        """
        Saves the trained model into a h5 file
        Args:
            file_name_prefix: a file name prefix having the following format 'named_entity_recognition_%Y%m%d_%H%M%S'
            save_folder: folder under which to save the files
        Return:
            None
        """
        file_url_keras_model = os.path.join(save_folder, file_name_prefix + "_rnn_model.h5")
        self.model.save(file_url_keras_model)
        file_url_class = os.path.join(save_folder, file_name_prefix + "_rnn_class.pkl")
        with open(file_url_class, 'wb') as handle:
            pickle.dump(self.use_pretrained_embedding, handle)
            pickle.dump(self.vocab_size, handle)
            pickle.dump(self.embedding_dimension, handle)
            pickle.dump(self.embeddings_path, handle)
            pickle.dump(self.max_length, handle)
            pickle.dump(self.word_index, handle)
        print("----> model saved to %s" % file_url_keras_model)
        print("----> class saved to %s" % file_url_class)
