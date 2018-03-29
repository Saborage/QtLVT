class NetworkBranch:
    # CONSTRUCTOR
    def __init__(self, phases=None, r=None, x=None, length=None, Imax=None):
        """
        A branch has an R, an X, a list of Phases (len: 4), a maximum Intensity and a length.
        :param phases:
        :param r:
        :param x:
        :param length:
        :param Imax:
        """
        if phases is None:
            self.__phases = [1, 1, 1, 0]
        else:
            self.__phases = phases
        self.__R = r
        self.__X = x
        self.__length = length
        self.__Imax = Imax

    # GETTERS/ACCESSORS
    def get_phases(self):
        """
        :return: the phases that are on the branch.
        """
        return self.__phases

    def get_R(self):
        """
        :return: R: a list containing each resistance depending on the phase.
        """
        return self.__R

    def get_X(self):
        """
        :return: X: a list containing each reactance depending on the phase.
        """
        return self.__X

    def get_length(self):
        """
        :return: length: the length of the branch
        """
        return self.__length

    def get_Imax(self):
        """
        :return: Imax: the maximum Intensity that the branch can support.
        """
        return self.__Imax

    # SETTERS/MUTATORS
    def set_phases(self, pob):
        """
        :param pob: a list of boolean
        :return:
        """
        self.__phases = pob

    def set_R(self, r):
        """
        :param r: a list of double
        :return:
        """
        self.__R = r

    def set_X(self, x):
        """
        :param x: a list of double
        :return:
        """
        self.__X = x

    def set_length(self, l):
        """
        :param l: a double
        :return:
        """
        self.__length = l

    def set_Imax(self, imax):
        """
        :param imax: a double
        :return:
        """
        self.__Imax = imax

    def calculate_impedance(self):
        """
        Will calculate impedances on the differant phases.
        impedance must look like:
        [[11, 12, 13], [21, 22, 23], [31, 32, 33]]
        Z[i] = (R[i]+jX[i])*length
        :return: impedance, a 3 by 3 matrix
        """
        impedance = [[0 for i in range(3)] for j in range(len(self.__phases))]
        R = self.__R
        X = self.__X
        for i in range(len(self.__phases)):
            phase = []
            for j in range(len(self.__phases)):
                phase.append((complex(R[i][j]*self.__length, X[i][j]*self.__length)))
            impedance[i] = [phase[0], phase[1], phase[2]]
        return [impedance[0], impedance[1], impedance[2]]

    def __str__(self):
        return "Branch"+" Phases: "+str(self.__phases)


if __name__ == '__main__':
    pass
