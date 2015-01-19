from datetime import datetime
import sys
import copy
import os
import pickle as pk

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
    return confidence, predicted_result


def get_matches():
    #fix for pythonanywhere.com
    my_dir = os.path.dirname(__file__)
    f = open(os.path.join(my_dir,'../../data/Train/train.pkl'), 'rb')
    matches_data = pk.load(f)
    f.close()
    orig_data = copy.deepcopy(matches_data)
    return orig_data

def run(input_match=None):
    # Load the
    print 'Loading data ...'
    orig_data = get_matches()
    print 'Start CBR ...'
    # if the main is called manually, this if/else-branch will be executed:
    # create a 'mock' match object with minimum information required and run the cbr for the given fixture
    conf, prediction_result = main_CBR(input_match, orig_data)
    output = "checking for manual input: %s\n" % str(input_match)
    output += "result: %s" % conf
    output += "prediction_result: %s" % prediction_result
    print output
    return prediction_result


def gen_input_match(team1, team2, odds={}):
    match_date = datetime.now()
    params = Match.gen_params(team1, team2, match_date, odds)
    input_match = w.Match(params)
    print "params=%s" % params
    return input_match

if __name__ == '__main__':
    _, team1, team2 = sys.argv
    input_match = gen_input_match(team1, team2)
    run(input_match)
