import match as m

# PREPROCESS THE MATCH LIST OBTAINED:
#
# + Erasing invalid values : NaN and so on
#   + Erasing columns we don't need

def preprocess(matchList):
    matchListPreprocessed = []

    for match in matchList:
        # MAKE THE PREPROCESS WITH OF ALL THE DATA....
        matchListPreprocessed.append(match)

    return matchListPreprocessed


# Retrieve only matches with the same local and the same foreigner.
def retrieve(matchList, local, foreign, grade):
    similarMatchList = []

    for match in matchList:
        if (match.local == str(local)) & (match.foreign == str(foreign)):
            match = m.make_match(match.id, match.data, match.local, match.foreign, match.lGoals, match.fGoals, match.result)
            similarMatchList.append(match)
        if (grade > 1):
            if (match.foreign == str(local)) & (match.local == str(foreign)):
                match = m.make_match(match.id, match.data, match.local, match.foreign, match.lGoals, match.fGoals, match.result)
                similarMatchList.append(match)
    return similarMatchList