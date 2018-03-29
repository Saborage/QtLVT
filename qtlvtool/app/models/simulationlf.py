from time import process_time

import numpy as np
from scipy.sparse import block_diag

from app.models.timestamp import Timestamp
import os


class SimulationLF:
    def __init__(self, nb=1, tol=0.01, delta=Timestamp.QUARTERS):
        """
        :param nb: for number of iterations to do for Monte Carlo
        :param tol: the value to which the voltages have to converge
        :param delta: a Timestamp value which can be: Timestamp.QUARTERS, Timestamp.HOURS, Timestamp.DAYS.
        """
        if nb > 0:
            self.__nb_iterations = nb
        if tol >= 0:
            self.__tolerance = tol
        if delta in Timestamp:
            self.__delta_time = delta
            self.__q = self.calculate_Q()

    def calculate_Q(self):
        """
        This method will check the value of the simulation's delta_time and will set the Q index value for Monte Carlo
        loop.
        :return: q, which can be 96 if we use Quarters, 24 for Hours and 1 for Days.
        """
        if self.__delta_time is Timestamp.QUARTERS:
            q = 96
        elif self.__delta_time is Timestamp.HOURS:
            q = 24
        else:
            q = 1
        return q

    # GETTERS/ACCESSORS
    def get_nb_iterations(self): return self.__nb_iterations

    def get_tolerance(self): return self.__tolerance

    def get_delta_time(self): return self.__delta_time

    # SETTERS/MUTATORS
    def set_nb_iterations(self, nb): self.__nb_iterations = nb

    def set_tolerance(self, t): self.__tolerance = t

    def set_delta_time(self, d): self.__delta_time = d

    def grid_definition(self, network):
        zeros = np.zeros
        # As we are working with brackets that are containing a node and a branch, the number of brackets corresponds
        # to the number of nodes
        nb_brackets = network.get_nb_brackets()-1
        # Boolean vector of nodes phases [ [1, 1, 1], [1, 1, 1], ...]
        vec_phases = np.ones((1, 3 * nb_brackets))
        vec_phases = vec_phases[0]
        # Number of phases for each node/bracket
        num_phases = zeros((1, nb_brackets+1))
        num_phases = num_phases[0]
        # Parent line impedances (intermediate step for Zbr construction
        z = [0 for i in range(nb_brackets)]
        # Power matrix (3 possible phases, number of nodes)
        # p = zeros(3, nb_brackets)
        # K = cell(nb_brackets, nb_brackets): This kind of Matlab variable can be translated into a nested list.
        K = [[np.zeros((3, 3), int) for j in range(nb_brackets)]
             for i in range(nb_brackets)]
        # As we are going to use the list a certain number of times, we are assigning it to a variable for more
        # efficiency
        brackets = network.get_brackets()
        vec_phases[0:3] = brackets[0].get_branch().get_phases()
        num_phases[0] = np.sum(brackets[0].get_branch().get_phases())
        for i in range(1, nb_brackets+1):
            current_bracket = brackets[i-1]
            vec_phases[3*(i-1):3*(i-1)+3] = current_bracket.get_branch().get_phases()
            num_phases[i] = np.sum(current_bracket.get_branch().get_phases())
        vec_phases_index = np.nonzero(vec_phases)[0]

        # We won't work on the slack node because it is pointless, so we're only taking nodes starting with the second
        brackets = brackets[1:]
        for i in range(nb_brackets):
            current_bracket = brackets[i]
            # p = self.power_definition()
            z[i] = (current_bracket.get_branch().calculate_impedance())
            for j in range(nb_brackets):
                # If there is a path, we change K[i,j,k,k] to -1
                if i + 2 in network.find_path(0, j):
                    for k in range(3):
                        K[i][j][k][k] = -1
        K = np.vstack([np.hstack(c) for c in K])
        K = K[vec_phases_index][vec_phases_index]
        # z = np.reshape(z, (19,1))
        Zbr = block_diag(z).toarray()
        Zbr = Zbr[vec_phases_index][vec_phases_index]
        # Transforming all of our matrixes into real matrixes. At this point, they were just arrays.
        K = np.mat(K)
        Zbr = np.mat(Zbr)
        # Zbr = Zbr[vec_phases_index[:], vec_phases_index[:]]
        # np.resize(Zbr, (len(Zbr)*3, len(Zbr)*3))
        # End of Grid_definition
        return {
            'K': K,
            'Zbr': Zbr,
            'vec_phases_index': vec_phases_index
        }

    # LOAD FLOW METHOD
    def load_flow(self, network):
        """
        This method will implement the Load Flow algorithm.
        :param: network: the network on which we want to do the load flow.
        :return: dic: A dictionnary containing every matrix/array involved in the load flow resolution.
        """
        # main.m
        alpha = 1
        nb_brackets = network.get_nb_brackets()-1
        # Battery settings
        bat_node = 2
        bat_phase = 2
        bat = (bat_node-2)*3 + bat_phase
        Ebat = 0
        Ebat_max = 120000
        Pbat = 60000
        # End
        # Grid_definition.m
        grid = self.grid_definition(network)
        K = grid['K']
        Zbr = grid['Zbr']
        vec_phases_index = grid['vec_phases_index']
        # End of Grid_Definition
        brackets = network.get_brackets()[1:]
        network_nodes = [brackets[i].get_node() for i in range(nb_brackets)]
        # load_flow.m
        Ibus = np.zeros((3 * nb_brackets), dtype=np.complex128)
        Ibus = Ibus[:, np.newaxis]
        Vnl = network.get_slack_voltage()
        Vnl = Vnl[vec_phases_index]
        Vbus = Vnl
        Vbr_prev = Vnl
        # If we don't define Tmp as a N-Dim Array, the Tile function will broadcast it to a N-Dim Array of shape
        # (1, 1, 57) instead of letting it be (57, 1, 1). This will result by producing a new matrix of shape
        # (1, 570, 96). I guess that the tile function will perform some multiplication on the dimensions
        # and then will join'em. If Vnl(57,1) & Newmat(10,96):
        # Result = (1, 57*10, 96)... Which is not really what we want.
        Tmp = (Vnl * 0)
        Tmp = Tmp[:, np.newaxis]
        V = np.tile(Tmp, (1,1,1))
        I = np.tile(Tmp, (1,1,1))
        # We don't use the Tmp matrix here because Vnl won't be broadcasted to a 3D matrix but to a 1D. So the bug
        # that has been resolved earlier won't happen here
        # Imean = np.tile(Vnl*0, (96))
        # Vmean = np.tile(Vnl*0, (96))
        powers = []

        for node in network_nodes:
            n_pow = []
            for user in node.get_users():
                n_pow.append(user.get_P())
            powers.extend(n_pow)

        """
        Here, we are assigning the NumPy functions we are going to use into the load flow loop to gain
        a little bit more efficiency.
        """
        # NumPy Functions
        conj = np.conj
        divide = np.divide
        absolute = np.abs
        less = np.less
        zeros = np.zeros
        # Here is the wrapping of the load flow:
        # h = 0, nb iterations
        # q = 0, 96
        P = np.asarray(powers)
        P = divide(P, 2)
        Q = np.dot(P, np.array([0]))
        # Initializing arrays to optimize
        Ibr = zeros((nb_brackets, 1))
        Vbr = zeros((nb_brackets, 1))
        # Before we enter the loop, we make sure we are going to work with matrices instead of arrays.
        Ibr = np.matrix(Ibr)
        Vbr = np.matrix(Vbr)
        # LOAD FLOW LOOP
        k = 0
        t = process_time()
        while True:
            k += 1
            bal = 0
            for i in range(len(P)):
                if k == 1:
                    Ibus[i] = -(np.matrix(np.complex(P[i], Q[i])/Vbus[i]).conj())
                else:
                    Ibus[i] = -(np.matrix(np.complex(P[i], Q[i]) / Vbus[i]).conj())
                if i % 3 == bat:
                    bal = bal + P[i]
            if bat != 0:
                if bal < 0:
                    if Ebat < Ebat_max:
                        Ibus[bat] = min([conj(-Pbat/Vbus[bat]),
                                         conj(bal/Vbus[bat]),
                                         conj(-(Ebat_max - Ebat)/(Vbus[bat]*0.25))])
                        Ebat += absolute(np.dot(Ibus[bat], Vbus[bat])) * 0.25
                    elif Ebat > 0:
                        Ibus[bat] = min([conj(Pbat/Vbus[bat]),
                                         conj(bal/Vbus[bat]),
                                         conj(Ebat/(Vbus[bat]*0.25))])
                        Ebat -= absolute(np.dot(Ibus[bat], Vbus[bat])) * 0.
            Ibr = K * Ibus
            Vbr = Zbr * Ibr
            if (less(divide(absolute(Vbr - Vbr_prev), absolute(Vbr + 0.0000000000000001)), self.__tolerance)).all():
                break
            Vbr = Vbr_prev + (alpha * (Vbr - Vbr_prev))
            Vbr_prev = Vbr
            Vbus = Vnl + np.dot(K.conj().T, Vbr)
        Vbus = Vnl + np.dot(K.conj().T, Vbr)
        V[:] = Vbus[:, :, np.newaxis]
        I[:] = Ibr[:, :, np.newaxis]
        Pbr = Qbr = np.array([[[0 for k in range(2)]for j in range(len(vec_phases_index))] for i in range(nb_brackets)])
        for i in range(nb_brackets):
            for j in range(len(vec_phases_index)):
                i_to_j = self.powerflow(Vbus[i], Ibr[i])
                j_to_i = self.powerflow(Vbus[i+1], Ibr[i])
                Pbr[i][j][0] = i_to_j['active']
                Pbr[i][j][1] = j_to_i['active']
                Qbr[i][j][0] = i_to_j['reactive']
                Qbr[i][j][1] = j_to_i['reactive']
        print(np.shape(Pbr), Qbr.shape)
        # END OF LOAD FLOW
        # End of load_flow.m
        print("Process executed in", process_time() - t, "s")
        dic = {
            'Ibus_bat': Ibus[bat],
            'Ebat': Ebat,
            'V': V,
            'Vbr': Vbr,
            'Vbus': Vbus,
            'I': I,
            'Ibus': Ibus,
            'Ibr': Ibr,
            'Zbr': Zbr,
            'P': P,
            'K': K,
            'Vnl': Vnl,
            'Pbr': Pbr,
            'Qbr': Qbr
        }
        return dic

    def powerflow(self, voltage, intensity, conj=np.conj, real=np.real, imag=np.imag):
        flow = voltage * conj(intensity)
        return {
            'active': real(flow),
            'reactive': imag(flow)
        }

    def printMenu(self, network):
        np.set_printoptions(threshold=np.nan, suppress=True, precision=10)
        # import re
        while True:
            # This block is relevant if we use a timestamp.
            # It will check the user's input.
            # If you uncomment the block, don't forget to uncomment "import re"
            """print("Which time do you want to simulate over? (hh:mm:ss) (q or Q to quit)")
            try:
                timestamp = str(input())
                if timestamp is 'q' or timestamp is 'Q':
                    print("Goodbye!")
                    break
                # The following is called a Regular Expression:
                # It will check if a user input matches a given pattern.
                # In this case, the pattern is:
                # [0-2 digit][0-9 digit]:[0-5 digit][0-9 digit]:[0 digit][0 digit]
                # (?!00:00:00) will ensure that the following pattern won't result in the string "00:00:00"
                # (We use the format 01:00:00 -> 24:00:00 and not 00:00:00 -> 23:59:59)
                # The first group ([0-1][0-9]|2[0-3]):
                #   It will check if we enter an hour between 00 and 19, or between 20 and 23.
                # Then if we entered the first group, it will check if we enters mins and secs between 00 and 59.
                # Finally, if we did not enter a matching hour (between 00 and 23), it will check if the expression
                # matches the last group: 24:00:00.
                if not re.compile("(?!00:00:00)((([0-1][0-9]|2[0-3]):[0-5][0-9]:00)|(24:00:00))") \
                        .match(timestamp):
                    print("Please enter a valid time : hh:mm:ss")
                    continue
            except TypeError:
                continue"""

            print("                      GELEC MAIN MENU")
            print("Low Voltage Tool ------------------------- Debug Mode")
            print("-----------------------------------------------------")
            print("What would you want to do?")
            print(" 0. Exit debug mode")
            print(" 1. Print Network")
            print(" 2. Print Voltages (V[i][j]([h][q]))")
            print(" 3. Print Voltages at branches (Vbr)")
            print(" 4. Print Voltages at nodes (Vbus)")
            print(" 5. Print Intensities (I[i][j]([h][q]))")
            print(" 6. Print Intensities at nodes (Ibus)")
            print(" 7. Print Intensities at branches(Ibr)")
            print(" 8. Print Power Flows on Branches")
            print(" 9. Print Topology (K)")
            print("10. Print Voltages at slack node (Vnl)")
            print("11. Print Impendances on branches (Zbr)")
            print("12. Print Intensity at battery node(Ibus[bat])")
            print("13. Print Energy at battery(Ebat)")
            try:
                choice = int(input())
            except ValueError:
                continue

            if choice == 0:
                print("Goodbye!")
                break
            if choice == 1:
                from anytree.render import RenderTree
                root = network.get_slack_node()
                tree = RenderTree(root)
                for pre, _, node in tree:
                    print("%s%s" % (pre, "Node " + str(node.get_id())))
            else:
                print("calculating load flow...")
                load_flow = self.load_flow(network)
                if choice == 2:
                    voltages = load_flow['V']
                    mods = []
                    phases = []
                    print(voltages)
                    """for el in voltages:
                        mods.append(np.absolute(el))
                        phases.append(np.angle(el))
                    for i, e in enumerate(voltages):
                        print("Node %s: %s e^%s" % ((i//3)+1,mods[i][0], phases[i][0]))"""
                    print(np.shape(voltages))
                elif choice == 3:
                    Vbr = load_flow['Vbr']
                    mods = []
                    phases = []
                    for el in Vbr:
                        mods.append(np.abs(el))
                        phases.append(np.angle(el))
                    for i, e in enumerate(Vbr):
                        print("Node %s: %s e^%s" % ((i // 3) + 1, mods[i][0], phases[i][0]))
                    print(np.shape(Vbr))
                elif choice == 4:
                    Vbus = load_flow['Vbus']
                    mods = []
                    phases = []
                    for el in Vbus:
                        mods.append(np.abs(el))
                        phases.append(np.angle(el))
                    for i, e in enumerate(Vbus):
                        print("Node %s: %s e^%s" % ((i // 3) + 1, mods[i][0], phases[i][0]))
                    print(np.shape(Vbus))
                elif choice == 5:
                    intensities = load_flow['I']
                    for i, e in enumerate(intensities):
                        print("Node", (i//3)+1, e)
                    print(np.shape(intensities))
                elif choice == 6:
                    Ibus = load_flow['Ibus']
                    mods = []
                    phases = []
                    for el in Ibus:
                        mods.append(np.abs(el))
                        phases.append(np.angle(el))
                    for i, e in enumerate(Ibus):
                        print("Node %s: %s e^%s" % ((i // 3) + 1, mods[i][0], phases[i][0]))
                    print(np.shape(Ibus))
                elif choice == 7:
                    Ibr = load_flow['Ibr']
                    mods = []
                    phases = []
                    for el in Ibr:
                        mods.append(np.abs(el))
                        phases.append(np.angle(el))
                    for i, e in enumerate(Ibr):
                        print("Node %s: %s e^%s" % ((i // 3) + 1, mods[i][0], phases[i][0]))
                    print(np.shape(Ibr))
                elif choice == 8:
                    Pbr = load_flow['Pbr']
                    Qbr = load_flow['Qbr']
                    print("Active powers:\n")
                    for i, e in enumerate(Pbr):
                        print("Branch between %s and %s: %s" %(i, i+1, e))
                    print("Reactive power:\n", Qbr)
                elif choice == 9:
                    K = load_flow['K']
                    print(K)
                    print(np.shape(K))
                elif choice == 10:
                    Vnl = load_flow['Vnl']
                    mods = []
                    phases = []
                    for el in Vnl:
                        mods.append(np.abs(el))
                        phases.append(np.angle(el))
                    for i, e in enumerate(Vnl):
                        print("Node %s: %s e^%s" % ((i // 3) + 1, mods[i][0], phases[i][0]))
                    print(np.shape(Vnl))
                elif choice == 11:
                    Zbr = load_flow['Zbr']
                    Zbr = Zbr[np.nonzero(Zbr)]
                    mods = []
                    phases = []
                    for el in Zbr:
                        mods.append(np.abs(el))
                        phases.append(np.angle(el))
                    for i, e in enumerate(Zbr):
                        print("Modules\n: %s \n Phases:\n%s" % (mods[i][0], phases[i][0]))
                    print(np.shape(Zbr))
                elif choice == 12:
                    Ibat = load_flow['Ibus_bat']
                    print(Ibat)
                    print(Ibat.shape)
                elif choice == 13:
                    Ebat = load_flow['Ebat']
                    print("Ebat =", Ebat)
                else:
                    print("Please enter a valid number (see Main Menu)")


if __name__ == '__main__':
    from app.models.singleton import NetworkManager
    from app.serialization.serialization import Serialization
    sim = SimulationLF(tol=0.01)
    manager = NetworkManager()
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Block comment to uncomment before packaging
        """while True:
            print("Veuillez entrer le chemin du réseau à charger:")
            path = str(input())
            try:
                path = os.path.normpath(path)
                break
            except Exception:
                continue"""
        dir = os.path.dirname(__file__)
        path = os.path.normpath(os.path.join(dir, '..', '..', 'resource', 'Network_Flobecq.xlsx'))
        t0 = process_time()
        network = Serialization.load_network_from_XLSX(path)
        t1 = process_time()
    print("Network read in", t1 - t0, "seconds")
    manager.add_network(network)

    sim.printMenu(network)
