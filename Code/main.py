
import sys
import preprocessMatches as ppm
import utils as ut
import match as read
import glob

def main(local, foreigner):

    # LOAD DATA
    dataset = []

    # for files in glob.glob("../Data/*.csv"):
    #     dataset.append(files)

    # READ DATASET
    # for data in dataset:
    #     matches_data = read.read_match_dataset(data)
    # matches_data = read.read_match_dataset('../Data/LaLiga2003-04.csv')error
    matches_data = read.read_match_dataset('../Data/LaLiga2004-05.csv')

    # PREPROCESS DATASET RETRIEVE SIMILAR MATCHES
    matches_preprocessdata = ppm.preprocess(matches_data)


    for match in matches_preprocessdata:
        # print match.local
        if str(match.local).__eq__(local) & str(match.foreign).__eq__(foreigner) :
            print "Match "+str(match.local)+" vs "+str(match.foreign)+" on "+str(match.data)+" RESULT "+str(match.lGoals) +"-"+str(match.fGoals)
        # To know the week day
        # print ut.int_to_weekday(ut.date_to_day_of_week(match.data))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
