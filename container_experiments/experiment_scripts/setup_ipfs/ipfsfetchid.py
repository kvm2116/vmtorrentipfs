# -*- coding: utf-8 -*-
import subprocess
import os
import csv


"""

python ipfsfetchid.py
"""

ips = []

with open('dest_ips.txt', 'r') as f:
	for ip in f:
		ips.append(ip.strip('\n'))
print ips

with open('ids.csv', 'w') as fd:
	writer = csv.writer(fd, delimiter=',')
	for i in range(len(ips)):
		command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/Downloads/id_rsa ubuntu@" + ips[i] + " /home/ubuntu/go/bin/ipfs id | grep 'ID' | cut -d' ' -f2 | cut -d',' -f1"
		ipfsid = os.popen(command)
		command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/Downloads/id_rsa ubuntu@" + ips[i] + " /home/ubuntu/go/bin/ipfs id | grep 'ip4/10'"
		# print command
		addr = os.popen(command)
		ipid = ipfsid.read().strip()
		address = addr.read().strip()
		writer.writerow([ips[i], ipid, address])

# Run this command after
# manually do cleanup after