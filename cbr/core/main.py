from datetime import datetime
import sys
import glob
import copy
import pickle as pk

from joblib import Parallel, delayed
import numpy as np

import cbr.core.internal_repr.phases as cbr
from cbr.core.wrapper import MatchesCaseBase, Match
from cbr.core import wrapper as w
import multiprocessing

# ______________________________________________________________________
#
#
#
#       How to execute: e.g.
#                  python hello.py "Real Madrid" Barcelona
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

    predicted_result = cbr.reuse(retrieved_matches, actual_match, similarities, cbr.substitutional_adaptation, w.reuse_matches)
    # print "predicted result = " + predicted_result
    # print "real result = " + actual_match.get_solution()

    # 3-. REVISE
    confidence, actual_match = cbr.revise(actual_match, w.expert_function, predicted_result)

    # 4-. RETAIN

    conf_thr = kwargs['conf_thr'] if 'conf_thr' in kwargs else 0.8
    sim_thr = kwargs['sim_thr'] if 'sim_thr' in kwargs else 1

    cbr.retain(actual_match, matches, confidence, conf_thr, similarities, sim_thr)
    return confidence


def test(orig_data, test_matches, n, params):
    m, thr1, thr2, thr3 = params
    matches_data = copy.deepcopy(orig_data)
    i = 0
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
    return acc, lc


def run(args=[]):
    # Load the
    print 'Loading data ...'
    num_cpu = multiprocessing.cpu_count()

    # dataset = [files for files in glob.glob("../../data/Train/*.csv")]
    # matches_data = MatchesCaseBase()
    # Parallel(n_jobs=1)(delayed(w.read_match_dataset)(dataset[i], matches_data) for i in range(len(dataset)))

    f = open('../../data/Train/train1.pkl', 'rb')
    matches_data = pk.load(f)
    f.close()

    orig_data = copy.deepcopy(matches_data)

    print 'Start CBR ...'
    # if the main is called manually, this if/else-branch will be executed:
    # create a 'mock' match object with minimum information required and run the cbr for the given fixture
    if len(args) == 3:
        _, team1, team2 = args
        now = datetime.now()
        params = {'FTR': 'N/A',
                  'HomeTeam': team1,
                  'AwayTeam': team2,
                  'Date': '%s/%s/%s' % (now.day, now.month, now.year)}

        match = w.Match(params)
        conf = main_CBR(match, orig_data)
        output = "checking for manual input: %s\n" % str(match)
        output += "result: %s" % conf
        print output
        return output
    else:
        # Read from CSV file
        f = open('../../data/Test/LaLiga2013-14.csv', 'rb')
        test_matches = pk.load(f)
        f.close()

        n = len(test_matches.get_case_values())

        # Create grid of parameters
        max_m = range(3, 13)
        r1_threshold = np.array(range(1, 10))/10.0
        conf_threshold = np.array(range(1, 10))/10.0
        sim_threshold = np.array(range(1, 10))/10.0

        params = []
        for m in max_m:
            for thr1 in r1_threshold:
                for thr2 in conf_threshold:
                    for thr3 in sim_threshold:
                        params.append([m, thr1, thr2, thr3])

        r = Parallel(n_jobs=num_cpu, verbose=3)(delayed(test)(orig_data, test_matches, n, params[i]) for i in range(len(params)))
        acc, lc = zip(*r)

        best_acc = max(acc)
        idx = acc.index(best_acc)
        best_param = params[idx]
        best_lc = lc[idx]

        print '\n--------- BEST PARAMETERS -----------'
        print best_param
        print '\n--------- BEST ACCURACY -----------'
        print best_acc
        print '\n--------- BEST LEARNING CURVE -----------'
        print best_lc

        f = open('../../data/Results/results.csv', 'w')
        f.write('# Learning Curve\n')
        for i in best_lc:
            f.write(str(i) + ',')

        f.write('\n# Best Parameters (max_matches, retreave_threshold, confidence_threshold, similarity_threshold)\n')
        for i in best_param:
            f.write(str(i) + ',')
        f.close()

if __name__ == '__main__':
    run(sys.argv)