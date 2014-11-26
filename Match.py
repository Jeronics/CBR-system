__author__ = 'Iosu'



class Match(object):
    data = 0
    local = ""
    foreign = ""
    # HERE WE HAVE TO DISCUSS THE ATTRIBUTES OF THE MATCH TO RETRIEVE SIMILAR MATCHES.
    #     For example:
    #         + referee.
    #         + local team quality.
    #         + foreign team quality.
    #

    # The class "constructor" - It's actually an initializer
    def __init__(self, data, local, foreign):
        self.data = data
        self.local = local
        self.foreign = foreign

def make_match(data, local, foreign):
    match = Match(data, local, foreign)
    return match

def read_match_dataset(dataset):
    # Read TweetLID dataset
    matchList = []
    with open(dataset) as file:
        for l in file.readlines():
            line = l.strip().split(";")
            match = make_match(line[1], line[2], line[3])
            matchList.append(match)
        file.close()
    return matchList