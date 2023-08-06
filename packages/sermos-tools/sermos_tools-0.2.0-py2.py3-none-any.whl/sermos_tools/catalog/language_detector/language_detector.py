""" A tool for determining the language of a body of text.

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
from langdetect import detect
from sermos_tools import SermosTool


@attr.s
class LanguageDetector(SermosTool):
    """ Detect the language of a set of text.

        Usage::

            detector = LanguageDetector(full_text='my full text here')
            language = detector.detect_lang()
            is_english = detector.is_english()
    """
    full_text: str = attr.ib()

    def detect_lang(self, default_lang: str = None) -> str:
        """ Detect the language of the provided text.

            Optionally default to a specified language in the event of
            an exception. Set to None to raise on exception.
        """
        try:
            detected_lang = detect(self.full_text)
        except Exception as e:
            if default_lang is not None:
                detected_lang = default_lang
            else:
                raise e
        return detected_lang

    def is_english(self, true_on_err: bool = False) -> bool:
        """ Determine whether text is english.

            Optionally return "True" in the event of an exception.
        """
        try:
            detected_lang = self.detect_lang(self.full_text)
        except Exception as e:
            if true_on_err is True:
                detected_lang = 'en'
            else:
                raise e
        return detected_lang == 'en'
