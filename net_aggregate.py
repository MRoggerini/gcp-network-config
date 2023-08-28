#!/usr/bin/python3

import json
import yaml


# this file binds each networking project to its legal entity
projects = json.load(open('projects.json'))
network = {}

for legal_entity, prjs in projects.items():
    network[legal_entity] = {
        'landing': {},
        'nonprod': {},
        'prod': {}
    }
    for project in prjs:
        if 'landing' in project:
            current_env = network[legal_entity]['landing']
        elif 'nonprod' in project:
            current_env = network[legal_entity]['nonprod']
        else:
            current_env = network[legal_entity]['prod']

        subnets = json.load(open(f'{legal_entity}/{project}-nets.json'))
        connectors = json.load(open(f'{legal_entity}/{project}-connectors.json'))
        peering = json.load(open(f'{legal_entity}/{project}-peer.json'))

        for subnet in subnets:
            net = subnet['network'].split('/')[-1]

            try:
                current_net = current_env[net]
            except KeyError:
                current_env[net] = {
                    'subnets': {},
                    'peering': {},
                    'connectors': {}
                }
                current_net = current_env[net]

            subnet_name = f'{subnet["name"]} {subnet["region"].split("/")[-1]}'
            current_net['subnets'][subnet_name] = {
                'IP': subnet['IPv4'],
            }

            try:
                current_subnets = {
                    i['rangeName']: i['ipCidrRange'] for i in subnet['subnets']
                }
            except TypeError:
                current_subnets = {}

            current_net['subnets'][subnet_name]['secondary_ranges'] = current_subnets

        for peer in peering:
            try:
                net = peer['network'].split('/')[-1]
            except:
                continue
            current_net['peering'][peer['name']] = f'{peer["address"]}/{peer["prefixLength"]}'

        for connector in connectors:
            try:
                net = connector['network'].split('/')[-1]
            except:
                continue
            current_net['connectors'][connector['name']] = connector['IPv4']


yaml.dump(network, open('net_config.yaml', 'w'))
