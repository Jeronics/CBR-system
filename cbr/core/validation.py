import copy
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from main import main_CBR, get_matches
from wrapper import MatchesCaseBase, Match, read_match_dataset
from joblib import Parallel, delayed

num_cpu = multiprocessing.cpu_count()


def plot_lc(lc, name):
    aux = np.array(range(1, len(lc[0])+1))*1.0
    x1 = np.array(lc[0])/aux
    x2 = np.array(lc[1])/aux
    plt.figure()
    plt.title('Learning Curve')
    plt.xlabel('New Cases')
    plt.ylabel('Accuracy')
    plt.plot(x1)
    plt.plot(x2, 'r')
    plt.legend(['Matches History Similarity', 'Betting odds Similarity'])
    plt.show()
    plt.savefig(name)


def test(orig_data, test_matches, n, weighting_method, params):
    m, thr1, thr2, thr3 = params
    matches_data = copy.deepcopy(orig_data)
    i = 0
    lc = []
    for match in test_matches.get_case_values():
        conf, _ = main_CBR(actual_match=match,
                           matches=matches_data,
                           max_matches=m,
                           retrieve_thr=thr1,
                           conf_thr=thr2,
                           sim_thr=thr3,
                           weighting_method=weighting_method)
        i += int(conf)
        lc.append(i)
    acc = i*(100/float(n))
    return acc, lc


def run_validation():
    """
    Loads the data from the Train and run the CBR for different parameters
    validating them and finally prints the best ones. It also creates an output
    files with the learning curve and the best parameters.
    :return:
    """
    # Load the data
    print 'Loading data ...'
    orig_data = get_matches(input='load_from_pkl')
    print 'Start CBR ...'
    # if the main is called manually, this if/else-branch will be executed:
    # create a 'mock' match object with minimum information required and run the cbr for the given fixture

    # Read from CSV file
    test_matches = MatchesCaseBase()
    read_match_dataset('../../data/Test/LaLiga2013-14.csv', test_matches)
    # read_match_dataset('../../data/Test/ultimaJornada.csv', test_matches)

    n = len(test_matches.get_case_values())

    # Create grid of parameters
    max_m = range(3, 13)
    r1_threshold = np.array(range(1, 10))/10.0
    conf_threshold = 0.5
    sim_threshold = 1

    params = []
    for m in max_m:
        for thr1 in r1_threshold:
            params.append([m, thr1, conf_threshold, sim_threshold])

    lc_plot = []
    for j in [2, 3]:
        print 'Similarity Function %i' % j
        r = Parallel(n_jobs=num_cpu, verbose=3)(delayed(test)(orig_data, test_matches, n, j, params[i]) for i in range(len(params)))
        acc, lc = zip(*r)

        best_acc = max(acc)
        idx = acc.index(best_acc)
        best_param = params[idx]
        best_lc = lc[idx]
        lc_plot.append(best_lc)

        print '\n--------- BEST PARAMETERS -----------'
        print best_param
        print '\n--------- BEST ACCURACY -----------'
        print best_acc
        print '\n--------- BEST LEARNING CURVE -----------'
        print best_lc

        f = open('../../data/Results/validation_results_sim' + str(j) + '.csv', 'w')
        f.write('# Best Accuracy\n%f\n' % best_acc)

        f.write('# Learning Curve\n')
        for i in best_lc:
            f.write(str(i) + ',')

        f.write('\n# Best Parameters (max_matches, retreave_threshold, confidence_threshold, similarity_threshold)\n')
        for i in best_param:
            f.write(str(i) + ',')
        f.close()

    plot_lc(lc_plot, '../../data/Results/learning_curve.png')

if __name__ == '__main__':
    run_validation()