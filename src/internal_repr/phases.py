from model import CaseBase, Case


def retrieve(casebase, case, sim, thr, max_cases):
    """
    This function will retrieve the most similar cases
    stored in the 'casebase' to the 'case'.

    :type  casebase: CaseBase
    :param casebase: CaseBase storing Cases with its solutions.

    :type  case: Case
    :param case: New case to your CBR, with an unknown solution.

    :type  sim: callable
    :param sim: Similarity function which takes as an argument
                two cases and returns an float between 0 and 1.
                Where 0 means the two cases are dissimilar and
                1 means that the two cases are equal or vary
                similar.

    :type  thr: float
    :param thr: Threshold to determine weather a given similarity
                is considered as a possible retrievable case.

    :type  max_cases: int
    :param max_cases: Maximum number of similar cases to be retrieved.

    :return: List of similar cases.
    """
    similar_cases = []
    for c in casebase.get_case_values():
        similarity = sim(c, case)
        if similarity > thr:
            if len(similar_cases) < max_cases:
                similar_cases.append(c)
                similar_cases.sort(key=lambda x: sim(x, case))
            elif similarity > sim(similar_cases[-1], case):
                similar_cases[-1] = case
                similar_cases.sort(key=lambda x: sim(x, case))

    return similar_cases