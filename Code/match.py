import utils as ut
import pandas as pd
import datetime as dt

# HERE WE HAVE TO DISCUSS THE ATTRIBUTES OF THE MATCH TO RETRIEVE SIMILAR MATCHES.
#     For example:
#         + referee.
#         + local team quality.
#         + foreign team quality.
#

class Match(object):
    id = 0
    data = dt.datetime.now()
    local = ""
    foreign = ""
    lGoals = 0
    fGoals = 0
    # RESULT OF MATCH
        # L = Local wins.
        # D = Draw
        # F = Foreign wins.
    result = "D"





    # The class "constructor" - It's actually an initializer
    def __init__(self, id, data, local, foreign, lGoals, fGoals, result):
        self.id = id
        self.data = data
        self.local = local
        self.foreign = foreign
        self.lGoals = lGoals
        self.fGoals = fGoals
        self.result = result


def make_match(id, data, local, foreign, lGoals, fGoals, result):
    match = Match(id, data, local, foreign, lGoals, fGoals, result)
    return match

def read_match_dataset(dataset):
    matchList = []
    data_2013_2014 = pd.io.parsers.read_csv(dataset, ';')
    for line in data_2013_2014.iterrows():
        match = make_match(line[0], ut.date_to_python_date(line[1][1]), line[1][2], line[1][3], line[1][4], line[1][5], line[1][6])
        matchList.append(match)
    return matchList