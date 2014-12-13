import sys
import cbrMatches as cbrm
import utils as ut
import match as read
import glob
import datetime as dt
import wrapper as w
from wrapper import MatchesCaseBase, Match


 # ______________________________________________________________________
 #
 #
 #
 #       How to execute: e.g.
 #                  python main.py "Real Madrid" Barcelona
 #
 #
 # ______________________________________________________________________


def main(actualMatch):

    # 1-. LOAD DATA
    # dataset = []
    #
    # for files in glob.glob("../data/*.csv"):
    #     dataset.append(files)

    dataset = '../data/Train/train.jpkl'
    matches = w.read_case_base(dataset)

    print matches.get_case_values()[0].get_home()

    # 2-. READ DATASET
    # for data in dataset:
    #     matches_data = read.read_match_dataset(data)

    # TODO: 3-. PREPROCESS DATASET



    # 4-. RETRIEVE SIMILAR MATCHES

    # Grade of similarity:
    #   When grade higher less similarity.
    #   e.g:
    #         grade = 1  --> highest similarity, return only matches of local as local.
    #         grade = 2  --> less similarity, return matches of locals as local and foreign.

    # grade = 1
    # matches_retrieved = cbrm.retrieve(matches_data, actualMatch, grade)

    # TODO 5-. REUSE
    # REUSE the information retrieved from the archieves and predict a result and a score
    # actualMatch, probability = cbrm.reuse(matches_retrieved, actualMatch)

    # TODO 6-. REVISE

    # TODO 7-. RETAIN

    # Print matches
    # ut.printMatches(matches_retrieved)

    # Print result
    # ut.printResult(actualMatch, probability * 100)


if __name__ == '__main__':

    test_matches = w.read_case_base('../data/Test/test.jpkl')

    for match in test_matches.get_case_values():
        main(match)
