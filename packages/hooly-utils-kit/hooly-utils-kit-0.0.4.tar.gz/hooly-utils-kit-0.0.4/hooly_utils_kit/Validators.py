from itertools import cycle
import datetime


class Validators:
    @staticmethod
    def is_rut_valid(rut: str) -> bool:
        """
           :param rut:
           :param rut_to_verify: The RUT (chilean) to be verified.
           :return: True if the passed RUT complies with the chilean RUT algorithm. False otherwise.
        """

        rut = rut.upper()
        rut = rut.replace("-", "")
        rut = rut.replace(".", "")
        aux = rut[:-1]
        dv = rut[-1:]

        reversed_rut = map(int, reversed(str(aux)))

        factors = cycle(range(2, 8))
        s = sum(d * f for d, f in zip(reversed_rut, factors))
        res = (-s) % 11

        if str(res) == dv:
            return True
        elif dv == "K" and res == 10:
            return True
        else:
            return False

    @staticmethod
    def is_composed_of_numbers(rut: str) -> bool:
        rut = rut[:-1]

        if rut.isdigit():
            return True
        else:
            return False

    @staticmethod
    def validate_date(date: str) -> bool:
        """
        :param date: date with format yy-mm-yyyy
        :return: True if the date is a valid date, otherwise return false
        """
        try:
            datetime.datetime.strptime(date, '%d-%m-%Y')
            return True
        except ValueError:
            return False
