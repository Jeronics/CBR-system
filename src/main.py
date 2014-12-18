import wrapper as w
import utils as ut
from wrapper import MatchesCaseBase, Match
import internal_repr.phases as cbr

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

    dataset = '../data/Train/train_original.jpkl'
    matches = w.read_case_base(dataset)

    # 2-. RETRIEVE SIMILAR MATCHES

    threshold = 0.01
    max_matches = 10
    retrieved_matches, similarities = cbr.retrieve(matches, actualMatch, w.similarity, threshold, max_matches)

    print actualMatch.__str__()
    print 'home '+actualMatch.get_home() + '  away '+actualMatch.get_away()
    print similarities

    # Print retrieved matches from the repository
    # ut.printMatches(retrieved_matches, w.similarity, actualMatch)

    # TODO 5-. REUSE
    # REUSE the information retrieved from the archieves and predict a result and a score

    predicted_result = cbr.reuse(retrieved_matches, actualMatch, similarities)
    print "predicted result = " + predicted_result
    print "real result = " + actualMatch.get_solution()

    # TODO 6-. REVISE

    conf = cbr.revise(actualMatch, w.expert, predicted_result)
    # TODO 7-. RETAIN

    thr = 0.5
    saved = cbr.retain(actualMatch, matches, conf, thr)


    # w.save_case_base(matches, '../data/Train/train.jpkl')
    return conf

if __name__ == '__main__':

    # Read from JSON pickle
    # test_matches = w.read_case_base('../data/Test/test.jpkl')

    # Read from CSV file
    test_matches = w.read_from_csv('../data/Test/ultimaJornada.csv')
    i = 0
    for match in test_matches.get_case_values():
        print match.__str__()
        conf = main(match)
        i = i + int(conf[0])

    print 'partidos acertados = '+str(i)