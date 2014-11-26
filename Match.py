__author__ = 'Iosu'



class Match(object):
    id = 0
    local = ""
    foreign = ""
    # HERE WE HAVE TO DISCUSS THE ATTRIBUTES OF THE MATCH TO RETRIEVE SIMILAR MATCHES.
    #     For example:
    #         + referee.
    #         + local team quality.
    #         + foreign team quality.
    #

    # The class "constructor" - It's actually an initializer
    def __init__(self, id, local, foreign):
        self.id = id
        self.local = local
        self.foreign = foreign

def make_match(id, local, foreign):
    match = Match(id, local, foreign)
    return match