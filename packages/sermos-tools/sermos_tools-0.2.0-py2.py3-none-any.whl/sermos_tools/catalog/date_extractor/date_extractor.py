""" A tool for identifying dates within a string of text.

    Example::

        date_extractor = DateExtractor(full_text=self.text_with_dates)
        date_extractor.normalized_dates[0]  # == '2020-01-02'
        date_extractor.find_copyright_year()  # == '2020-01-02'

"""
import calendar
import datetime
from typing import Match, List
import attr
import regex
from toolz.itertoolz import concat
from sermos_tools import SermosTool


@attr.s(auto_attribs=True)
class DatePatterns(object):
    """ Common date patterns for regex-based searches against fulltext.
    """

    MONTH_OPTIONS: frozenset = frozenset(m
                                         for m in concat((calendar.month_name,
                                                          calendar.month_abbr))
                                         if m)

    MONTH_ABBR_MAP: dict = {
        m.lower(): i
        for i, m in enumerate(calendar.month_abbr) if m
    }
    MONTH_NAME_MAP: dict = {
        m.lower(): i
        for i, m in enumerate(calendar.month_name) if m
    }

    NUM_MDY_PATTERN: regex = regex.compile(
        r'\b(?P<month>0?[1-9]|1[0-2])\s*[/\.\-]\s*'
        r'(?P<day>0?[1-9]|[12]\d|3[01])\s*[/\.\-]\s*'
        r'(?P<year>\d{4}|\d{2})\b')
    NUM_MY_PATTERN: regex = regex.compile(
        r'\b(?P<month>0?[1-9]|1[0-2])\s*[/\.\-]\s*'
        r'(?P<year>\d{4}|\d{2})\b')
    STR_MDY_PATTERN: regex = regex.compile(
        r'\b(?P<month>\L<month_options>)\s*[/\.\-\s]'
        r'\s*(?P<day>0?[1-9]|[12]\d|3[01])'
        r'\s*[/\.\-,]\s*(?P<year>\d{4}|\d{2})\b',
        month_options=MONTH_OPTIONS,
        flags=regex.IGNORECASE)
    STR_MY_PATTERN: regex = regex.compile(
        r'\b(?P<month>\L<month_options>)\s*[/\.\-\s,]'
        r'\s*(?P<year>\d{4}|\d{2})\b',
        month_options=MONTH_OPTIONS,
        flags=regex.IGNORECASE)

    DATE_PATTERNS: list = [
        NUM_MDY_PATTERN, NUM_MY_PATTERN, STR_MDY_PATTERN, STR_MY_PATTERN
    ]


@attr.s
class DateExtractor(SermosTool):
    """ Extract dates from provided `full_text`

        Usage:
            extractor = DateExtractor('Your Full Text Here Jan 2, 2000')
            extractor.normalized_dates --> ['2000-01-02']
    """
    full_text: str = attr.ib()
    raw_dates_as_dicts: bool = attr.ib(default=True)
    document_pages: List[str] = attr.ib(default=[])
    raw_captured_dates: List[str] = attr.ib(init=False)
    captured_date_lines: List[str] = attr.ib(init=False)
    normalized_dates: List[str] = attr.ib(init=False)
    date_patterns: DatePatterns = attr.ib(default=DatePatterns())

    def __attrs_post_init__(self):
        self.raw_captured_dates, self.captured_date_lines =\
            self.capture_all_dates()

        self.normalized_dates = self.normalize_dates()

    def capture_all_dates(self):
        raw_captured_dates = []
        captured_date_lines = []
        if self.full_text is not None:
            lines = self.full_text.split("\n")
            line_ctr = 0
            for l in lines:
                line_ctr += 1
                if "references" in l.lower():
                    break
                for pattern in self.date_patterns.DATE_PATTERNS:
                    if (pattern == self.date_patterns.NUM_MY_PATTERN
                            or pattern == self.date_patterns.STR_MY_PATTERN
                        ) and m is not None:
                        continue
                    m = None
                    matches = pattern.finditer(l)
                    for m in matches:
                        if self.raw_dates_as_dicts:
                            raw_captured_dates.append(m.groupdict())
                        else:
                            raw_captured_dates.append(m.group(0))
                        captured_date_lines.append(l)
        return raw_captured_dates, captured_date_lines

    def _extract_month(self, month_string: str) -> int:
        month_int = self.date_patterns.MONTH_NAME_MAP.get(month_string.lower())
        if not month_int:
            month_int = self.date_patterns.MONTH_ABBR_MAP[month_string.lower()]
        return month_int

    def extract_year_month_day(self, dt_match: Match):
        year = dt_match['year']
        if len(year) == 2:
            year = '20' + year
        month = dt_match['month']
        if len(month) > 2:
            month = str(self._extract_month(dt_match['month']))
        if len(month) == 1:
            month = '0' + month
        if dt_match.get('day') is not None:
            day = dt_match['day']
            if len(day) == 1:
                day = '0' + day
        else:
            day = '01'
        return '-'.join([year, month, day])

    def normalize_dates(self):
        normalized_dates = []
        for dt in self.raw_captured_dates:
            processed_dt = self.extract_year_month_day(dt)
            normalized_dates.append(processed_dt)
        return normalized_dates

    def find_copyright_year(self):
        if self.full_text is not None:
            all_years = []
            lines = self.full_text.split("\n")
            for l in lines:
                if '©' in l or '&copy;' in l or 'all rights reserved' in l.lower(
                ) or 'copy' in l.lower() or 'copyright' in l.lower():
                    years = regex.findall(r'(\d{4})', l)
                    for year in years:
                        # not in future
                        if int(year) <=\
                                int(datetime.datetime.utcnow().strftime('%Y')):
                            all_years.append(int(year))
            if len(all_years) > 0:
                return max(all_years)
        return None
