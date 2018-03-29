from app.serialization.serialization import Serialization


# Metaclass for Singleton Pattern
class Singleton(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance

    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__call__()
        return cls.__instance


# This class implements Singleton Pattern and will contain every Network in our database
class NetworkManager(metaclass=Singleton):
    """
    List<Network> networks
    """

    def __init__(self):
        self.__networks = []

    def get_networks(self):
        return self.__networks

    def set_networks(self, net):
        self.__networks=net

    def add_network(self, network):
        self.get_networks().append(network)
        return network

    def delete_network(self, network):
        self.__networks.remove(network)

    def update_network(self, id, network_updated):
        self.__networks[id] = network_updated
        return self.__networks[id]

    def research_network_by_id(self,id):
        return self.get_networks()[id]

    def research_network_by_object(self, network):
        return self.get_networks().index(network)

    @staticmethod
    # This will load a network from the given path_to_file
    def load_network_from_xlsx(path_to_file):
        ntw = Serialization.load_network_from_XLSX(path_to_file)
        return ntw


if __name__ == '__main__':
    pass
