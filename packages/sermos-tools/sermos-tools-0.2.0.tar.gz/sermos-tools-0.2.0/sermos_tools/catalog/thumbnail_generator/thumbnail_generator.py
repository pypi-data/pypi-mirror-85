""" A tool for generating thumbnails of a digital document.

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
import attr
import magic
import io
import tempfile
import logging
from typing import Union
from PIL import Image
from pdf2image import convert_from_bytes
from sermos_tools import SermosTool

logger = logging.getLogger(__name__)


class UnknownFileTypeError(Exception):
    """ TODO Move this into exceptions for reuse
    """
    pass


@attr.s
class ThumbnailGenerator(SermosTool):
    """ TODO: Add actual docstring / example usages.
    """
    document_bytes: bytes = attr.ib(repr=False)
    mimetype: Union[str, None] = attr.ib(default=None)
    width: int = attr.ib(default=327)
    height: int = attr.ib(default=450)

    def __attrs_post_init__(self):
        self._get_mimetype()

    def _get_mimetype(self):
        if not self.mimetype:
            logger.debug("No mimetype provided at init, inferring...")
            self.mimetype = magic.from_buffer(self.document_bytes, mime=True)
            logger.debug("Inferred mimetype: {0}".format(self.mimetype))

    def generate_thumbnail(self) -> str:
        if self.mimetype == 'application/pdf':
            try:
                with tempfile.TemporaryDirectory() as path:
                    images_from_path = convert_from_bytes(
                        self.document_bytes,
                        output_folder=path,
                        single_file=True,  # First page only
                        size=(self.width, self.height),  # resize
                    )
                    if len(images_from_path) == 1:
                        img_byte_arr = io.BytesIO()
                        images_from_path[0].save(img_byte_arr, format='JPEG')
                        new_blob = img_byte_arr.getvalue()
                    else:
                        raise ValueError("Unable to extract first page ...")
            except Exception as e:
                raise e
        elif self.mimetype in ('image/png', 'image/jpg', 'image/jpeg',
                               'image/tiff'):
            try:
                with tempfile.NamedTemporaryFile() as temp:
                    temp.write(self.document_bytes)
                    with Image.open(temp.name) as im:
                        # Deal with transparency layers if they exist
                        if im.mode in ('RGBA', 'LA'):
                            with Image.new(im.mode[:-1], im.size,
                                           'white') as background:
                                background.paste(im, im.split()[-1])
                                im = background

                        # First resize to max width
                        new_height = self.width * im.size[1] / im.size[0]
                        im.thumbnail((self.width, new_height))

                        # Then crop height to be desired height
                        with im.crop(
                            (0, 0, self.width, self.height)) as cropped:
                            img_byte_arr = io.BytesIO()
                            cropped.save(img_byte_arr, format='JPEG')
                            new_blob = img_byte_arr.getvalue()

            except Exception as e:
                raise e
        else:
            raise UnknownFileTypeError("No implemented logic for generating "
                                       "thumbnail from mimetype {0}!".format(
                                           self.mimetype))
        return new_blob


if __name__ == "__main__":  # pragma: no cover
    with open('tmp/sample-pdf.pdf', 'rb') as f:
        document_bytes = f.read()
    thumbnail_bytes = ThumbnailGenerator(document_bytes=document_bytes,
                                         width=100,
                                         height=150).generate_thumbnail()
    with open('tmp/sample-pdf-thumb.png', 'wb') as f:
        f.write(thumbnail_bytes)
