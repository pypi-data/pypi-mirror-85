""" A tool for producing a consistent hash of a digital file.

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
import re
import hashlib
import attr
from sermos_tools import SermosTool


@attr.s
class Hasher(SermosTool):
    """ Generate a consistent hash of bytes, full text, etc.

        Usage::

            hasher = Hasher()
            my_hash = hasher.hash_bytes(my_doc_bytes)
            # or
            my_hash = hasher.hash_string(my_doc_full_text)
    """
    def hash_bytes(self, bytes_to_hash: bytes) -> str:
        """ Generate an md5 hash from bytes.
        """
        hasher = hashlib.md5()
        hasher.update(bytes_to_hash)
        return hasher.hexdigest()

    def hash_string(self, string: str, remove_spaces: bool = True) -> str:
        """ Generate a hash from a "full text" string.

            This removes all spaces by default to attempt more consistent
            hashing of full text extracted from sources that may have arbitrary
            newline and spaces.
        """
        if remove_spaces:
            string = re.sub(r'[\s\n]+', '', string)
        stripped_bytes = string.encode()
        return self.hash_bytes(bytes_to_hash=stripped_bytes)
