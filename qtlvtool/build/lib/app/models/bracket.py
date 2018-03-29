class Bracket:
    def __init__(self, node=None, branch=None):
        """
        a Bracket is the association between a Node object and a Branch object.
        Thus, a Bracket will just contain a Node attribute and a Branch one
        :param node: the node contained by the bracket
        :param branch: the branch we want to link with the node
        """
        super(Bracket, self).__init__()
        self.__node = node
        self.__branch = branch

    # ACCESSORS: GETTERS
    def get_node(self):
        """
        :return: the node of the bracket.
        """
        return self.__node

    def get_branch(self):
        """
        :return: the branch of the bracket.
        """
        return self.__branch
    # END ACCESSORS
    # #################################################################################################################

    # MUTATORS: SETTERS
    def set_node(self, node):
        """
        :param node: the new NetworkNode we want this bracket to contain.
        :return:
        """
        self.__node = node

    def set_branch(self, branch):
        """
        :param branch: the new NetworkBranch we want this bracket to contain.
        :return:
        """
        self.__branch = branch
    # END MUTATORS
    # #################################################################################################################

    # OTHER METHODS
    # To String method
    def __str__(self):
        return self.__node.__str__()


if __name__ == '__main__':
    pass
