import datetime


def isNaN(x):
    return True if x != x else False


def date_to_day_of_week(date):
    """
    takes a date and returns day of the week
    :return:
    """
    return date.weekday()

def diff_in_league_years(last_date, earlier_date):
    '''
    Finds how many leagues have passed from one date to the other

    :param last_date (datetime.datetime.date object):
    :param earlier_date (datetime.datetime.date object):

    :return: league year differences: 0 if in the same league year etc.
    '''
    return subtract_months(last_date,6).year-subtract_months(earlier_date,6).year

def subtract_months(date, months):
    '''
    Subtracts 6 months from a date.
    Warning: The days are set to 01 to avoid problems in monthly day variations

    :param date: (datetime.datetime.object)
    :param months: (int) number of months to subtract
    :return: (datetime.datetime.object) a new date 6 months earlier but with day=1
    '''
    if months < 0:
        months = abs(months)
    date_x = date.replace(day=1)

    difference = (date.month - months)
    new_month = difference % 12
    diff_year = (months - 1 )/ 12 + (1 if difference <= 0 else 0)
    if new_month == 0:
        new_month = 12
    date_x = date_x.replace(year=date.year - diff_year)

    date_x = date_x.replace(month=new_month)
    return date_x

def date_to_python_date(date):
    # print date
    return datetime.datetime.strptime(date, "%d/%m/%y")


def int_to_weekday(day):
    """

    Returns day of the week from an integer
    :param day:
    :return:
    """
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return week[day]


def daysNumber(time):
    return datetime.datetime.day(time)


def printMatches(matches):
    for match in matches:
        print "Match " + str(match.local) + " vs " + str(match.foreign) + " on " + str(
               match.data) + " RESULT " + str(match.lGoals) + "-" + str(match.fGoals)


def printResult(match, probability):
    if str(match.result) == str("H"):
        print str(match.local) +" wins the game with a probability of "+str(probability)+"%"
    elif str(match.result) == str("L"):
        print str(match.local) +" looses the game with a probability of "+str(probability)+"%"
    else:
        print "draw with a probability of "+str(probability)+"%"

def printMatches(matches, similarity, actualMatch):
    for match in matches:
        print str(match.name) + ' | sim: ' + str(similarity(match, actualMatch))

# TEST
# date = "3/2/08"
# print int_to_weekday(date_to_day_of_week(date))
