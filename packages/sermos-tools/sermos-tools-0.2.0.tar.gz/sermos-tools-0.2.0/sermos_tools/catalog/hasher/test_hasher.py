""" Test Hasher tooling
"""
from sermos_tools.catalog.hasher import Hasher


class TestToolsHasher:
    """ Test Document Hasher
    """
    with open('tests/fixtures/pdfs/sample-pdf-1.pdf', 'rb') as f:
        sample_pdf = f.read()

    with open('tests/fixtures/html/sample-html-1.html', 'r') as f:
        sample_html = f.read()

    def test_hashing_on_pdf(self):
        """ Test loading PDF object bytes and generating hash.
        """
        hasher = Hasher()
        my_hash = hasher.hash_bytes(self.sample_pdf)

        assert my_hash == '1c310399c0ef9e6f62570ebf51f9802d'

    def test_hashing_on_html(self):
        """ Test loading HTML text and generating hash.
        """
        hasher = Hasher()
        my_hash = hasher.hash_string(self.sample_html)

        assert my_hash == 'b0f35b4bf7d001906b2b9527def1955d'
