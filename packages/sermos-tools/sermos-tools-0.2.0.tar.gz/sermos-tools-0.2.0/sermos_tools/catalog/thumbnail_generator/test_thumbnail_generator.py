import pytest
from boto3 import Session
import io
from PIL import Image
from sermos_tools.catalog.thumbnail_generator import ThumbnailGenerator


class TestToolsThumbnail:
    """ Test Thumbnail Generator
    """
    with open('tests/fixtures/pdfs/sample-pdf-1.pdf', 'rb') as f:
        sample_pdf = f.read()

    with open('tests/fixtures/pngs/rhoai-logo.png', 'rb') as f:
        sample_png = f.read()

    with open('tests/fixtures/tiffs/sample-tiff-1.tiff', 'rb') as f:
        sample_tiff = f.read()

    def test_thumbnail_generator_on_pdf(self):
        """ Test loading PDF object bytes.
        """
        thumbnail_bytes = ThumbnailGenerator(document_bytes=self.sample_pdf,
                                             width=100,
                                             height=150).generate_thumbnail()

        # Assert the resultant thumbnail is indeed 100x150px
        with Image.open(io.BytesIO(thumbnail_bytes)) as im:
            assert im.size[0] == 100
            assert im.size[1] == 150

    def test_thumbnail_generator_on_png(self):
        """ Test loading PNG object bytes.
        """
        thumbnail_bytes = ThumbnailGenerator(document_bytes=self.sample_png,
                                             width=100,
                                             height=150).generate_thumbnail()

        # Assert the resultant thumbnail is indeed 100x150px
        with Image.open(io.BytesIO(thumbnail_bytes)) as im:
            assert im.size[0] == 100
            assert im.size[1] == 150

    def test_thumbnail_generator_on_tiff(self):
        """ Test loading TIFF object bytes.
        """
        thumbnail_bytes = ThumbnailGenerator(document_bytes=self.sample_tiff,
                                             width=100,
                                             height=150).generate_thumbnail()

        # Assert the resultant thumbnail is indeed 100x150px
        with Image.open(io.BytesIO(thumbnail_bytes)) as im:
            assert im.size[0] == 100
            assert im.size[1] == 150
