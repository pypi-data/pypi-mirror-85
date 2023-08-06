"""
Contains abstract Neural network and data preprocessor for the use cases
"""

from abc import ABC, abstractmethod
import os
import matplotlib.pyplot as plt
import string
import pickle
import subprocess
from typing import List
import numpy as np
import pandas as pd
from dsg.layers import FastTextEmbedding, Glove6BEmbedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model, Input, load_model
from keras.layers import Embedding, Dense, LSTM
from sklearn.model_selection import train_test_split

class BasePreprocessor(ABC):
    """
    Base class for neural network preprocessor.
    """
    def __init__(self, **kwargs):
        keys = kwargs.keys()
        if 'preprocessor_file' in keys:
            self.init_from_file(kwargs['preprocessor_file'])
        else:
            self.init_from_config(**kwargs)

    @abstractmethod
    def init_from_file(self, preprocessor_file: str):
        """
        initalizes the preprocessor from a saved object
        preprocessor_file: saved preprocessor
        return initialized preprocessor
        """
        pass

    @abstractmethod
    def init_from_config(self, **kwargs):
        """
        initalizes the preprocessor from configuration parameters
        return initialized preprocessor
        """
        self.validation_split = kwargs['validation_split']

    @abstractmethod
    def clean(self, X: List):
        """
        Performs data cleaning operations such as removing html breaks, lower case,
        remove stopwords ...
        Args:
            X: input reviews to be cleaned
        Return:
            None
        """
        pass

    @abstractmethod
    def fit(self, X: List):
        """
        Performs data tokenization into a format that is digestible by the model
        Args:
            X: list of predictors already cleaned
        Return:
            tokenizer object and tokenized input features
        """
        pass

    def split_train_test(self, X, y):
        """
        Wrapper method to split training data into a validation set and a training set
        Args:
            X: tokenized predictors
            y: labels
        Return:
            tuple consisting of training predictors, training labels, validation predictors, validation labels
        """
        print("===========> data split")
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, test_size=self.validation_split)
        print("----> data splitted: validation ratio = %.1f" % self.validation_split)
        return X_train, X_test, np.asarray(y_train), np.asarray(y_test)

    @abstractmethod
    def save(self, file_name_prefix):
        """
        Stores the data preprocessor under 'models folder'
        Args:
            file_name_prefix: a file name prefix having the following format 'sentiment_analysis_%Y%m%d_%H%M%S'
        Return:
            None
        """
        pass

    @abstractmethod
    def preprocess(self, X):
        """
        Loads preprocessing tools for the model
        Args:
            X: data to evaluate
        Return:
            preprocessed object
        """
        pass

