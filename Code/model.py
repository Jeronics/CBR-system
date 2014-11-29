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
            elif type(kwargs[kw]) is list or type(kwargs[kw]) is dict:
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
        :type  values: list of int or dict
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
        :type  values: list of int or dict
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


class Case(CBRclass):
    """
    Case is a subclass of the CBRclass class.
    """
    pass


if __name__ == '__main__':
    # ----------
    # -- Test --
    # ----------

    player1 = CBRclass(name='Messi')

    # player1.add_feature(name='Skills', values=[1, 2, 3, 4])
    # player1.add_feature(name='Skills', values=[4, 3, 2, 1])
    # player1.set_feature(name='Skills', values={'A': 4})

    team1 = CBRclass(name='FCB', **{'Messi': player1})
    print team1
    print team1.classes
    print team1.attributes