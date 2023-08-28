#!/usr/bin/python3

from netaddr import *
import yaml
import copy
import sys


invalid_prompt = '''usage:
    calculator.py cidr network

    cidr: an IP CIDR in the form of x.x.x.x/y (suggested: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
    network: name of the VPC to analyze'''

if len(sys.argv) < 3:
    print(invalid_prompt)
    exit()

start_ip = sys.argv[1]
net = sys.argv[2]

net_config = yaml.safe_load(open('net_config.yaml'))

start_net = IPSet(IPNetwork(start_ip))
final_net = copy.deepcopy(start_net)

selected_net = None

for _, country in net_config.items():
    for _, env in country.items():
        if net in env:
            selected_net = env[net]
            break
    if selected_net:
        break

if not selected_net:
    print(f'network {net} does not exist!')
    exit()

allocated = []
allocated += [i for _, i in selected_net['peering'].items()]
allocated += [i for _, i in selected_net['connectors'].items()]

for _, i in selected_net['subnets'].items():
    allocated.append(i['IP'])
    allocated += [j for _, j in i['secondary_ranges'].items()]

for subnet in allocated:
    subnet = IPSet(IPNetwork(subnet))
    final_net -= subnet

print(f'starting available IPs:  {len(start_net)}')
print(f'currently available IPs: {len(final_net)}')
print(f'currently available nets:')
for i in final_net.iter_cidrs():
    print(i)
