import utils as ut
import pandas as pd
import datetime as dt

# HERE WE HAVE TO DISCUSS THE ATTRIBUTES OF THE MATCH TO RETRIEVE SIMILAR MATCHES.
# For example:
# + referee.
# + local team quality.
#         + foreign team quality.
#

matchList = []


class Match(object):
    id = 0
    data = dt.datetime.now()
    local = ""
    foreign = ""
    lGoals = 0
    fGoals = 0
    # RESULT OF MATCH
    # H = Local wins.
    # D = Draw
    # A = Foreign wins.
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
    data = pd.read_csv(dataset, error_bad_lines=False)
    for line in data.iterrows():
        match = make_match(line[0], ut.date_to_python_date(line[1][1]), str(line[1][2]), str(line[1][3]), int(line[1][4]),
                            int(line[1][5]), str(line[1][6]))
        matchList.append(match)
    return matchList