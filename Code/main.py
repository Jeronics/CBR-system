import sys
import preprocessMatches as ppm
import utils as ut
import match as read
import glob



 # ______________________________________________________________________
 #
 #
 #
 #       How to execute: e.g.
 #                  python main.py "Real Madrid" Barcelona
 #
 #
 # ______________________________________________________________________


def main(local, foreigner):

    # 1-. LOAD DATA
    dataset = []

    for files in glob.glob("../Data/*.csv"):
        dataset.append(files)

    # 2-. READ DATASET
    for data in dataset:
        matches_data = read.read_match_dataset(data)

    # TODO: 3-. PREPROCESS DATASET



    # 4-. RETRIEVE SIMILAR MATCHES

    # Grade of similarity:
    #   When grade higher less similarity.
    #   e.g:
    #         grade = 1  --> highest similarity, return only matches of local as local.
    #         grade = 2  --> less similarity, return matches of locals as local and foreign.

    grade = 2
    matches_retrieved = ppm.retrieve(matches_data, local, foreigner, grade)



    # TODO 5-. REUSE

    # TODO 6-. REVISE

    # TODO 7-. RETAIN

    # Print matches
    ut.printMatches(matches_retrieved)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
