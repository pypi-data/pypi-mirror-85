""" Tests for sparse embedding search tool
"""
import scipy.sparse as sparse
from rho_ml import Version

from sermos_tools.catalog.sparse_embedding_search.sparse_embedding_search\
    import SparseEmbeddingSearch, SimilarityResult


def test_new_index_and_search():
    """
    """
    vectors = sparse.random(20, 100, format='csr')
    ids = list(range(vectors.shape[0]))
    new_index = SparseEmbeddingSearch.create_new_search_index(
        model_name='some_name',
        version=Version.from_string("0.0.1"),
        vectors=vectors,
        ids=ids,
        save_model=False)
    similarity_results = new_index.run_similarity_search(
        search_vectors=vectors, k_results=10, k_clusters=5)
    assert isinstance(similarity_results, list)
    assert isinstance(similarity_results[0], list)
    assert isinstance(similarity_results[0][0], SimilarityResult)

    for id_, similarity_result_batch in zip(ids, similarity_results):
        assert similarity_result_batch[0] == id_
