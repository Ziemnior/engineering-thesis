from wifi import Cell, Scheme
from collections import namedtuple
from operator import attrgetter
from wifi.exceptions import ConnectionError

from optparse import OptionParser


class NetworkConnection:
    def __init__(self, prefix, interface, password):
        self.prefix = prefix
        self.interface = interface
        self.password = password

    def discover_avalible_networks(self, interface=None):
        all_networks = []
        interface = self.interface
        avalible_networks = Cell.all(interface)
        for network in avalible_networks:
            all_networks.append(network)
        return all_networks

    def select_appropriate_networks(self, prefix=None):
        appropriate_network = namedtuple('network', 'ssid quality encrypted encryption_type')
        appropriate_networks = []
        prefix = self.prefix
        for network in self.discover_avalible_networks():
            if network.ssid.startswith(prefix):
                appropriate_networks.append(
                    appropriate_network(network.ssid, network.quality, network.encrypted, network.encryption_type))
        return appropriate_networks

    def sort_appropriate_networks(self):
        unsorted_appropriate_networks = self.select_appropriate_networks()
        sorted_appropriate_networks = sorted(unsorted_appropriate_networks, key=attrgetter('quality'), reverse=True)
        return sorted_appropriate_networks

    def connect_to_gateway(self, interface=None, password=None):
        interface = self.interface
        password = self.password
        networks = self.sort_appropriate_networks()
        for network in networks:
            try:
                print("Trying to connect to {}").format(network.ssid)
                scheme = Scheme.for_cell(interface, network.ssid, network, password)
                scheme.save()
                scheme.activate()
                print("Connected to {}").format(network.ssid)
                break
	    except AssertionError:
		scheme = Scheme.find(interface, network.ssid)
		try:
		    scheme.activate()
                    print("Connected to {}").format(network.ssid)
                except ConnectionError:
                    print("Couldn't connect to {}").format(network.ssid)
                    scheme = Scheme.find(interface, network.ssid)
                    scheme.delete()
		    continue       
	        break
            except ConnectionError:
                print("Couldn't connect to {}").format(network.ssid)
                scheme = Scheme.find(interface, network.ssid)
                scheme.delete()
		continue       
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-p', '--prefix', dest='prefix', help="Specify gateway ssid prefix")
    parser.add_option('-i', '--interface', dest='interface', help="Specify name of wireless interface of choice")
    parser.add_option('-q', '--password', dest='password',
                      help="Specify password for the wireless network of choice")
    options, args = parser.parse_args()
    wireless_connection = NetworkConnection(prefix=options.prefix, interface=options.interface,
                                            password=options.password)
    wireless_connection.connect_to_gateway()

