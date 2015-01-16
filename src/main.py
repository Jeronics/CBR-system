from datetime import datetime
import sys
import wrapper as w
import internal_repr.phases as cbr
import glob
from joblib import Parallel, delayed
from wrapper import Match, MatchesCaseBase

 # ______________________________________________________________________
 #
 #
 #
 #       How to execute: e.g.
 #                  python main.py "Real Madrid" Barcelona
 #
 #
 # ______________________________________________________________________


def main_CBR(actual_match, matches, **kwargs):

    # 1-. RETRIEVE SIMILAR MATCHES

    threshold = kwargs['retrieve_thr'] if 'retrieve_thr' in kwargs else 0.01
    max_matches = kwargs['max_matches'] if 'max_matches' in kwargs else 5
    retrieved_matches, similarities = cbr.retrieve(matches, actual_match, w.similarity_function, threshold, max_matches)

    # print similarities
    # Print retrieved matches from the repository
    # ut.printMatches(retrieved_matches, similarities)

    # 2-. REUSE
    # REUSE the information retrieved from the archieves and predict a result and a score

    predicted_result = cbr.reuse(retrieved_matches, actual_match, similarities, cbr.substitutional_adaptation, w.specific_function)
    # print "predicted result = " + predicted_result
    # print "real result = " + actual_match.get_solution()

    # 3-. REVISE

    conf = cbr.revise(actual_match, w.expert_function, predicted_result)

    # 4-. RETAIN

    conf_thr = kwargs['conf_thr'] if 'conf_thr' in kwargs else 0.8
    sim_thr = kwargs['sim_thr'] if 'sim_thr' in kwargs else 1
    saved = cbr.retain(actual_match, matches, conf, conf_thr, similarities, sim_thr)

    # w.save_case_base(matches, '../data/Train/train.jpkl')
    return conf

if __name__ == '__main__':

    # Load the
    dataset = [files for files in glob.glob("../data/Train/*.csv")]
    matches_data = MatchesCaseBase()
    Parallel(n_jobs=8)(delayed(w.read_match_dataset)(dataset[i], matches_data) for i in range(len(dataset)))

    # if the main is called manually, this if/else-branch will be executed:
    # create a 'mock' match object with minimum information required and run the cbr for the given fixture
    if len(sys.argv) == 3:
        _, team1, team2 = sys.argv
        now = datetime.now()
        params = {'FTR': 'N/A',
                  'HomeTeam': team1,
                  'AwayTeam': team2,
                  'Date': '%s/%s/%s' % (now.day, now.month, now.year)}

        match = w.Match(params)
        conf = main_CBR(match)
        print "checking for manual input: %s" % str(match)
        print "result: %s" % conf
    else:
        # Read from JSON pickle
        # test_matches = w.read_case_base('../data/Test/test.jpkl')

        # Read from CSV file
        test_matches = w.read_from_csv('../data/Test/LaLiga2013-14.csv')
        # test_matches = w.read_from_csv('../data/Test/LaLiga2014-15 hasta diciembre.csv')

        i = 0
        for match in test_matches.get_case_values():
            conf = main_CBR(match, matches_data)
            i += int(conf[0])

        print 'Accuracy: {0}/{1}'.format(i, len(test_matches.get_case_values()))
