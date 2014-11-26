
import sys
import preprocessMatches as ppm
import utils as ut
import match as read

def main(local, foreigner):

    # LOAD DATA
    dataset = "../Data/Example2013-14.csv"

    # READ DATASET
    matches_data = read.read_match_dataset(dataset)

    # PREPROCESS DATASET
    matches_preprocessdata = ppm.preprocess(matches_data)


    for match in matches_preprocessdata:
        # print match.local
        if str(match.local).__eq__(local) & str(match.foreign).__eq__(foreigner) :
            print "Match "+str(match.local)+" vs "+str(match.foreign)+" on "+str(match.data)

        # To know the week day
        # print ut.int_to_weekday(ut.date_to_day_of_week(match.data))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
