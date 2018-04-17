

class NetworkUser:

    # CONSTRUCTOR
    def __init__(self, phases=None, P=None, Q=None):
        """
        A user is defined by the phases aat which it is linked, the Power that it consumes(positive)/reinjects(negative)
        and the Q.
        :param phases: list of 4 boolean. 1 = The User is on the phase ; 0 = The User doesn't use the phase: [1,1,1,0]
        means a user using ALL phases (The fourth index corresponds to the neutral phase)
        :param P: a double corresponding to the Power the client consumes (if positive) or reinjects on the network
        (if negative)
        :param Q: Yes.
        """
        self.__phases_required = phases
        self.__P = P
        self.__Q = Q

    # GETTERS/ACCESSORS
    def get_phases_required(self):
        """
        :return: the list of phases the user is linked to
        """
        return self.__phases_required

    def get_P(self):
        """
        :return: the power corresponding to the user.
        """
        return self.__P

    def get_Q(self):
        """
        :return: Q.
        """
        return self.__Q
    # END

    # SETTERS/MUTATORS
    def set_phases_required(self, phases):
        """
        :param phases: the new phases on which the user's linked.
        :return:
        """
        self.__phases_required = phases

    def set_P(self, p):
        """
        :param p: the new power that comes from the user
        :return:
        """
        self.__P = p

    def set_Q(self, q):
        """
        :param q: the Q.
        :return:
        """
        self.__Q = q


if __name__ == '__main__':
    pass
