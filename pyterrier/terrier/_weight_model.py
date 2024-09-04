from enum import Enum
from typing import Callable


class TerrierWeightModel(Enum):
    bm25 = 'BM25'
    tf = 'TF'
    tfidf = 'TFIDF'
    # TODO: more


TCustomWeightModel = Callable[[], float] # TODO: define arguments
