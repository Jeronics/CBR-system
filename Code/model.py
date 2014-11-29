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

    def add_class(self, name, **kwargs):
        """
        Adds a class to the classes dictionary.

        :param name: name of the class
        :type  name: str
        :param kwargs: optional attributes ('attributes' or classes)
        """
        self.classes[name] = CBRclass(name=name, **kwargs)

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

    def set_solution(self, solution):
        """
        :param solution: solution of the case.
        :type  solution: str
        """
        self.solution = solution

    def set_problem(self, problem):
        """
        :param problem: CBRclass containing the description of the problem.
        :type  problem: CBRclass
        """
        if type(problem) is CBRclass:
            self.problem = problem
        else:
            raise NameError("The problem must be an instance of CBRclass object.")

if __name__ == '__main__':
    # ----------
    # -- Test --
    # ----------

    player1 = CBRclass(name='Messi')
    player1.add_feature(name='Skills', values={'speed': 4})

    team1 = CBRclass(name='FCB', **{'Messi': player1})
    team1.add_feature(name='members', values=100000)

    print team1.name
    print team1.classes
    print team1.attributes

    print player1.name
    print team1.classes[player1.name].attributes