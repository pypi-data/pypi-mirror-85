import subprocess
import os
import io
import numpy as np
from zipfile import ZipFile
import wget
from keras.layers import Embedding
from keras.initializers import Constant
from abc import ABC, abstractmethod

class RNNEmbedding(ABC):
    """
    Parent embeddings class
    """
    def __init__(self, word_index, vocab_size, embeddings_path, max_length, save_folder):
        self.word_index = word_index
        self.vocab_size = vocab_size
        self.embeddings_path = embeddings_path
        self.max_length = max_length
        self.embedding_dimension = 300
        self.save_folder = save_folder
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.embedding_layer = self.build_embedding()

    def build_embedding(self):
        """
        Builds the embedding layer which will be called by the model
        Returns:
            An instance of keras.layers.Embedding
        """
        embeddings_matrix = self.get_embedding_matrix()
        embedding_layer = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_dimension,
                                    embeddings_initializer=Constant(embeddings_matrix),
                                    input_length=self.max_length, trainable=True)
        return embedding_layer
    
    @abstractmethod
    def get_embedding_matrix(self):
        """
        Gets the embedding matrix according to the specified embedding dimension
        Returns:
            None
        """


class Glove6BEmbedding(RNNEmbedding):
    """
    Loads glove embedding from stanford
    """
    def __init__(self, embedding_dimension, word_index, vocab_size, embeddings_path, max_length, save_folder):
        super().__init__(word_index, vocab_size, embeddings_path, max_length, save_folder)
        self.embedding_dimension = embedding_dimension
        self.embedding_layer = self.build_embedding()

    def get_embedding_matrix(self):
        """
        Gets the embedding matrix according to the specified embedding dimension
        Returns:
            None
        """
        print("===========> collecting pretrained embedding")
        output_zip_name = os.path.join(self.save_folder, "glove.6B.zip")
        output_file_name = os.path.join(self.save_folder, "glove.6B.100d.txt")
        if self.embedding_dimension in [50, 100, 200, 300]:
            file_name = 'glove.6B.%id.txt' % self.embedding_dimension
        output_file_name = os.path.join(self.save_folder, file_name)
        if not os.path.isfile(output_file_name):
            print("---> Collecting embedding file")
            output_zip_name = wget.download(self.embeddings_path, out=output_zip_name)
            print("")
            with ZipFile(output_zip_name, 'r') as zipObj:
                zipObj.extractall(self.save_folder)
            os.remove(output_zip_name)
            print("---> embedding file extracted to %s" % output_file_name)
        else:
            print("---> Embedding already exists %s" % output_file_name)
        embedding_index = {}
        with open(output_file_name) as f:
            for line in f:
                word, coefs = line.split(maxsplit=1)
                coefs = np.fromstring(coefs, 'f', sep=' ')
                embedding_index[word] = coefs
        embedding_matrix = np.zeros((self.vocab_size, self.embedding_dimension))
        for word, i in self.word_index.items():
            if i >= self.vocab_size:
                continue
            embedding_vector = embedding_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        return embedding_matrix



class FastTextEmbedding(RNNEmbedding):
    """
    Loads fasttext embedding from facebook research
    @inproceedings{mikolov2018advances,
    title={Advances in Pre-Training Distributed Word Representations},
    author={Mikolov, Tomas and Grave, Edouard and Bojanowski, Piotr and Puhrsch, Christian and Joulin, Armand},
    booktitle={Proceedings of the International Conference on Language Resources and Evaluation (LREC 2018)},
    year={2018}
    }
    """
    def __init__(self, word_index, vocab_size, embeddings_path, max_length, save_folder):
        super().__init__(word_index, vocab_size, embeddings_path, max_length, save_folder)

    def get_embedding_matrix(self):
        """
        Gets the embedding matrix according to the specified embedding dimension
        Returns:
            None
        """
        print("===========> collecting pretrained embedding")
        output_zip_name = os.path.join(self.save_folder, "wiki-news-300d-1M.vec.zip")
        output_file_name = os.path.join(self.save_folder, "wiki-news-300d-1M.vec")
        if not os.path.isfile(output_file_name):
            print("---> Collecting embedding file")
            output_zip_name = wget.download(self.embeddings_path, out=output_zip_name)
            print("")
            with ZipFile(output_zip_name, 'r') as zipObj:
                zipObj.extractall(self.save_folder)
            os.remove(output_zip_name)
            print("---> embedding file extracted to %s" % output_file_name)
        else:
            print("---> Embedding already exists %s" % output_file_name)

        fin = io.open(output_file_name, 'r', encoding='utf-8', newline='\n', errors='ignore')
        embedding_index = {}
        for line in fin:
            tokens = line.rstrip().split(' ')
            embedding_index[tokens[0]] = [float(t) for t in tokens[1:]]
        embedding_matrix = np.zeros((self.vocab_size, self.embedding_dimension))
        for word, i in self.word_index.items():
            if i >= self.vocab_size:
                continue
            embedding_vector = embedding_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        return embedding_matrix