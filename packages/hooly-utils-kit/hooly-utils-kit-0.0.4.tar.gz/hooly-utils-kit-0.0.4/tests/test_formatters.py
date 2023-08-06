import unittest
import datetime
from hooly_utils_kit import Formatters


class TestFormatter(unittest.TestCase):

    # setUp method to be executed first
    # create an object of Validator class and save it as a class attribute
    def setUp(self) -> None:
        self.formatters = Formatters

    # tests for formatter rut
    def test_datetime_formatter(self):
        test_date = "06-09-1995"
        time_flag = 0
        date_formatted = self.formatters.format_to_datetime(test_date, time_flag)
        self.assertIsInstance(date_formatted, datetime.datetime)

    def test_datetime_formatter_fail(self):
        test_date = "06-09"
        time_flag = 0
        date_formatted = self.formatters.format_to_datetime(test_date, time_flag)
        self.assertIsInstance(date_formatted, IndexError.__class__)

    # tests for formatter rut
    def test_phone_number_formatter(self):
        test_phone_number = "961315674"
        phone_number_formatted = self.formatters.format_phone_number(test_phone_number)
        self.assertIsInstance(phone_number_formatted, str)