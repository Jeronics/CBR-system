import numpy as np

from cbr.core.internal_repr.model import CaseBase, Case


def retrieve(casebase, case, similarity_function, thr, max_cases, **kwargs):
    """
    This function will retrieve the most similar cases
    stored in the 'casebase' to the 'case'.

    :type  casebase: CaseBase
    :param casebase: CaseBase storing Cases with its solutions.

    :type  case: Case
    :param case: New case to your CBR, with an unknown solution.

    :type  similarity_function: callable
    :param similarity_function: Similarity function which takes as an argument
                two cases and returns a float number between 0 and 1.
                Where 0 means the two cases are dissimilar and
                1 means that the two cases are equal or vary
                similar.

    :type  thr: float
    :param thr: Threshold to determine weather a given similarity
                is considered as a possible retrievable case.

    :type  max_cases: int
    :param max_cases: Maximum number of similar cases to be retrieved.
    
    :param kwargs: Optional parameters for the similarity function

    :return: List of similar cases.
    """
    if hasattr(similarity_function, '__call__'):
        similar_cases = []
        similarities = []
        for c in casebase.get_case_values():
            similarity = similarity_function(c, case, **kwargs)
            if similarity > thr:
                if len(similar_cases) < max_cases:
                    similar_cases.append(c)
                    similarities.append(similarity)
                elif similarity > similarity_function(similar_cases[-1], case):
                    similar_cases[-1] = c
                    similarities[-1] = similarity
                similar_cases.sort(key=lambda x: similarity_function(x, case), reverse=True)
                similarities.sort(reverse=True)

        return similar_cases, similarities
    else:
        raise NameError('The argument "sim" should be callable.')


def null_adapatation(new_case, retrieved_cases, similarities, specific_function):
    """
    This is an adaptation function to a sub-case of the adaptational substitution.
    It returns the solution of the most similar case. Null adaptation.

    :type new_case: Case (Unused)
    :param new_case: New case to solve (Unused)

    :type retrieved_cases: List of Case Objects
    :param retrieved_cases:

    :type similarities: List of floats
    :param similarities: list of similarities between elements in retrieved_cases and the new case.

    :type specific_function: Function Object
    :param specific_function: (Unused)

    :type: Solution Object
    :return: solution object in the most similar case.
    """
    return retrieved_cases[np.argmax(similarities)].get_solution()


def substitutional_adaptation(new_case, retrieved_cases, similarities, specific_function):
    """
    This function is a domain specific substitutional_adaptation which using a specific domain function returns a new
    solution.

    :type new_case: Case
    :param new_case: New case to solve

    :type retrieved_cases: List of Case
    :param retrieved_cases:

    :type similarities: List of floats
    :param similarities: list of similarities between elements in retrieved_cases and the new case.

    :type specific_function: Function Object - must have as inputs: (new_case, retrieved_cases, similarities)
    :param specific_function: Specific function that determines the domain specific substitutional adaptation.

    :type: Solution Object
    :return: solution object returned by the specific function
    """
    new_solution = specific_function(new_case, retrieved_cases, similarities)
    return new_solution


def structural_adaptation(new_case, retrieved_cases, similarities, specific_function):
    """
    This function is a generic structural adaptation which when using a specific domain function returns a new
    solution.

    :type new_case: Case
    :param new_case: New case to solve

    :type retrieved_cases: List of Case
    :param retrieved_cases:

    :type similarities: List of floats
    :param similarities: list of similarities between elements in retrieved_cases and the new case.

    :type specific_function: Function Object
            - must have as inputs: (new_case, retrieved_cases, similarities)
            - output: modifier: operation which modifies the structure of the solution and the solution Object to change
    :param specific_function: Specific function that determines the domain specific substitutional adaptation.

    :type: Solution Object
    :return: solution object returned by the specific function
    """
    # structural changes in solution
    modifier, solution_to_change = specific_function(new_case, retrieved_cases, similarities)

    return modifier(solution_to_change)


