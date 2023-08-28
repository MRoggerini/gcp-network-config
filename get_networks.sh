#! /bin/bash

for PROJECT in $(cat projects.txt)
do
	if [[ ${PROJECT} == *-* ]]
	then
		echo "project: $PROJECT"

		# list subnetworks in project
		gcloud compute networks subnets list \
			--project=$PROJECT \
			--format=json | jq "[.[] | { name: .name, network: .network, IPv4: .ipCidrRange, IPv6: .ipv6CidrRange, region: .region, subnets: .secondaryIpRanges }]" > $FOLDER/$PROJECT-nets.json 

		# list of all VPC-PEERING reserved IPs in the project
		gcloud compute addresses list \
			--project=$PROJECT \
			--filter='purpose:VPC_PEERING' \
			--format=json | jq "[.[] | { address: .address, name: .name, network: .network, prefixLength: .prefixLength }]" > $FOLDER/$PROJECT-peer.json

		# list VPC access connectors in the project
		printf '' > $FOLDER/$PROJECT-connectors.json
 		echo '[' >> $FOLDER/$PROJECT-connectors.json
		for i in {1..10}
		do
			gcloud compute networks vpc-access connectors list \
				--project=$PROJECT \
				--region=europe-west$i \
				--format=json | jq '.[] | {name: .name, IPv4: .ipCidrRange, network: .network}' >> $FOLDER/$PROJECT-connectors.json
		done
 		echo ']' >> $FOLDER/$PROJECT-connectors.json
	else
		FOLDER=$PROJECT
	fi
done
