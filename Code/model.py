
class CBRclass():
    """
    The class Case defines in a general way the cases of the CBR.

    """
    def __init__(self, name):
        self.attributes = {}
        self.name = name
        pass

    def add_class(self, name):
        pass

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
            raise NameError('The attribute {0} already exists, to update its values use set_feature.'.format(name))

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
                raise NameError('The attribute {0} is type {1} not {2}.'.format(name,
                                                                                type(self.attributes[name]),
                                                                                type(values)))
            self.attributes[name] = values
        else:
            raise NameError('The attribute {0} doesn\'t exists, to add a new attribute use add_feature.'.format(name))


if __name__=='__main__':
    # Test

    team1 = CBRclass(name='Messi')

    team1.add_feature(name='Skills', values=[1, 2, 3, 4])
    team1.add_feature(name='Skills', values=[4, 3, 2, 1])
    team1.set_feature(name='Skills', values={'A': 4})