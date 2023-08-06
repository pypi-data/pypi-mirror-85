""" Test Lang Detect tooling
"""
import pytest
from sermos_tools.catalog.language_detector import LanguageDetector


class TestToolsLanguage:
    """ Test Language Detector
    """
    with open('tests/fixtures/text/sample-pdf-1-text.txt', 'r') as f:
        sample_text = f.read()

    with open('tests/fixtures/html/sample-html-1.html', 'r') as f:
        sample_html = f.read()

    def test_language_on_text(self):
        """ Test identifying language in string of text.
        """
        language = LanguageDetector(full_text=self.sample_text)

        # Test proper detection of this as an english language document
        assert language.detect_lang() == 'en'
        assert language.is_english() is True

        # Test error cases for known exception case of 'None' as fulltext
        language = LanguageDetector(full_text=None)

        # Test exception handling with default lang
        assert language.detect_lang(default_lang='foo') == 'foo'

        # Test exception handling with no default lang (exception raised)
        with pytest.raises(TypeError):
            language.detect_lang()

        # Test exception handling with true_on_err
        assert language.is_english(true_on_err=True) is True

        # Test exception handling without true_on_err (exception raised)
        with pytest.raises(TypeError):
            language.is_english()

    def test_language_on_html(self):
        """ Test loading HTML object bytes from S3 and extracting it dates.
        """
        language = LanguageDetector(full_text=self.sample_html)

        # TODO - langdetect does NOT properly identify this as a latin
        # document ... Also seems to be non-deterministic, as it variably
        # reports 'ca' and 'fr' during testing
        # assert language.detect_lang() == 'la'

        # Assert non-english
        assert language.is_english() is False
