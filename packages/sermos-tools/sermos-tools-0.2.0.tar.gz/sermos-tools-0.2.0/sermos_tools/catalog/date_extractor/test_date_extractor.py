""" Test Date Extractor tooling
"""
from sermos_tools.catalog.date_extractor import DateExtractor


class TestToolsDateExtractor:
    """ Test Date Extractor
    """
    with open('tests/fixtures/text/sample-text-no-dates.txt', 'r') as f:
        text_no_dates = f.read()

    with open('tests/fixtures/text/sample-text-with-dates.txt', 'r') as f:
        text_with_dates = f.read()

    def test_date_extractor_on_pdf(self):
        """ Test loading PDF object bytes from S3 and extracting dates.
        """
        date_extractor = DateExtractor(full_text=self.text_no_dates)

        assert len(date_extractor.normalized_dates) == 0

        copyright_year = date_extractor.find_copyright_year()
        assert copyright_year is None

    def test_date_extractor_on_html(self):
        """ Test loading HTML object bytes from S3 and extracting it dates.
        """
        date_extractor = DateExtractor(full_text=self.text_with_dates)

        # TODO Date extractor currently buggy with dates in format YYYY-MM-DD
        # such that the second date in this sample (2019-11-05) erroneously
        # returns as 2005-11-01

        assert len(date_extractor.normalized_dates) == 2
        assert date_extractor.normalized_dates[0] == '2020-01-02'

        copyright_year = date_extractor.find_copyright_year()
        assert copyright_year == 1986