class BaseNN(ABC):
    """
    Base class for recurrent neural network models.
    """
    def __init__(self, **kwargs):
        keys = kwargs.keys()
        if 'data_preprocessor' in keys:
            self.init_from_config(**kwargs)
        else:
            self.init_from_files(**kwargs)

    def init_from_files(self, **kwargs):
        """
        Initializes the class from a previously saved model
        Args:
            h5_file: url to a saved h5 model file
            class_file: url to a saved class file
        Return:
            None
        """
        pass

    def init_from_config(self, **kwargs):
        """
        initialize the class for the first time from a given configuration file and data processor
        Args:
            config: .json configuration file
            data_preprocessor: preprocessing tool for the training data
        Return:
            None
        """
        pass

    @abstractmethod
    def build_model(self):
        """
        Builds an RNN model according to fixed architecture
        Return:
            None
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def predict(self, encoded_text_list):
        """
        Inference method
        Args:
            encoded_text_list: a list of texts to be evaluated. the input is assumed to have been
            preprocessed
        Return:
            numpy array containing the probabilities of a positive review for each list entry
        """
        pass

    @abstractmethod
    def predict_proba(self, encoded_text_list):
        """
        Inference method
        Args:
            encoded_text_list: a list of texts to be evaluated. the input is assumed to have been
            preprocessed
        Return:
            numpy array containing the probabilities of a positive review for each list entry
        """
        pass

    def save(self, file_name_prefix, save_folder):
        """
        Stores the data preprocessor under 'models folder'
        Args:
            file_name_prefix: a file name prefix having the following format 'sentiment_analysis_%Y%m%d_%H%M%S'
            save_folder: folder under which to save the files
        Return:
            None
        """
        pass

    def save_learning_curve(self, history, file_name_prefix, save_folder, metric="acc"):
        """
        Saves the learning curve plot
        Args:
            history: a dictionary object containing training and validation dataset loss function values and
            objective function values for each training iteration
            save_folder: folder under which to save the files
            file_name_prefix: a file name prefix having the following format 'sentiment_analysis_%Y%m%d_%H%M%S'
        Return:
            None
        """
        acc = history.history[metric]
        val_acc = history.history['val_'+metric]
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        epochs = range(len(acc))

        fig, ax = plt.subplots(1, 2)
        ax[0].plot(epochs, acc, 'bo', label='Training acc')
        ax[0].plot(epochs, val_acc, 'b', label='Validation acc')
        ax[0].set_title('Training and validation accuracy')
        ax[0].legend()
        fig.suptitle('model performance')
        ax[1].plot(epochs, loss, 'bo', label='Training loss')
        ax[1].plot(epochs, val_loss, 'b', label='Validation loss')
        ax[1].set_title('Training and validation loss')
        ax[1].legend()
        plot_file_url = os.path.join(save_folder, file_name_prefix + "_learning_curve.png")
        plt.savefig(plot_file_url)
        plt.close()
        print("----> learning curve saved to %s" % plot_file_url)

    def save_classification_report(self, report, file_name_prefix, save_folder):
        """
        Saves the classification report to a txt file
        Args:
            report: a classification report object
            file_name_prefix: a file name prefix having the following format 'named_entity_recognition_%Y%m%d_%H%M%S'
            save_folder: folder under which to save the files
        Return:
            None
        """
        report_file_url = os.path.join(save_folder, file_name_prefix + "_report.txt")
        df = pd.DataFrame(report).transpose().round(2)
        df['classes'] = df.index
        f = open(report_file_url, "w")
        line = "{:15} |{:10} |{:10} |{:10} |{:10}|\n".format("classes", "precision", "recall", "f1-score", "support")
        f.write(line)
        for _, row in df.iterrows():
            line = "{:15} |{:10} |{:10} |{:10} |{:10}|\n".format(row[4], row[0], row[1], row[2], row[3])
            f.write(line)
        f.close()
        print("----> classification report saved to %s" % report_file_url)

class BaseRNN(BaseNN):
    """
    Base class for recurrent neural network models.
    """
    def __init__(self, **kwargs):
        self.model_name = "rnn"
        self.use_pretrained_embedding = None
        self.vocab_size = None
        self.embedding_dimension = None
        self.embeddings_path = None
        self.max_length = None
        self.word_index = None
        self.embedding_layer = None
        self.model = None
        keys = kwargs.keys()
        if 'data_preprocessor' in keys:
            self.init_from_config(pre_trained_embedding=kwargs['pre_trained_embedding'],
                                       vocab_size=kwargs['vocab_size'],
                                       embedding_dimension=kwargs['embedding_dimension'],
                                       embedding_algorithm=kwargs['embedding_algorithm'],
                                       save_folder=kwargs['save_folder'],
                                       n_iter=kwargs['n_iter'],
                                       embeddings_path=kwargs['embeddings_path'],
                                       max_sequence_length=kwargs['max_sequence_length'],
                                       data_preprocessor=kwargs['data_preprocessor'])
        else:
            self.init_from_files(h5_file=kwargs['h5_file'], class_file=kwargs['class_file'])

    def init_from_files(self, h5_file: str, class_file:str):
        """
        Initializes the class from a previously saved model
        Args:
            h5_file: url to a saved h5 model file
            class_file: url to a saved class file
        Return:
            None
        """
        self.model = load_model(h5_file)
        with open(class_file, 'rb') as f:
            self.use_pretrained_embedding = pickle.load(f)
            self.vocab_size = pickle.load(f)
            self.embedding_dimension = pickle.load(f)
            self.embeddings_path = pickle.load(f)
            self.max_length = pickle.load(f)
            self.word_index = pickle.load(f)

    def init_from_config(self, pre_trained_embedding: bool, vocab_size:int, embedding_dimension:int, embedding_algorithm: str,
                         save_folder: str, n_iter: int, embeddings_path: str, max_sequence_length: int,
                         data_preprocessor: BasePreprocessor):
        """
        initialize the class for the first time from a given configuration file and data processor
        Args:
            config: .json configuration file
            data_preprocessor: preprocessing tool for the training data
        Return:
            None
        """
        self.use_pretrained_embedding = pre_trained_embedding
        self.vocab_size = vocab_size
        self.embedding_dimension = embedding_dimension
        self.embeddings_name = embedding_algorithm
        self.n_iter = n_iter
        self.save_folder = save_folder
        self.embeddings_path = embeddings_path
        self.max_length = max_sequence_length
        self.word_index = data_preprocessor.tokenizer_obj.word_index
        self.embedding_layer = self.build_embedding()
        self.model = self.build_model()

    def build_embedding(self):
        """
        Builds the embedding layer. depending on the configuration, it will either
        load a pretrained embedding or create an empty embedding to be trained along
        with the data
        Return:
            None
        """
        if self.use_pretrained_embedding and self.embeddings_name == "glove":
            glove_embeddings = Glove6BEmbedding(self.embedding_dimension, self.word_index,
                                                self.vocab_size, self.embeddings_path, self.max_length, self.save_folder)
            embedding_layer = glove_embeddings.embedding_layer
        elif self.use_pretrained_embedding and self.embeddings_name == "fasttext":
            fasttext_embeddings = FastTextEmbedding(self.word_index, self.vocab_size, self.embeddings_path,
                                                    self.max_length, self.save_folder)
            embedding_layer = fasttext_embeddings.embedding_layer
        else:
            print("===========> embedding trained with the model")
            embedding_layer = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_dimension,
                                        input_length=self.max_length, trainable=True)
        return embedding_layer

    @abstractmethod
    def build_model(self):
        """
        Builds an RNN model according to fixed architecture
        Return:
            None
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def predict(self, encoded_text_list):
        """
        Inference method
        Args:
            encoded_text_list: a list of texts to be evaluated. the input is assumed to have been
            preprocessed
        Return:
            numpy array containing the probabilities of a positive review for each list entry
        """
        pass

    @abstractmethod
    def predict_proba(self, encoded_text_list):
        """
        Inference method
        Args:
            encoded_text_list: a list of texts to be evaluated. the input is assumed to have been
            preprocessed
        Return:
            numpy array containing the probabilities of a positive review for each list entry
        """
        pass

    def save(self, file_name_prefix, save_folder):
        """
        Stores the data preprocessor under 'models folder'
        Args:
            file_name_prefix: a file name prefix having the following format 'sentiment_analysis_%Y%m%d_%H%M%S'
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

class BaseRF(ABC):
    pass