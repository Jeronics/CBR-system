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
    if hasattr(sim, '__call__'):
        similar_cases = []
        similarities = []
        for c in casebase.get_case_values():
            similarity = sim(c, case)
            if similarity > thr:
                if len(similar_cases) < max_cases:
                    similar_cases.append(c)
                    similarities.append(similarity)
                    similar_cases.sort(key=lambda x: sim(x, case), reverse=True)
                    similarities.sort(reverse=True)
                elif similarity > sim(similar_cases[-1], case):
                    similar_cases[-1] = case
                    similarities[-1] = similarity
                    similar_cases.sort(key=lambda x: sim(x, case), reverse=True)
                    similarities.sort(reverse=True)

        return similar_cases, similarities
    else:
        raise NameError('The argument "sim" should be callable.')


def reuse(matches):


    pass


def revise(case, expert):
    """
    In the Revise Phase, a proposed solution for a given case is evaluated
    and a confidence probability is returned.

    :type  case: Case
    :param case: It is a Case with a proposed solution by the Reuse Phase.

    :type  expert: callable
    :param expert: A callable function which evaluates the proposed solution,
                   this 'expert' could be a real expert, a simulation or a
                   real world Test. The function should a return a list with
                   the first element being a confidence measure and the second
                   element an improved solution if there is.

    :return: confidence measure of the proposed solution to be positive.
    """
    if hasattr(expert, '__call__'):
        v = expert(case)
        confidence = v[0]
        if len(v) > 1:
            improved_sol = v[1]
            case.set_solution(improved_sol)

        return [confidence, case]
    else:
        raise NameError('The argument "expert" should be callable.')


def retain():
    pass