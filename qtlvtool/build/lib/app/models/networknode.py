from anytree import NodeMixin


class NetworkNode(NodeMixin):
    # CONSTRUCTOR
    def __init__(self, identifier=0, parent=None, users=None, voltage_min=0, voltage_max=0):
        """
        A Node is defined by its ID, its Parent, the Users related to it, its minimum and maximum Voltage.
        It also has a parent_ID, for more ease-of-use.
        :param identifier:
        :param parent:
        :param users:
        :param voltage_min:
        :param voltage_max:
        """
        super(NetworkNode, self).__init__()
        if users is None:
            self.__users = []
        else:
            self.__users = users
        self.__voltage_min = voltage_min
        self.__voltage_max = voltage_max
        self.__identifier = identifier
        self.parent = parent
        if parent is not None:
            self.__parent_id = parent.__identifier
        else:
            self.__parent_id = 0
        self.name = "Node" + str(identifier)

    # GETTERS/ACCESSORS
    def get_id(self):
        """
        Gets the ID of a network_node.
        :return: identifier, an integer telling the ID of the node.
        """
        return self.__identifier

    def get_parent(self):
        """
        :return: The parent's node of the current one.
        """
        return self.parent

    def get_users(self):
        """
        :return: A list containing all the users that are linked to the current node.
        """
        return self.__users

    def get_voltage_min(self):
        """
        :return: The value of the current node's minimum voltage.
        """
        return self.__voltage_min

    def get_voltage_max(self):
        """
        :return: The value of the current node's maximum voltage.
        """
        return self.__voltage_max

    def get_children(self):
        """
        :return: A list containing all of the node's children.
        """
        return self.children

    def get_parent_id(self):
        """
        :return: An integer corresponding to the ID of the parent.
        """
        return self.__parent_id

    # SETTERS/MUTATORS
    def set_id(self, iden):
        """
        :param iden: an integer corresponding to the ID we want to give to the node.
        :return: None.
        """
        self.__identifier = iden
        self.name = "Node" + str(self.__identifier)

    def set_parent(self, parent):
        """
        :param parent: The node that has to be the parent of the current one
        :return: None
        """
        self.parent = parent

    def set_parent_id(self, pid):
        """
        :param pid: the id of the node we want to set as parent.
        :return: None.
        """
        self.__parent_id = pid

    def set_users(self, users):
        """
        :param users: A list corresponding to the users linked to this node.
        :return: None.
        """
        self.__users = users

    def set_voltage_min(self, vmin):
        """
        :param vmin: A double that will be the new value of minimum voltage for this node.
        :return: None.
        """
        self.__voltage_min = vmin

    def set_voltage_max(self, vmax):
        """
        :param vmax: A double that will be the new value of maximum voltage for this node.
        :return:
        """
        self.__voltage_max = vmax

    # OTHER METHODS
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return True if self.__identifier == other.__identifier else False


if __name__ == '__main__':
    pass
