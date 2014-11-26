__author__ = 'Iosu'

import Match as m


def main(matchList):
    matchListPreprocessed = []
    matchPreprocessed = ""

    for match in matchList:
        matchPre = m.make_match(match.data, match.local, match.foreign)
        matchListPreprocessed.append(matchPre)

    return matchListPreprocessed