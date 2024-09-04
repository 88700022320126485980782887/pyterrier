import pyterrier as pt
from typing import Union, List, Optional, Literal, Dict, Tuple
from pathlib import Path


@pt.java.required
class Index: # TODO: inherit Artifact once merged
    """Represents a Terrier index."""

    def __init__(self, path: Union[str, Path], *, memory: Union[bool, List[str]] = False):
        """Initialise the index.

        Args:
            path: The path to the index
            memory: If a ``bool``, whether to load the index into memory. Defaults to False. If a ``list``, the names
            of the index structures to load into memory.
        """
        self.path = Path(path) # TODO: call Artifact constructor
        self._index_obj = None
        if memory:
            if isinstance(memory, list):
                self._load_into_memory(memory)
            else:
                self._load_into_memory() # all structures

    def _index(self):
        if self._index_obj is None:
            self._index_obj = pt.terrier.J.IndexFactory.of(str(self.path.resolve()))
        return self._index_obj

    def _load_into_memory(self, structures=['lexicon', 'direct', 'inverted', 'meta']):
        pass # TODO: write this (adapt from IndexFactory)

    def as_inmem(self, structures=['lexicon', 'direct', 'inverted', 'meta']) -> 'Index':
        """Return a new Index object with the specified structures loaded into memory."""
        return Index(self.path, memory=structures)

    @staticmethod
    def of(item: Union['Index', str, Path]) -> 'Index':
        if isinstance(item, Index):
            return item
        elif isinstance(item, (str, Path)):
            return Index(item)
        # TODO: other things to coerce into Index objects?
        raise ValueError(f'Unexpected input {item!r}')

    # ----------------------------------------
    # Transformer factories
    # ----------------------------------------

    def bm25(self,
        *,
        num_results: int = 1000,
        k1: float = 1.2,
        b: float = 0.8,
        include_fields: Optional[Union[Literal['*'], str, List[str]]] = None,
        threads: int = 1,
        verbose: bool = False
    ):
        return self.retriever(
            weight_model=TerrierWeightModel.bm25,
            weight_model_args={'k1': k1, 'b': b},
            num_results=num_results,
            include_fields=include_fields,
            verbose=verbose,
        )

    def retriever(
        self,
        weight_model: Union[str, TerrierWeightModel, TCustomWeightModel],
        weight_model_args: Optional[Dict] = None,
        *,
        num_results: int = 1000,
        include_fields: Optional[Union[Literal['*'], str, List[str]]] = None,
        threads: int = 1,
        verbose: bool = False
    ) -> pt.Transformer:
        """Provides a retriever that uses the specified similarity function.

        Args:
            weight_model: The weighting model to use.
            weight_model_args: The arguments to the weighting model. Defaults to None.
            num_results: The number of results to return. Defaults to 1000.
            include_fields: The extra fields to include with the results. When "*" extracts all available fields.
            Defaults to None.
            threads: The number of threads to use. Defaults to 1.
            verbose: Output verbose logging. Defaults to False.

        Returns:
            A transformer that can be used to retrieve documents from this index.
        """
        controls, properties = self._resolve_controls_properties(weight_model, weight_model_args)
        return pt.terrier.Retriever(self,
            wmodel=weight_model,
            controls=weight_model_args,
            num_results=num_results,
            metadata=self._resolve_fields(include_fields),
            verbose=verbose)

    # ... TODO

    def _resolve_fields(self, fields):
        pass # TODO

    def _resolve_controls_properties(self, weight_model, weight_model_args) -> Tuple[dict, dict]:
        if weight_model == 'BM25':
            controls = {
                'bm25.k1': weight_model_args.get('k1', 1.2),
                'bm25.b': weight_model_args.get('b', 0.8),
            }
            properties = {}
            return controls, properties
        pass # TODO

    # ----------------------------------------
    # Java class wrappers
    # ----------------------------------------

    def close(self):
        if self._index_obj is not None:
            self._index_obj.close()
            self._index_obj = None

    def getCollectionStatistics(self):
        """Get the collection statistics"""
        return self._index().getCollectionStatistics()

    def getDirectIndex(self):
        """Return the DirectIndex associated with this index"""
        return self._index().getDirectIndex()

    def getDocumentIndex(self):
        """Return the DocumentIndex associated with this index"""
        return self._index().getDocumentIndex()

    def getEnd(self):
        """Returns the last docid in this index"""
        return self._index().getEnd()

    def getIndexRef(self):
        """Returns a direct IndexRef to this index"""
        return self._index().getIndexRef()

    def getIndexStructure(self, structureName: str):
        """Return a particular index data structure"""
        return self._index().getIndexStructure(structureName)

    def getIndexStructureInputStream(self, structureName: str):
        """Return a particular index data structure input stream"""
        return self._index().getIndexStructureInputStream(structureName)

    def getInvertedIndex(self):
        """Returns the InvertedIndex to use for this index"""
        return self._index().getInvertedIndex()

    def getLexicon(self):
        """Return the Lexicon associated with this index"""
        return self._index().getLexicon()

    def getMetaIndex(self):
        """Get the Meta Index structure"""
        return self._index().getMetaIndex()

    def getStart(self):
        """Returns the first docid in this index"""
        return self._index().getStart()

    def hasIndexStructure(self, structureName: str):
        """Returns true iff the structure exists"""
        return self._index().hasIndexStructure(structureName)

    def hasIndexStructureInputStream(self, structureName: str):
        """Returns true iff the structure input stream exists"""
        return self._index().hasIndexStructureInputStream(structureName)
