"""
`mlp.layers` module gathers neural network layers used for each use case.
"""

from ._rnn_layers import FastTextEmbedding, Glove6BEmbedding, RNNEmbedding

__all__ = ['FastTextEmbedding',
           'Glove6BEmbedding',
           'RNNEmbedding']