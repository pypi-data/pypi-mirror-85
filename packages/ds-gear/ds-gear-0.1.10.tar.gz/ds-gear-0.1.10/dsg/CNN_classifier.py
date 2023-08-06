import os
import pickle
import re
import subprocess
import time
from itertools import compress
import numpy as np
from cv2 import cv2
from keras.applications.vgg16 import VGG16
from keras.models import Model, load_model
from keras.layers import Dense, Flatten, Dropout
from keras.utils import to_categorical
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
from dsg.base import BasePreprocessor, BaseNN


class CNNClassifierPreprocessor(BasePreprocessor):
    """
    Utility class performing several data preprocessing steps
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def init_from_config(self, image_height: int, image_width: int, validation_split: float):
        self.validation_split = validation_split
        self.image_height = image_height
        self.image_width = image_width
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
            self.image_height = pickle.load(f)
            self.image_width = pickle.load(f)
            self.validation_split = pickle.load(f)
            self.labels_to_idx = pickle.load(f)

    def clean(self, X):
        return X

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
            pickle.dump(self.image_height, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.image_width, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.validation_split, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.labels_to_idx, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("----> proprocessor object saved to %s" % file_url)

    def preprocess(self, X, y=None):
        """
        Loads an array containing training images ready to be injected in the CNN
        Args:
            X: list of image urls
            y: labels
        Returns:
            array having shape (n_images, image_height, image_width, 3)
        """
        X_result = []
        for image_url in X:
            im = cv2.imread(image_url, 1)
            im = cv2.resize(im, (self.image_width, self.image_height))
            X_result.append(im)
        X_result = np.asarray(X_result)
        if y is not None:
            y_result = [self.labels_to_idx[k] for k in y]
            y_result = to_categorical(y_result, len(self.labels_to_idx))
            return X_result, y_result
        else:
            return X_result

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
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, stratify=y, test_size=self.validation_split)
        print("----> data splitted: validation ratio = %.1f" % self.validation_split)
        return X_train, X_test, y_train, y_test
    
    def fit(self, X, y):
        """
        updates the labels_to_idx dict with the training values
        Args:
            X: list of image urls
            y: labels
        Returns:
            None
        """
        labels = list(set(y))
        self.labels_to_idx = {k:v for v,k in enumerate(labels)}
        return


class CNNClassifier(BaseNN):
    """
    Handles the RNN model
    """
    def __init__(self, *args, **kwargs):
        self.use_pretrained_cnn = None
        self.pretrained_network_path = None
        self.pretrained_network_name = None
        self.pretrained_layer = None
        self.model = None
        self.n_labels = None
        self.idx_to_labels = None
        self.batch_size = None
        keys = kwargs.keys()
        if 'h5_file' in keys:
            self.init_from_files(h5_file=kwargs['h5_file'], idx_to_labels=kwargs['idx_to_labels'])
        else:
            self.init_from_config(idx_to_labels=kwargs['idx_to_labels'],
                                 pre_trained_cnn=kwargs['pre_trained_cnn'],
                                 pretrained_network_name=kwargs['pretrained_network_name'],
                                 n_iter=kwargs['n_iter'],
                                 image_height=kwargs['image_height'],
                                 image_width=kwargs['image_width'],
                                 batch_size=kwargs['batch_size'],
                                 pretrained_network_path=kwargs['pretrained_network_path'])

    def init_from_files(self, h5_file, idx_to_labels):
        """
        Initializes the class from a previously saved model
        Args:
            h5_file: url to a saved class
            idx_to_labels: conversion from indices to original labels
        Return:
            None
        """
        self.model = load_model(h5_file)
        self.idx_to_labels = idx_to_labels

    def init_from_config(self, idx_to_labels, pre_trained_cnn, pretrained_network_name,
                        n_iter, image_height, image_width, batch_size, pretrained_network_path):
        """
        initialize the class for the first time from a given configuration file and data processor
        Args:
            idx_to_labels: conversion from indices to original labels
            pre_trained_cnn: whether to use a pretrained network
            pretrained_network_name: name of the pretrained network to use
            n_iter: number of backprop iterations
            image_height: height in pixels
            image_width: width in pixels
            batch_size: back prop batch size
            pretrained_network_path: url for the pretrained network
        Return:
            None
        """
        self.use_pretrained_cnn = pre_trained_cnn
        self.pretrained_cnn_name = pretrained_network_name
        self.model = None
        self.n_iter = n_iter
        self.image_height = image_height
        self.image_width = image_width
        self.idx_to_labels = idx_to_labels
        self.batch_size = batch_size
        self.n_labels = len(idx_to_labels)
        self.pretrained_network_path = pretrained_network_path
        self.model = self.build_model()

    def build_model(self):
        """
        Builds an CNN model according to fixed architecture
        Return:
            None
        """
        print("===========> build model")
        vggmodel = VGG16(include_top=False, input_shape=(self.image_height, self.image_width, 3))
        for layer in vggmodel.layers:
            layer.trainable = False
        x = vggmodel.layers[-1].output
        x = Flatten()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(self.n_labels, activation='softmax')(x)
        # define new model
        model = Model(inputs=vggmodel.inputs, outputs=x)
        # summarize
        model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['acc'])
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
            history of mertrics + classification report
        """
        report = None
        if (X_test is not None) and (y_test is not None):
            history = self.model.fit(x=X_train, y=y_train, epochs=self.n_iter,
                                     batch_size=self.batch_size, validation_data=(X_test, y_test),
                                     verbose=2)
            y_hat = self.predict(X_test)
            y = np.argmax(y_test, axis=1)
            y = [self.idx_to_labels[i] for i in y]
            report = classification_report(y, y_hat, output_dict=True)
            df = pd.DataFrame(report).transpose().round(2)
            print(df)
        else:
            history = self.model.fit(x=X_train, y=y_train, epochs=self.n_iter, batch_size=self.batch_size, verbose=2)
        return history, report

    def predict(self, X_test):
        """
        Inference method
        Args:
            X_test: predictors array
        Return:
            numpy array containing the class for token character in the sentence
        """
        probs = self.model.predict(X_test)
        print(probs)
        ids = np.argmax(probs, axis=1)
        max_probs = probs.max(axis=1)
        labels = [self.idx_to_labels[i] for i in ids]
        return labels

    def predict_proba(self, X_test):
        """
        Inference method
        Args:
            X_test: array of predictors
        Return:
            numpy array containing the probabilities of a positive review for each list entry
        """
        print("classed dict")
        print(self.idx_to_labels)
        probs = self.model.predict(X_test)
        return probs

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
        print("----> model saved to %s" % file_url_keras_model)
    
