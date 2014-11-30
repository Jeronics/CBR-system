import datetime

def isNaN(x):
    if x != x:
        return True
    else:
        return False

def date_to_day_of_week(date):
    '''
    takes a date and returns day of the week
    :return:
    '''
    return date.weekday()


def date_to_python_date(date):
    # print date
    return datetime.datetime.strptime(date, "%d/%m/%y")

def int_to_weekday(day):
    '''

    Returns day of the week from an integer
    :param day:
    :return:
    '''
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

# TEST
# date = "3/2/08"
# print int_to_weekday(date_to_day_of_week(date))
