from datetime import datetime


class GormanianDatetime:
    _MONTHS = ['March', 'April', 'May', 'June', 'Quintilis', 'Sextilis', 'September', 'October', 'November', 'December',
               'January', 'February', 'Gormanuary']
    _DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    _WEEK_LENGTH = 7
    _MONTH_LENGTH = 28

    def __init__(self, date: datetime):
        self._dayofyear = date.timetuple().tm_yday

        if self._dayofyear >= 365:
            self.day = ""
            self.day_string = "Intermission"
            self.week = ""
            self.month_string = ""
            self.month = ""
            self.year = date.year
            self.intermission = True
        else:
            self.day = self._calculate_day()
            self.day_string = self._calculate_day_str()
            self.day_suffix = self._calculate_day_suffix()
            self.week = self._calculate_week()
            self.month_string = self._calculate_month()
            self.month = self._calculate_month_int()
            self.year = date.year
            self.intermission = False

        self.as_string = self.__str__()
        self.isoformat = self._iso_format()

    def __str__(self):
        return f"{self.day_string} {self.day}{self.day_suffix} {self.month_string} {self.year}"

    def _iso_format(self):
        return f"{self.year}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)}"

    def _calculate_day(self):
        a = self._dayofyear % self._MONTH_LENGTH
        return a

    def _calculate_day_suffix(self):
        if self.day in [1, 21]:
            return "st"
        elif self.day in [2, 22]:
            return "nd"
        elif self.day in [3, 23]:
            return "rd"
        else:
            return "th"

    def _calculate_day_str(self):
        a = self._dayofyear % len(self._DAYS)
        day_str = self._DAYS[a]
        return day_str

    def _calculate_week(self):
        week_int = self._dayofyear // self._WEEK_LENGTH
        return week_int

    def _calculate_month(self):
        month_int = self._dayofyear // self._MONTH_LENGTH
        month = self._MONTHS[month_int]
        return month

    def _calculate_month_int(self):
        month_int = self._dayofyear // self._MONTH_LENGTH
        return month_int


def convert(datetime_obj: datetime):
    gormanian_datetime = GormanianDatetime(datetime_obj)
    return gormanian_datetime


def now():
    gormanian_datetime = GormanianDatetime(datetime.now())
    return gormanian_datetime
