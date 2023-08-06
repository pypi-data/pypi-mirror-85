""" A tool for extracting the fulltext from a digital document.

    To use in an API class, follow the standard convention accessing the
    ``tools`` property that Sermos injects.

    Example::

        class DemoApiClass(object):
            def post(self):
                TODO: Example

    To use in a worker method, follow the standard convention accessing the
    ``tools`` argument that Sermos injects.

    Example::

        def demo_worker_task(event, tools):
            TODO: Example

"""
import io
import re
from typing import BinaryIO, TextIO, Optional
from sermos_tools import SermosTool
import pdftotext
import attr
import bs4
import magic
import logging

logger = logging.getLogger(__name__)


class UnknownFileTypeError(Exception):
    pass


@attr.s
class TextExtractor(SermosTool):
    """ Extract fulltext from supported filetypes.

        Usage::

            extractor = TextExtractor(
                document_bytes=blob_bytes
            )
            fulltext = extractor.full_text
    """
    document_bytes: bytes = attr.ib(repr=False)
    mimetype: Optional[str] = attr.ib(default=None)
    full_text: str = attr.ib(default='')
    word_count: int = attr.ib(default=0)
    page_count: int = attr.ib(default=0)

    def __attrs_post_init__(self):
        self._get_mimetype()
        self.full_text = self._extract_text()
        self.word_count = self._calculate_word_count()

    def _get_mimetype(self):
        if not self.mimetype:
            logger.debug("No mimetype provided at init, inferring...")
            self.mimetype = magic.from_buffer(self.document_bytes, mime=True)
            logger.debug("Inferred mimetype: {0}".format(self.mimetype))

    def _extract_text(self) -> str:
        """ Extracts text from document based on document type.
            Sets page_count as well.
        """
        if self.mimetype == 'application/pdf':
            self.full_text, self.page_count =\
                self.extract_pdf_text_and_page_count(self.document_bytes)
        elif self.mimetype == 'text/html':
            self.full_text = self.extract_html_text(self.document_bytes)
            self.page_count = 1
        else:
            raise UnknownFileTypeError("No implemented logic for extracting "
                                       "text from mimetype {0}!".format(
                                           self.mimetype))
        return self.full_text

    def _calculate_word_count(self) -> str:
        """ Calculates word count from document based on full_text.
        """
        if self.full_text == '':
            self._extract_text()
        self.word_count = len(re.sub(' +', ' ', self.full_text).split(' '))
        return self.word_count

    def _get_html_fileobj_from_bytes(self, b: bytes) -> TextIO:
        # todo add chardet to properly decode data
        f = io.StringIO()
        f.write(b.decode('utf-8'))
        f.seek(0)
        return f

    def _get_fileobj_from_bytes(self, b: bytes) -> BinaryIO:
        f = io.BytesIO()
        f.write(b)
        f.seek(0)
        return f

    def extract_pdf_text_and_page_count(self, document_bytes: bytes) -> str:
        f = self._get_fileobj_from_bytes(document_bytes)
        pdf = pdftotext.PDF(f)
        logger.debug("Extracted {0} pages from pdf".format(len(pdf)))
        return "\n\n".join(pdf), len(pdf)

    def extract_html_text(self, document_bytes: bytes) -> str:
        """ Tag removal found here: https://stackoverflow.com/a/19760007 """
        f = self._get_html_fileobj_from_bytes(document_bytes)
        soup = bs4.BeautifulSoup(f, features="html.parser")
        [
            s.extract()
            for s in soup(['style', 'script', '[document]', 'head', 'title'])
        ]
        return soup.getText()
