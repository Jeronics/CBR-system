import match as m
import utils as ut

# PREPROCESS THE MATCH LIST OBTAINED:
#
# + Erasing invalid values : NaN and so on
# + Erasing columns we don't need

def preprocess(matchList):
    matchListPreprocessed = []

    for match in matchList:
        # MAKE THE PREPROCESS WITH OF ALL THE DATA....
        matchListPreprocessed.append(match)

    return matchListPreprocessed


# Retrieve only matches with the same local and the same foreigner.
def retrieve(matchList, actualMatch, grade):
    similarMatchList = []

    for match in matchList:
        if (match.local == str(actualMatch.local)) & (match.foreign == str(actualMatch.foreign)):
            match = m.make_match(match.id, match.data, match.local, match.foreign, match.lGoals, match.fGoals,
                                 match.result)
            similarMatchList.append(match)
        if (grade > 1):
            if (match.foreign == str(actualMatch.local)) & (match.local == str(actualMatch.foreign)):
                match = m.make_match(match.id, match.data, match.local, match.foreign, match.lGoals, match.fGoals,
                                     match.result)
                similarMatchList.append(match)
    return similarMatchList

# Reuses the results of the retrieved matches having into account the time (days) that have passed from those matches.
def reuse(matchList, actualMatch):
    winProb = 0
    drawProb = 0
    loseProb = 0
    timeProb = []


    # We calculate how many days have passed since the game.
    for match in matchList:
        timeSinceGame = abs(actualMatch.data - match.data)
        timeProb.append(timeSinceGame.days)

    # Assign a probability to the time:
    #    + More probable result if nearer.
    #    + Less probable result if far away.

    newTP = []
    for t in timeProb:
        a = t-min(timeProb)
        b = max(timeProb)-min(timeProb)
        c = float(float(a)/float(b))
        newTP.append(1-c + 0.000000001)


    for idx, match in enumerate(matchList):
        # H = Home team wins.
        if (str(match.result) == str("H")):
            if (str(actualMatch.local) == str(match.local)):
                winProb = winProb + (1 * newTP[idx]);
            else:
                loseProb = loseProb + (1 * newTP[idx]);
        # A = Away team wins.
        elif (str(match.result) == str("A")):
            if (str(actualMatch.foreign) == str(match.foreign)):
                loseProb = loseProb + (1 * newTP[idx]);
            else:
                winProb = winProb + (1 * newTP[idx]);
        # D = Draw
        else:
            drawProb = drawProb + (1 * newTP[idx]);

    total = winProb+loseProb+drawProb

    print "win/home = " + str(winProb/total)
    print "lose/away = " + str(loseProb/total)
    print "draw = " + str(drawProb/total)

    probabilities = {'H': winProb/total, 'A': loseProb/total, 'D': drawProb/total}

    probability = max(winProb/total, loseProb/total, drawProb/total)
    result = max(probabilities, key=probabilities.get)

    actualMatch.result = result
    return actualMatch, probability