class CBRclass(object):
    """
    The class CBRclass defines in a general way the cases of the CBR.

    """

    def __init__(self, name, **kwargs):
        self.attributes = {}
        self.classes = {}
        self.name = name

        for kw in kwargs.keys():
            if type(kwargs[kw]) is CBRclass:
                self.classes[kw] = kwargs[kw]
            else:
                self.attributes[kw] = kwargs[kw]

    def add_class(self, name, *args, **kwargs):
        """
        Adds a class to the classes dictionary.

        :param name: name of the class in the dictionary of classes.
        :type  name: str
        :param kwargs: optional attributes ('attributes' or classes)
        :param args: optional inside name of the inner-class
        """
        inname = args[0] if args else name
        self.classes[name] = CBRclass(name=inname, **kwargs)

    def get_class(self, name):
        """
        Gets a class from the classes dictionary.

        :param name: name of the class
        :type  name: str
        :return CBRclass
        """
        return self.classes[name]

    def pop_class(self, name):
        """
        Removes the class 'name' from the dictionary of classes and returns it.
        :param name: name of the class to pop
        :type  name: str
        :return: class popped
        """
        return self.classes.pop(name)

    def add_feature(self, name, values):
        """
        These method adds a new attribute to the CBRclass.

        :param name: name of the new attribute.
        :type  name: str
        :param values: list of features if is flat or dictionary if is hierarchical.
        :type  values: int | list of int | float | lost of float | dict
        """
        if name not in self.attributes:
            self.attributes[name] = values
        else:
            raise NameError("The attribute '{0}' already exists, to update its values use set_feature.".format(name))

    def get_feature(self, name):
        """
        Gets a feature from the attributes dictionary.

        :param name: name of the class
        :type  name: str
        :return int | list of int | float | list of float | dict
        """
        return self.attributes[name]

    def set_feature(self, name, values):
        """
        These method sets the values of an attribute from the CBRclass.

        :param name: name of the attribute to update.
        :type  name: str
        :param values: list of features if is flat or dictionary if is hierarchical.
        :type  values: int | list of int | float | lost of float | dict
        """
        if name in self.attributes:
            if not type(self.attributes[name]) is type(values):
                raise NameError("The attribute '{0}' is type {1} not {2}.".format(name,
                                                                                  type(self.attributes[name]),
                                                                                  type(values)))
            self.attributes[name] = values
        else:
            raise NameError("The attribute '{0}' doesn't exists, to add a new attribute use add_feature.".format(name))

    def pop_feature(self, name):
        """
        Removes and returns the element 'name' from the dictionary of attributes.
        :param name: 'name' of the attribute to pop
        :return: popped element from the dictionary of attributes
        """
        return self.attributes.pop(name)

    def __str__(self):
        return "CBRclass " + self.name + ": Attr=" + str(self.attributes) + " | Classes=" + str(self.classes)


class Case(object):
    """
    Case is the main class in the CBR.
    Contains a problem (CBRclass) and a solution (default empty string).
    """
    def __init__(self, name, problem, **kwargs):
        assert type(name) is str, 'The name of the Case must be a string.'
        self.name = name

        if type(problem) is CBRclass:
            self.problem = problem
        else:
            raise NameError("The problem must be an instance of CBRclass object.")

        self.solution = kwargs['solution'] if 'solution' in kwargs else ''

    def get_solution(self):
        return self.solution

    def set_solution(self, solution):
        """
        :param solution: solution of the case.
        :type  solution: str
        """
        self.solution = solution

    def get_problem(self):
        return self.problem

    def set_problem(self, problem):
        """
        :param problem: CBRclass containing the description of the problem.
        :type  problem: CBRclass
        """
        if type(problem) is CBRclass:
            self.problem = problem
        else:
            raise NameError("The problem must be an instance of CBRclass object.")

    def __str__(self):
        return "Case " + self.name + ":\n\t-Problem: " + str(self.problem) + "\n\t-Solution: " + self.solution


class CaseBase(object):
    """
    Repository of Cases a the CBR.
    """
    def __init__(self):
        self.cases = {}

    def add_case(self, case):
        if type(case) is Case or issubclass(type(case), Case):
            self.cases[case.name] = case
        else:
            raise NameError("The case must be an instance of Case object.")

    def pop_case(self, case):
        self.cases.pop(case.name)

    def get_case_keys(self):
        return self.cases.keys()

    def get_case_values(self):
        return self.cases.values()

    def get_case(self, case):
        if case in self.cases.keys():
            return self.cases[case]
        elif case in self.cases.values():
            return self.cases[case.name]
        else:
            if type(case) is Case:
                raise NameError("The case is not stored in the CaseBase")
            else:
                raise NameError("The case must be an instance of Case object.")


if __name__ == '__main__':
    # ----------
    # -- test --
    # ----------

    player1 = CBRclass(name='Messi')
    player1.add_feature(name='Skills', values={'speed': 4})

    team1 = CBRclass(name='FCB', **{'Messi': player1})
    team1.add_feature(name='members', values=100000)

    team2 = CBRclass(name='RMD')

    match1 = CBRclass(name='2014-15.j2.FBC-RMD', **{'FCB': team1, 'RMD': team2})
    result = '1'
    case1 = Case(name='2014-15.j2.FBC-RMD', problem=match1, **{'solution': result})

    print team1.name
    print team1.classes
    print team1.attributes

    print player1.name
    print team1.classes[player1.name].attributes

    print case1