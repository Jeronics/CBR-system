from datetime import datetime
import sys
import wrapper as w
import internal_repr.phases as cbr
import glob
from joblib import Parallel, delayed
from wrapper import MatchesCaseBase
import copy
import numpy as np

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

    confidence, actual_match = cbr.revise(actual_match, w.expert_function, predicted_result)

    # 4-. RETAIN

    conf_thr = kwargs['conf_thr'] if 'conf_thr' in kwargs else 0.8
    sim_thr = kwargs['sim_thr'] if 'sim_thr' in kwargs else 1

    cbr.retain(actual_match, matches, confidence, conf_thr, similarities, sim_thr)
    return confidence

if __name__ == '__main__':

    # Load the
    print 'Loading data ...'
    dataset = [files for files in glob.glob("../data/Train/*.csv")]
    matches_data = MatchesCaseBase()
    Parallel(n_jobs=8)(delayed(w.read_match_dataset)(dataset[i], matches_data) for i in range(len(dataset)))

    orig_data = copy.deepcopy(matches_data)

    print 'Start CBR ...'
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
        # Read from CSV file
        test_matches = w.read_from_csv('../data/Test/LaLiga2013-14.csv')
        test_matches

        n = len(test_matches.get_case_values())

        # Create grid of parameters
        max_m = range(3, 13)
        r1_threshold = np.array(range(1, 10))/10.0
        conf_threshold = np.array(range(1, 10))/10.0
        sim_threshold = np.array(range(1, 10))/10.0

        best_param = {}
        best_acc = 0
        best_lc = []
        count = 0
        for m in max_m:
            for thr1 in r1_threshold:
                for thr2 in conf_threshold:
                    for thr3 in sim_threshold:
                        matches_data = copy.deepcopy(orig_data)
                        i = 0
                        count += 1
                        lc = []
                        for match in test_matches.get_case_values():
                            conf = main_CBR(actual_match=match,
                                            matches=matches_data,
                                            max_matches=m,
                                            retrieve_thr=thr1,
                                            conf_thr=thr2,
                                            sim_thr=thr3)
                            i += int(conf)
                            lc.append(i)
                        acc = i*(100/float(n))
                        if acc > best_acc:
                            best_acc = acc
                            best_lc = lc
                            best_param = {'m': m, 'retr_thr': thr1, 'conf_thr': thr2, 'sim_thr': thr3}

                        print '{4}/{5} - Accuracy: {0}/{1} - Best Accuracy: {2} - Best param: {3}'.format(i, n,
                                                                                                          best_acc,
                                                                                                          best_param,
                                                                                                          count,
                                                                                                          len(max_m)*len(r1_threshold)*len(conf_threshold)*len(sim_threshold))

        print '\n\n--------- BEST PARAMETERS -----------'
        print best_param
        print '\n--------- BEST ACCURACY -----------'
        print best_acc

        f = open('data/Results/results_long.csv', 'w')
        f.write('# Learning Curve')
        for i in best_lc:
            f.write(str(i))

        f.write('# Best Parameters')
        for i in best_param.keys():
            f.write(i + ': ' + str(best_param[i]))
        f.close()