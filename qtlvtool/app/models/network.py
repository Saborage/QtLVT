from anytree.walker import Walker
import numpy as np


class Network:
    # CONSTRUCTOR
    def __init__(self, vnl=230.):
        """
        A Network is defined here by its Voltage at Slack Node (called 'Voltage No Load').
        :param vnl: A double that will determine the initial value of the network's voltages. Default vnl=230.
        """
        self.__brackets = []
        self.__voltage_no_load = vnl

    # GETTERS/ACCESSORS
    def get_brackets(self):
        """
        This method will call the superclass method "treelib.tree.Tree.nodes()"
        :return: self.nodes(), a dictionnary of the form {id: node_instance}
        """
        return self.__brackets

    def get_branches(self):
        """
        This method will iterate over ALL the brackets in the network, and will retrieve every branch on it.
        :return: branches, a list of all branches in this network
        """
        branches = []
        for bracket in self.__brackets:
            branches.append(bracket.get_branch())
        return branches

    def get_voltage_no_load(self):
        """
        This is used to get the value of the Voltage on the slack node
        :return: self.__voltage_no_load
        """
        return self.__voltage_no_load

    def get_slack_node(self):
        """
        :return: The first item of the list of brackets which corresponds to the slack node.
        """
        return self.__brackets[0].get_node()
    # END

    # SETTERS/ACCESSORS
    def set_voltage_no_load(self, vnl):
        """
        This method receives a new VNL that will replace the value of the ancient one.
        :param vnl: the double corresponding to the value we want to set voltage_no_load.
        :return: None
        """
        self.__voltage_no_load = vnl
    # END

    # CRUD
#######################################################################################################################
    # Brackets
    def add_bracket(self, bracket):
        """
         This method will check if the given node to add is already in the network. If not, it will add it.
        Otherwise it will do nothing.
        :param bracket: the bracket to add to the network.
        :return: self
        """
        if bracket not in self.__brackets:
            self.__brackets.append(bracket)
        return self

    def delete_bracket(self, nid):
        """
        This method will delete a bracket from the network. First it checks if the network contains the id,
        then whether it is a leaf or not.
        If it is, it will simply remove it from the network.
        If it isn't, it will remove it AND link its children to its parent.
        :param nid: ID of the node to delete
        :return: self
        """
        if 0 < nid < len(self.__brackets):
            del self.__brackets[nid]
        return self

    def research_bracket(self, nid):
        """
        Will search the Network after a bracket.
        :param nid: the bracket's id we have to find
        :return: The nidth item in the network's list of brackets
        """
        # return self.get_node(nid)
        return self.__brackets[nid]

    # Updates a bracket
    def update_bracket(self, bid, bracket):
        """
        Replaces the bracket at the given id by the other one given in argument
        :param bid: index of the bracket to replace
        :param bracket: bracket updated
        :return: The updated bracket.
        """
        self.get_brackets()[bid] = bracket
        return self.get_brackets()[bid]
#######################################################################################################################
    # END

    # TREE METHODS

    def set_parent_of_bracket(self, bracket, pid):
        """
        :param bracket: the bracket we want to link to the one corresponding to pid
        :param pid: the ID of the parent we want to link to the bracket
        :return: None
        """
        parent = self.__brackets[pid].get_node()
        bracket.get_node().set_parent(parent)

    @staticmethod
    def next_sibling(node):
        """
        static method that receives a node. It will just check if the node's parent has other children.
        :param node: the node we were traversing the tree from
        :return: index +1 if there are other children, instead returns None if IndexError or AttributeError
        """
        try:
            i = node.get_parent().child_nodes.index(node)
            return node.get_parent().get_children()[i+1]
        except(IndexError, AttributeError):
            return None

    def find_path(self, srcid, dstid):
        """
        method that receives a source node and a destination one. It will check if two nodes are directly
        connected.
        :param srcid: the node's id from which we will start to iterate
        :param dstid: the node's id we want to know if it's connected to source.
        :return: path: the list of nodes that will lead from source to dest.
        """
        source = self.find_node(srcid + 2)
        dest = self.find_node(dstid + 2)
        if source is dest:
            return [source.get_id()]
        w = Walker()
        walk_path = w.walk(source, dest)
        up = walk_path[0]
        common = walk_path[1]
        down = walk_path[2]
        uplist = [e for e in up]
        downlist = [e for e in down]
        uplist.append(common)
        uplist.extend(down)
        path = [source.get_id()]
        for node in uplist:
            path.append(node.get_id())
        return path
#######################################################################################################################
    # END

    # OTHER METHODS
    def get_nb_brackets(self):
        """
        :return: the size of the brackets list.
        """
        return len(self.__brackets)

    def find_node(self, nid):
        """
        :param nid: the index of the node we want to find
        :return: node of the bracket at given node_ID
        """
        for bracket in self.__brackets:
            if bracket.get_node().get_id() == nid:
                return bracket.get_node()

    def get_slack_voltage(self):
        """
        This will modelises the network's Vnl matrix.
        :return: slack_voltage, a 19 by 3 matrix corresponding to the voltages on each slack node's phases.
        """
        first_val = self.__voltage_no_load
        second_val = self.__voltage_no_load * np.exp(-2j * np.pi/3)
        third_val = self.__voltage_no_load * np.exp(2j * np.pi/3)
        matrix = np.array(([first_val], [second_val], [third_val]), dtype=np.complex128)
        slack_voltage = np.tile(matrix, (self.get_nb_brackets()-1, 1))
        return slack_voltage

    def __str__(self):
        string = "Network{\n"
        for bracket in self.__brackets:
            string += "\t" + "Bracket" + "[ " + bracket.__str__()+"]\n"
        string += "}"
        return string


if __name__ == '__main__':
    pass
