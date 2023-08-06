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
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model, Input, load_model
from keras.layers import Embedding, Dense, LSTM
nltk.download('punkt')
nltk.download('stopwords')


class RNNMTOPreprocessor(BasePreprocessor):
    """
    Utility class performing several data preprocessing steps
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
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
            self.max_sequence_length = pickle.load(f)
            self.validation_split = pickle.load(f)
            self.vocab_size = pickle.load(f)

    def init_from_config(self, max_sequence_length: int, vocab_size: int, validation_split: float):
        self.max_sequence_length = max_sequence_length
        self.vocab_size = vocab_size
        self.validation_split = validation_split
        self.tokenizer_obj = None

    def clean(self, X: List):
        """
        Performs data cleaning operations such as removing html breaks, lower case,
        remove stopwords ...
        Args:
            X: input reviews to be cleaned
        Return:
            None
        """
        print("===========> data cleaning")
        review_lines = list()
        for line in X:
            line = line.replace('<br /><br />', ' ')
            line = line.replace('<br />', ' ')
            tokens = word_tokenize(line)
            tokens = [w.lower() for w in tokens]
            table = str.maketrans('', '', string.punctuation)
            stripped = [w.translate(table) for w in tokens]
            words = [word for word in stripped if word.isalpha()]
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word not in stop_words]
            review_lines.append(words)
        print("----> data cleaning finish")
        return review_lines

    def fit(self, X: List):
        """
        Performs data tokenization into a format that is digestible by the model
        Args:
            X: list of predictors already cleaned
        Return:
            tokenizer object and tokenized input features
        """
        print("===========> data tokenization")
        tokenizer_obj = Tokenizer(num_words=self.vocab_size)
        tokenizer_obj.fit_on_texts(X)
        self.tokenizer_obj = tokenizer_obj
        self.tokenizer_obj.word_index["pad"] = 0
        print("----> data fit finish")
        print("found %i unique tokens" % len(self.tokenizer_obj.word_index))

    def save(self, file_name_prefix, save_folder):
        """
        Stores the data preprocessor under 'models folder'
        Args:
            file_name_prefix: a file name prefix having the following format 'sentiment_analysis_%Y%m%d_%H%M%S'
            save_folder: folder under which to save the files
        Return:
            None
        """
        file_url = os.path.join(save_folder, file_name_prefix + "_preprocessor.pkl")
        with open(file_url, 'wb') as handle:
            pickle.dump(self.tokenizer_obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.max_sequence_length, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.validation_split, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.vocab_size, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("----> proprocessor object saved to %s" % file_url)

    def preprocess(self, data):
        """
        Performs data preprocessing before inference
        Args:
            data: data to evaluate
        Return:
            preprocessed data
        """
        data = self.tokenizer_obj.texts_to_sequences(data)
        data = pad_sequences(data, maxlen=self.max_sequence_length, padding="post",
                             value=self.tokenizer_obj.word_index["pad"])
        print("features tensor shape ", data.shape)
        return data


class RNNMTO(BaseRNN):
    """
    RNN Many to One classifier, this architecture applies to use cases such as sentiment analysis, reviews rating, ...
    """
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
        x = LSTM(64, dropout=0.2, recurrent_dropout=0.2)(x)
        x = Dense(250, activation='relu')(x)
        x = Dense(1, activation='sigmoid')(x)
        model = Model(inputs=input_layer, outputs=x)
        # non sequential preferred because it can incorporate residual dependencies
        # model = Sequential()
        # model.add(self.embedding_layer)
        # model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
        # model.add(Dense(250, activation='relu'))
        # model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['acc'])
        print(model.summary())
        return model

    def fit(self, X_train, y_train, X_test=None, y_test=None):
        """
        Fits the model object to the data
        Args:
            X_train: numpy array containing encoded training features
            y_train: numpy array containing training targets
            X_test: numpy array containing encoded test features
            y_test: numpy array containing test targets
        Return:
            list of values related to each datasets and loss function
        """
        if (X_test is not None) and (y_test is not None):
            history = self.model.fit(x=X_train, y=y_train, epochs=self.n_iter,
                                     batch_size=128, validation_data=(X_test, y_test),
                                     verbose=2)
        else:
            history = self.model.fit(x=X_train, y=y_train, epochs=self.n_iter, batch_size=128, verbose=2)
        return history

    def predict(self, encoded_text_list):
        """
        Inference method
        Args:
            encoded_text_list: a list of texts to be evaluated. the input is assumed to have been
            preprocessed
        Return:
            numpy array containing the probabilities of a positive review for each list entry
        """
        probs = self.model.predict(encoded_text_list)
        boolean_result = probs > 0.5
        return [int(b) for b in boolean_result]

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
