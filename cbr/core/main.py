from datetime import datetime
import sys
import copy
import pickle as pk

from joblib import Parallel, delayed
import numpy as np

import cbr.core.internal_repr.phases as cbr
from cbr.core.wrapper import MatchesCaseBase, Match
from cbr.core import wrapper as w
import multiprocessing

num_cpu = multiprocessing.cpu_count()

# ______________________________________________________________________
#
#       How to execute: e.g.
#                  python hello.py "Real Madrid" Barcelona
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


def get_matches():
    f = open('../../data/Train/train.pkl', 'rb')
    matches_data = pk.load(f)
    f.close()
    orig_data = copy.deepcopy(matches_data)
    return orig_data


def run(args=[]):
    # Load the
    print 'Loading data ...'
    orig_data = get_matches()
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
        pass

if __name__ == '__main__':
    run(sys.argv)