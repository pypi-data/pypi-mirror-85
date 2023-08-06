""" A tool for performing ultra-fast searches across vectorized document sets.

    To use in an API class, follow the standard convention accessing the
    ``tools`` property that Sermos injects.

    Example::

        class DemoApiClass(object):
            def post(self, search_vectors: csr_matrix):
                embedding_tool = self.tools['embedding_search']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
                similarity_results = embedding_tool.run_similarity_search(
                    search_vectors=search_vectors, k_results=20)
                # for each row in search_vectors get the 20 closest matches
                ...

    To use in a worker method, follow the standard convention accessing the
    ``tools`` argument that Sermos injects.

    Example::

        def demo_worker_task(event, tools):
            embedding_tool = tools['embedding_search']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
            similarity_results = embedding_tool.run_similarity_search(
                search_vectors=search_vectors, k_results=20)

"""
import operator
from typing import Optional, List, Type, Tuple
import logging
import attr
from scipy.sparse import csr_matrix
from pysparnn.cluster_index import MultiClusterIndex
from rho_ml import RhoModel, Version, load_rho_model,\
    store_rho_model, ModelNotFoundError
from sermos_tools import SermosTool

logger = logging.getLogger(__name__)


@attr.s
class SimilarityResult(object):
    """ Result returned from
    :meth:`~.SparseEmbeddingSearch.run_similarity_search`.

    Args:
        id_ (str): ID in the search index
        cosine_distance (float): score between 0 (most similar) and 1 (least
            similar)

    """
    id_ = attr.ib(type=str)
    cosine_distance = attr.ib(type=float)

    @property
    def cosine_similarity(self):
        """ Score between 0 (least similar) and 1 (most similar).

        Complement of self.cosine_distance. """
        return 1 - self.cosine_distance


def _convert_pysparnn_result(result: List[Tuple[float, str]]) \
        -> List[SimilarityResult]:
    return sorted([
        SimilarityResult(id_=x[1], cosine_distance=float(x[0])) for x in result
    ],
                  key=operator.attrgetter('cosine_distance'),
                  reverse=False)


# TODO ???
@attr.s
class SparseEmbeddingSearch(RhoModel):
    """ Find similar IDs in the index by vector cosine distance.  The index
    is fixed after init (i.e. no dynamic updates) """
    search_index = attr.ib(kw_only=True, type=MultiClusterIndex, default=None)

    # todo: gracefully fail if search_index isn't set

    def initialize_index(self,
                         ids: List[str],
                         vectors: csr_matrix,
                         index_matrix_size: Optional[int],
                         num_indexes: int = 2):
        self.search_index = MultiClusterIndex(features=vectors,
                                              records_data=ids,
                                              matrix_size=index_matrix_size,
                                              num_indexes=num_indexes)

    def run_similarity_search(self,
                              search_vectors: csr_matrix,
                              k_results: int,
                              k_clusters: int = 1,
                              num_indexes: Optional[int] = None) \
            -> List[List[SimilarityResult]]:
        """ For each embedding in vector_batch (n samples x d embedding dim),
        return a list of (score, id) tuples """
        raw_results = self.search_index.search(features=search_vectors,
                                               k=k_results,
                                               k_clusters=k_clusters,
                                               return_distance=True,
                                               num_indexes=num_indexes)
        results = [_convert_pysparnn_result(row) for row in raw_results]
        return results


@attr.s
class SparseEmbeddingSearch(SermosTool):
    """ Fast search index for sparse vectors.

    Given a :meth:`~.scipy.sparse.csr_matrix` of vectors to index and an
    associated ID for each row in the matrix, allows for very quickly finding
    the IDs of the nearest vectors to some query vector(s).

    This tool should almost always be instantiated via one of two classmethods,
    :meth:`~.SparseEmbeddingTool.create_new_search_index` for building a new
    search index, and :meth:`~SparseEmbeddingTool.restore_existing_search_index`
    for pulling an existing search index from local or cloud storage.
    """
    search_model = attr.ib(type=Type[SparseEmbeddingSearch])

    @classmethod
    def restore_existing_search_index(cls,
                                      model_name: str,
                                      version_pattern: str,
                                      force_search: bool,
                                      api_download_lock_seconds: Optional[int] = 60) \
            -> 'SparseEmbeddingSearch':
        """ Instantiate a sparse embedding cache from local or cloud storage.

        Given the version pattern, load the appropriate model from local
        storage (if available) or cloud storage.  If force_search == True, cloud
        storage will always be checked to see if there is a higher version
        available in the cloud than locally.

        Args:
            model_name (str): Cache model name
            version_pattern (str): Version pattern (incl. wildcards) to search
                for
            force_search (bool): Check cloud storage for a higher version even
                if a matching local version exists.

        Returns:
            SparseEmbeddingSearch: instantiated search tool
        """
        try:
            model = load_rho_model(
                model_name=model_name,
                version_pattern=version_pattern,
                force_search=force_search,
                request_lock_seconds=api_download_lock_seconds)
            logger.info(
                f"Loaded model {model.name}, version {model.version} to "
                f"sparse embedding tool")
            return cls(search_model=model)
        except ModelNotFoundError:
            logger.warning(f"No model found by name {model_name}, version "
                           f"{version_pattern} (force search: {force_search}")
        return None

    @classmethod
    def create_new_search_index(cls,
                                model_name: str,
                                version: Version,
                                vectors: csr_matrix,
                                ids: List[str],
                                index_matrix_size: Optional[int] = None,
                                num_indexes: int = 2,
                                save_model: bool = True):
        """ Create a new embedding search index from scratch.

        Args:
            model_name (str): model name for the new search tool
            version (str): version for the newly created tool
            vectors (csr_matrix): The vectors to index.  This should be a
                `csr_matrix` with each row corresponding to one search vector.
            ids (list): A list of string IDs where each element corresponds to
                one row in self.vectors
            index_matrix_size (int): Index matrix size
            num_indexes (int): Number of search indices to use.  Higher values
                improve recall, but also increase memory consumption.
            save_model (bool): If `True` store the model in the cloud after
                indexing.

        Returns:
            SparseEmbeddingSearch: instantiated search tool
        """
        model = SparseEmbeddingSearch(name=model_name, version=version)
        model.initialize_index(ids=ids,
                               vectors=vectors,
                               index_matrix_size=index_matrix_size,
                               num_indexes=num_indexes)
        tool = cls(search_model=model)
        logger.info(f"Created new model {model.name}, "
                    f"version {model.version}")
        if save_model:
            store_rho_model(model=model)
        return tool

    # todo: throw a useful message if this isn't instantiated correctly
    def run_similarity_search(self,
                              search_vectors: csr_matrix,
                              k_results: int,
                              k_clusters: int = 1,
                              num_indexes: Optional[int] = None) \
            -> List[List[SimilarityResult]]:
        """ Search for the closest vectors to each vector in the batch of
        search_vectors.

        Args:
            search_vectors (csr_matrix): Batch of query vectors to perform
                similarity search on.  Each row corresponds to one embedding.
            k_results (int): Number of :class:`~.SimilaritySearch` objects to
                return for each row.
            k_clusters (int, optional): Number of clusters to search for
                results in.  A larger value increases recall, but also increase
                search time.
            num_indexes (int, optional): Number of indexes to search

        Returns:
            list: A nested list of SimilarityResult objects.  For each row in
                search_vectors there is one list of SimilarityResults (up to
                k_clusters)
        """
        result = self.search_model.run_similarity_search(
            search_vectors=search_vectors,
            k_results=k_results,
            k_clusters=k_clusters,
            num_indexes=num_indexes)
        return result