def generative_adaptation(new_case, retrieved_cases, similarities, specific_function):
    """

    This is an adaptation function that acts as a gereric function of the generative substitution. It generates an
    operation based on the retrieved cases to obtain a solution.

    :type new_case: Case
    :param new_case: New case to solve

    :type retrieved_cases: List of Case
    :param retrieved_cases:

    :type similarities: List of floats
    :param similarities: list of similarities between elements in retrieved_cases and the new case.

    :type specific_function: Function Object - inputs: (new_case, retrieved_cases, similarities)
                                             - output: Operation function which returns the solution from the new case.

    :param specific_function: Specific function that determines the domain specific substitutional adaptation.

    :type: Solution Object
    :return: solution object returned by the specific function
    """
    # return the operation that returns the solution given a problem
    operation = specific_function(retrieved_cases, similarities, specific_function)

    # Apply the operation on the problem of the new_case
    return operation(new_case)


def reuse(similar_cases, new_case, similarities, adaptation_function, specific_function):
    """
    In the Reuse Phase we will observe the retrieved solutions and we will try to adapt them to our new case with
    the implementation of an heuristic.

    :type  similar_cases: list of Case
    :param similar_cases: Array of cases similar to the new case.

    :type  new_case: Case
    :param new_case: New case to solve

    :type  similarities: list of float
    :param similarities: Vector with the similarity values of the similar cases.

    :type  adaptation_function: callable
    :param adaptation_function: General adaption technique used

    :type  specific_function: callable
    :param specific_function: Specific problem-dependent function

    :type: String
    :return: result of the case
    """
    if hasattr(adaptation_function, '__call__'):
        if hasattr(specific_function, '__call__'):
            return adaptation_function(new_case, similar_cases, similarities, specific_function)
        else:
            raise NameError(
                'The "specific_function" must be a callable object not a {0}.'.format(type(specific_function)))
    else:
        raise NameError('The "method! must be a callable object not a {0}'.format(type(adaptation_function)))


def revise(case, expert_function, predicted_result):
    """
    In the Revise Phase, a proposed solution for a given case is evaluated
    and a confidence probability is returned.

    :type  case: Case
    :param case: It is a Case with a proposed solution by the Reuse Phase.

    :type  expert_function: callable
    :param expert_function: A callable function which evaluates the proposed solution,
                   this 'expert' could be a real expert, a simulation or a
                   real world Test. The function should a return a list with
                   the first element being a confidence measure and the second
                   element an improved solution if there is.

    :type: Tuple list of confidence and case object
    :return: confidence measure of the proposed solution to be positive.
    """
    if hasattr(expert_function, '__call__'):
        v = expert_function(case, predicted_result)
        confidence = v[0]
        if len(v) > 1:
            improved_sol = v[1]
            case.set_solution(improved_sol)

        return [confidence, case]
    else:
        raise NameError('The argument "expert" should be callable object not a {0}.'.format(type(expert_function)))


def retain(case, casebase, confidence, conf_thr, retrieved_sim, sim_thr):
    """
    In the Retain Phase, the proposed solution will be considered to be saved
    in the repository of the case base or not.

    :type  case: Case
    :param case: It is a case with the proposed solution to be saved or not
                 in the retain phase.

    :type  casebase: CaseBase
    :param casebase: CaseBase storing Cases with its solutions.

    :type  confidence: float
    :param confidence: Confidence given by the Revise Phase.

    :type  conf_thr: float
    :param conf_thr: Threshold to chose whether to add a case to the case library
                     given a certain confidence.

    :type  retrieved_sim: list of float
    :param retrieved_sim: List of similarities given by the Retrieve Phase.

    :type  sim_thr: float
    :param sim_thr: Threshold to chose whether two cases are similar.

    :return: CaseBase
    """
    if confidence > conf_thr:
        if retrieved_sim:
            if max(retrieved_sim) < sim_thr:
                casebase.add_case(case)
        else:
            casebase.add_case(case)

    return casebase
