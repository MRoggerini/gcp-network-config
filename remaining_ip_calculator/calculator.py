from netaddr import *
import json
import copy


net_config = json.load(open('net_config.json'))

start_net = IPSet(IPNetwork(net_config["network"]))
final_net = copy.deepcopy(start_net)
print(final_net)

for subnet in net_config["subnets"]:
    subnet = IPSet(IPNetwork(subnet))
    # symmetric difference
    final_net -= subnet

print(f'starting available IPs:  {len(start_net)}')
print(f'currently available IPs: {len(final_net)}')
print(f'currently available nets: {final_net}')
