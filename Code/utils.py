import datetime


def date_to_day_of_week(date):
    '''
    takes a date and returns day of the week
    :return:
    '''
    return date.weekday()

def date_to_python_date(date):
   return datetime.datetime.strptime(date, "%d/%M/%y")

def int_to_weekday(day):
    '''
    Returns day of the week from an integer
    :param day:
    :return:
    '''
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return week[day]


# TEST
# date = "3/2/08"
# print int_to_weekday(date_to_day_of_week(date))
