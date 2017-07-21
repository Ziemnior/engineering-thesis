from wifi import Cell, Scheme
from collections import namedtuple
from operator import attrgetter
from wifi.exceptions import ConnectionError

class NetworkConnection(object):
	
	def __init__(self, prefix):
		self.prefix = prefix	

        def discoverAvalibleNetworks(self):
                all_networks = []
                avalible_networks = Cell.all('wlan0')
                for network in avalible_networks:
                        all_networks.append(network)
                return all_networks


        def selectAppropriateNetworks(self):
                appropriate_network = namedtuple('network', 'ssid quality encrypted encryption_type')
                appropriate_networks = []
                for network in self.discoverAvalibleNetworks():
                        if network.ssid.startswith(self.__init__()):
		                appropriate_networks.append(appropriate_network(network.ssid, network.quality, network.encrypted, network.encryption_type))
                return appropriate_networks


        def sortAppropriateNetworks(self):
                unsorted_appropriate_networks = self.selectAppropriateNetworks()
                sorted_appropriate_networks = sorted(unsorted_appropriate_networks, key = attrgetter('quality'), reverse = True)
                return sorted_appropriate_networks


        def connectToGateway(self, interface, password):
                networks = self.sortAppropriateNetworks()
                for network in networks:
                        try:
				print(network)
                                scheme = Scheme.for_cell(interface, network.ssid, network, password)
                                scheme.save()
                                scheme.activate()
                                print('connected to {}').format(network.ssid)
                        except ConnectionError:
                                print("couldn't connect to network")
			except AssertionError:
				scheme = Scheme.find(interface, network.ssid)
				scheme.activate()
                        else:
                                print("general error")
				network.delete()



connection = NetworkConnection('TP')
connection.connectToGateway('wlan0', 'lolidupa')
