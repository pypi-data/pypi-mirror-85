from datetime import datetime


class Formatters:
    @staticmethod
    def format_phone_number(phone_number: str) -> str:
        """
            :param phone_number: the phone number to be transformed, in case is necessary, to a valid phone number (+56XXXXXXXXX)
            :return: The formatted phone number. As an String.
            """

        formatted_phone_number = str(phone_number).strip()

        if len(phone_number) is not 12:
            if len(phone_number) is 9:
                formatted_phone_number = "+56" + formatted_phone_number
                return formatted_phone_number

            if len(phone_number) is 8:
                formatted_phone_number = "+569" + formatted_phone_number
                return formatted_phone_number

        return formatted_phone_number

    @staticmethod
    def format_to_datetime(date, time_flag) -> datetime:
        """
        :param date: the specific date (dd-mm-yyyy) to be transformed in datetime format
        :param time_flag: specific if the date to be transformed with first hour of day (00:00:00) or end (23:59:59)
        :return: return a datetime
        """

        # slit dd/mm/yyyy in separate dates
        try:
            year = int(date.split("-")[2])
            month = int(date.split("-")[1])
            day = int(date.split("-")[0])

            if time_flag == 0:
                datetime_format = datetime(year, month, day, 00, 00, 00)
                return datetime_format

            datetime_format = datetime(year, month, day, 23, 59, 59)
            return datetime_format
        except IndexError:
            return IndexError
        except (ValueError, TypeError):
            return {"message": "an error occurred formatting date"}
