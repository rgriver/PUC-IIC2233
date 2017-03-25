class DateTime:
    def __init__(self):
        self.year = 2016
        self.month = 2
        self.day = 28
        self.hour = 23
        self.minute = 59
        self.second = 59

    def add_seconds(self, delta):
        while delta != 0:
            if self.second + delta > 59:
                delta -= 60 - self.second
                self.second = 0
                if self.minute == 59:
                    self.minute = 0
                    if self.hour == 23:
                        self.hour = 0
                        self.change_date()
                    else:
                        self.hour += 1
                else:
                    self.minute += 1
            else:
                self.second += delta
                delta = 0

    def change_date(self):
        months_with_30 = [4, 6, 9, 11]
        if self.day == 29 and self.month == 2:
            self.day = 1
            self.month += 1
        elif self.day == 28 and self.month == 2:
            if self.leap_year(self.year):
                self.day += 1
            else:
                self.day = 1
                self.month += 1
        elif self.day == 30 and self.month in months_with_30:
            self.day = 1
            self.month += 1
        elif self.day == 31 and self.month not in months_with_30:
            if self.month == 12:
                self.month = 1
                self.day = 1
                self.year += 1
            else:
                self.day = 1
                self.month += 1
        else:
            self.day += 1

    @staticmethod
    def leap_year(year):
        if not year % 4:
            if not year % 100:
                if not year % 400:
                    return True
            else:
                return True
        return False

    def set_date_time(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def get_formatted_date_time(self):
        word = str(self.year) + '-' + str(self.month).zfill(2) + '-' + \
               str(self.day).zfill(2) + ' ' + str(self.hour).zfill(2) + ':' + \
               str(self.minute).zfill(2) + ':' + str(self.second).zfill(2)
        return word

    def set_formatted_date_time(self, word):
        word = word.split(' ')
        date = word[0]
        date = date.split('-')
        self.year = int(date[0])
        self.month = int(date[1])
        self.day = int(date[2])
        time = word[1]
        time = time.split(':')
        self.hour = int(time[0])
        self.minute = int(time[1])
        self.second = int(time[2])

    def __sub__(self, other):
        result = 0
        k = 1
        start = DateTime()
        end = DateTime()
        if self.get_formatted_date_time() > other.get_formatted_date_time():
            start.set_formatted_date_time(other.get_formatted_date_time())
            end.set_formatted_date_time(self.get_formatted_date_time())
        else:
            start.set_formatted_date_time(self.get_formatted_date_time())
            end.set_formatted_date_time(other.get_formatted_date_time())
        while start.get_formatted_date_time() != end.get_formatted_date_time():
            start.add_seconds(1)
            result += 1
        return result * k



