import logging
from typing import Union, Optional

from tensorflow import keras

from kolibri_dnn.embeddings.base_embedding import BaseEmbedding
from kolibri_dnn.indexers.base_indexer import BaseIndexer

L = keras.layers

class DefaultEmbedding(BaseEmbedding):

    """Embedding layer without pre-training, train embedding layer while training model"""

    def __init__(self,
                 task: str = None,
                 sequence_length: Union[int, str] = 'auto',
                 embedding_size: int = 100,
                 indexer: Optional[BaseIndexer] = None,
                 from_saved_model: bool = False):
        """
        Init bare embedding (embedding without pre-training)

        Args:
            sequence_length: ``'auto'``, ``'variable'`` or integer. When using ``'auto'``, use the 95% of corpus length
                as sequence length. When using ``'variable'``, model input shape will set to None, which can handle
                various length of input, it will use the length of max sequence in every batch for sequence length.
                If using an integer, let's say ``50``, the input output sequence length will set to 50.
            embedding_size: Dimension of the dense embedding.
        """
        super(DefaultEmbedding, self).__init__(task=task,
                                               sequence_length=sequence_length,
                                               embedding_size=embedding_size,
                                               indexer=indexer,
                                               from_saved_model=from_saved_model)
        if not from_saved_model:
            self._build_model()

    def _build_model(self, **kwargs):
        if self.sequence_length == 0 or \
                self.sequence_length == 'auto' or \
                self.token_count == 0:
            logging.debug('need to build after build_word2idx')
        else:
            input_tensor = L.Input(shape=(self.sequence_length,),
                                   name=f'input')
            layer_embedding = L.Embedding(self.token_count,
                                          self.embedding_size,
                                          name=f'layer_embedding')

            embedded_tensor = layer_embedding(input_tensor)
            self.embed_model = keras.Model(input_tensor, embedded_tensor)


if __name__ == "__main__":
    print('hello world')
