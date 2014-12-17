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


def main(actualMatch):

    # 1-. LOAD DATA

    dataset = '../data/Train/train.jpkl'
    matches = w.read_case_base(dataset)

    # 2-. RETRIEVE SIMILAR MATCHES

    # Grade of similarity:
    #   When grade higher less similarity.
    #   e.g:
    #         grade = 1  --> highest similarity, return only matches of local as local.
    #         grade = 2  --> less similarity, return matches of locals as local and foreign.
    threshold = 0.01
    max_matches = 10
    retrieved_matches, similarities = cbr.retrieve(matches, actualMatch, w.similarity, threshold, max_matches)

    print len(retrieved_matches)
    print 'home '+actualMatch.get_home() + '  away '+actualMatch.get_away()

    print similarities
    # for match in retrieved_matches:
        # print str(match.name) + ' | sim: ' + str(w.similarity(match, actualMatch))


    # TODO 5-. REUSE
    # REUSE the information retrieved from the archieves and predict a result and a score

    predicted_result = cbr.reuse(retrieved_matches, actualMatch, similarities)
    print "predicted result = " + predicted_result
    print "real result = " + actualMatch.get_solution()

    # TODO 6-. REVISE
    actualMatch.get_solution()

    solution = cbr.revise(actualMatch, w.expert, predicted_result)

    # TODO 7-. RETAIN

    saved = cbr.retain(actualMatch, solution, matches, w.save_case_base, filename='../data/Train/train.jpkl')

    print 'saved in cbr new case = ' + str(saved)


if __name__ == '__main__':

    test_matches = w.read_case_base('../data/Test/test.jpkl')

    for match in test_matches.get_case_values():
        main(match)
        break