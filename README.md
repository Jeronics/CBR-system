CBR Bet Assistant
(this a GitHub readme file)
==========

Task List
---------
- [x] **Data Structure**
- [x] **Read fast the data**
- [x] **Retrieve**
 - [x] Create abstract Retrieve.
 - [x] Adapt the abstract case to our problem.
- [x] **Reuse**
 - [x] Create abstract Reuse.
 - [x] Adapt the abstract case to our problem.
- [x] **Revise**
 - [x] Create abstract Revise.
 - [x] Adapt the abstract case to our problem.
- [x] **Retain**
 - [x] Create abstract Retain.
 - [x] Adapt the abstract case to our problem.


Deadlines
----------

- 19/01/2015 Delivery 2: Project Documentation and software code.

- 22/01/2015 Delivery 3: Project work presentation and public exposition.

Global Goals
------------

OPTIMAL CBR SYSTEM (Case base maintenance especially affects space and time)

- 1.  Maximum Competence: to maximize the # of target problems it can satisfactorily solve
- 2.  Optimal Efficiency:
 - a)  Time: minimize time
 - b)  Space: Smaller CL

0. Data
-------
   - We have csv-s of first and second division of Spain from 1996/97 til now. And lots of additional information.
                        http://www.football-data.co.uk/spainm.php

   - Here we have history of 'quinielas': http://www.resultados-futbol.com/quiniela/historico/18
   
   - Here we have the statistics of the 2014-15: http://www.lfp.es/estadisticas/liga-bbva/goles/
   
   - Here we can get everything: http://www.marca.com/estadisticas/futbol/primera/2010_11/

1. Data Structure
-----------------
The data structure is largely defined by the three classes:

### CBRclass:
Is an abstraction of an object class, which can contain other instances of CBRclass 
in a dictionary of classes and can also contain other data structures in the attributes 
dictionary.

```python
class CBRclass(object):
    """
    The class CBRclass defines in a general way the cases of the CBR.

    """
    def __init__(self, name, **kwargs):
```

| Method | Description |
| ------ | ----------- |
| ```add_class``` | Adds a class to the classes dictionary. |
| ```get_class``` | Gets a class from the classes dictionary. |
| ```pop_class``` | Removes the class 'name' from the dictionary of classes and returns it. |
| ```add_feature``` | These method adds a new attribute to the CBRclass. |
| ```get_feature``` | These method sets the values of an attribute from the CBRclass. |
| ```pop_feature``` | Removes and returns the element 'name' from the dictionary of attributes. |

### Case:
The Case class is a subclass of the CBRclass with an attribute called solution and a CBRclass
called problem. This class is the base of our CBR system.

```python
class Case(object):
    """
    Case is the main class in the CBR.
    Contains a problem (CBRclass) and a solution (default empty string).
    """
    def __init__(self, name, problem, **kwargs):
```

| Method | Description |
| ------ | ----------- |
| ```get_solution``` | Returns the solution of the case. |
| ```set_solution``` | Sets the current solution to a given one. |
| ```get_problem``` | Gets the problem of the case. |
| ```set_problem``` | Set the problem of the case to a given problem. |


### CaseBase:
This class contains basically a dictionary with all the cases in our Case Base. 

```python
class CaseBase(object):
    """
    Repository of Cases a the CBR.
    """
    def __init__(self):
```

| Method | Description |
| ------ | ----------- |
| ```add_case``` | Add a new case to de Case Base. |
| ```pop_case``` | Pops a case from the CaseBase. |
| ```get_case_keys``` | Returns the keys of the cases dictionary. |
| ```get_case_values``` | Return the values of the cases dictionary. |
| ```get_case``` | Gets a case from the Case Base given a value or a key of the cases dictionary. |

2. Retrieve
-----------

The Retrieve phase is performed in the function retrieve from the ```internal_repr``` module.
It is defined as follows:

```python
def retrieve(casebase, case, similarity_function, thr, max_cases):
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

    :return: List of similar cases.
    """
```


3. Reuse
--------

In the Reuse phase some adaptation methods where implemented:

```python
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
```
 
```python
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
```

```python
def transformational_adaptation(new_case, retrieved_cases, similarities, specific_function):
    """
    This function is a domain specific transformational adaptation which using a specific domain function returns a new
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
```

```python
def generative_adaptation(new_case, retrieved_cases, similarities, specific_function):
    """
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
```

The Reuse function (phase) will try to adapt the retrieved solutions to the new case.

```python
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
```
4. Revise
---------

In the Revise Phase, a proposed solution for a given case is evaluated and a confidence probability is returned.
    
```python
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
```
5. Retain
---------

In the Retain Phase, the proposed solution will be considered to be saved in the repository of the case base or not.
    
```python
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

    :return: Boolean
    """
```