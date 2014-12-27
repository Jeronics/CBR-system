import wrapper as w
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


def main(actual_match):

    # 1-. LOAD DATA

    dataset = '../data/Train/train.jpkl'
    matches = w.read_case_base(dataset)

    # 2-. RETRIEVE SIMILAR MATCHES

    threshold = 0.01
    max_matches = 10
    retrieved_matches, similarities = cbr.retrieve(matches, actual_match, w.similarity, threshold, max_matches)

    # print similarities

    # Print retrieved matches from the repository
    # ut.printMatches(retrieved_matches, similarities)

    # TODO 5-. REUSE
    # REUSE the information retrieved from the archieves and predict a result and a score

    predicted_result = cbr.reuse(retrieved_matches, actual_match, similarities, cbr.substitutional_adaptation, w.adapt_match_result)
    print "predicted result = " + predicted_result
    print "real result = " + actual_match.get_solution()

    # TODO 6-. REVISE

    conf = cbr.revise(actual_match, w.expert, predicted_result)
    # TODO 7-. RETAIN

    conf_thr = 0.5
    sim_thr = 1
    saved = cbr.retain(actual_match, matches, conf, conf_thr, similarities, sim_thr)

    # w.save_case_base(matches, '../data/Train/train.jpkl')
    return conf

if __name__ == '__main__':

    # Read from JSON pickle
    # test_matches = w.read_case_base('../data/Test/test.jpkl')

    # Read from CSV file
    test_matches = w.read_from_csv('../data/Test/ultimaJornada.csv')
    # test_matches = w.read_from_csv('../data/Test/LaLiga2014-15 hasta diciembre.csv')
    i = 0
    for match in test_matches.get_case_values():
        print match
        conf = main(match)
        # break
        i += int(conf[0])

    print 'Accuracy: {0}/{1}'.format(i, len(test_matches.get_case_values()))
