import unittest
from hooly_utils_kit import Validators


class TestValidator(unittest.TestCase):

    # setUp method to be executed first
    # create an object of Validator class and save it as a class attribute
    def setUp(self) -> None:
        self.validators = Validators

    # tests for validator rut
    def test_is_rut_valid(self):
        test_rut = "18788484-5"
        self.assertEqual(self.validators.is_rut_valid(test_rut), True)

    def test_is_not_rut_valid(self):
        test_rut = "187884-5"
        self.assertEqual(self.validators.is_rut_valid(test_rut), False)

    # tests to test string composed of numbers
    def test_is_composed_of_numbers(self):
        test_value = "9191"
        self.assertEqual(self.validators.is_composed_of_numbers(test_value), True)

    def test_is_not_composed_of_numbers(self):
        test_value = "some_value2"
        self.assertEqual(self.validators.is_composed_of_numbers(test_value), False)

    # tests for validator date
    def test_valid_date(self):
        test_date = "06-09-1995"
        self.assertEqual(self.validators.validate_date(test_date), True)

    def test_invalid_date(self):
        test_date = "35-09-1995"
        self.assertEqual(self.validators.validate_date(test_date), False)