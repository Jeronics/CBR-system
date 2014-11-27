import sys
import preprocessMatches as ppm
import utils as ut
import match as read
import glob


def main(local, foreigner):
    # LOAD DATA
    dataset = []

    for files in glob.glob("../Data/*.csv"):
        dataset.append(files)

    # READ DATASET
    for data in dataset:
        # print data
        
        matches_data = read.read_match_dataset(data)

    # RESULTS OF 2003-04 AND 04-05 ARE GOING BAD
    # THE CSV IS NOT WELL OR THE PANDA IS NOT DOING IT WELL
    #
    # match es_data = read.read_match_dataset('../Data/LaLiga2003-04.csv.OLD')
    # matches_data = read.read_match_dataset('../Data/LaLiga2004-05.csv.OLD')

    # PREPROCESS DATASET RETRIEVE SIMILAR MATCHES
    matches_preprocessdata = ppm.preprocess(matches_data)

    for match in matches_preprocessdata:
        if str(match.local).__eq__(local) & str(match.foreign).__eq__(foreigner):
            print "Match " + str(match.local) + " vs " + str(match.foreign) + " on " + str(
                match.data) + " RESULT " + str(match.lGoals) + "-" + str(match.fGoals)
            # To know the week day
            # print ut.int_to_weekday(ut.date_to_day_of_week(match.data))
        if str(match.local).__eq__(foreigner) & str(match.foreign).__eq__(local):
            print "Match " + str(match.local) + " vs " + str(match.foreign) + " on " + str(
                match.data) + " RESULT " + str(match.lGoals) + "-" + str(match.fGoals)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
