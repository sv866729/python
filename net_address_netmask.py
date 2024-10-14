import ipaddress

def get_network_info(cidr):
    # Create an IP network object
    network = ipaddress.ip_network(cidr, strict=False)
    
    # Get the network address and netmask
    network_address = str(network.network_address)
    netmask = str(network.netmask)
    
    return network_address, netmask
