import datetime


def date_to_day_of_week(date):
    """
    takes a date and returns day of the week
    :return:
    """
    return date.weekday()


def diff_in_league_years(last_date, earlier_date):
    """
    Finds how many leagues have passed from one date to the other

    :param last_date (datetime.datetime.date object):
    :param earlier_date (datetime.datetime.date object):

    :return: league year differences: 0 if in the same league year etc.
    """
    return subtract_months(last_date, 6).year - subtract_months(earlier_date, 6).year


def subtract_months(date, months):
    """
    Subtracts 6 months from a date.
    Warning: The days are set to 01 to avoid problems in monthly day variations

    :param date: (datetime.datetime.object)
    :param months: (int) number of months to subtract
    :return: (datetime.datetime.object) a new date 6 months earlier but with day=1
    """
    if months < 0:
        months = abs(months)
    date_x = date.replace(day=1)

    difference = (date.month - months)
    new_month = difference % 12
    diff_year = (months - 1) / 12 + (1 if difference <= 0 else 0)
    if new_month == 0:
        new_month = 12
    date_x = date_x.replace(year=date.year - diff_year)

    date_x = date_x.replace(month=new_month)
    return date_x


def return_football_season(date=datetime.datetime.today()):
    """
    Returns the football season in which a date is in. By default it gets today's date
    :type date: datetime.datetime.date object
    :param date:

    :type season: str
    :return season: football season in this format: 'XXXX-YY'
    """
    date_aux = subtract_months(date, 6)
    beginning_year = str(date_aux.year)
    ending_year = date_aux.year + 1
    ending_year = str(ending_year)[-2:]
    season = ''.join([beginning_year, '-', ending_year])
    return season


def date_to_python_date(date):
    """
    parse possibly 'impure' string date into the string date object
    :type date: str
    :param date: string date represendation

    :type ret_date: str
    :param ret_date: string representation of the date
    """
    try:
        ret_date = datetime.datetime.strptime(date, "%d/%m/%y")
    except ValueError:
        #another format -- a year can also have four digits
        ret_date = datetime.datetime.strptime(date, "%d/%m/%Y")
    return ret_date