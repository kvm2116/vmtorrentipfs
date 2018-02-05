#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from datetime import datetime
import time
import csv


"""

python generate_csv.py.py
"""

e_ips = []
ips = []
zone_list = ['Oregon','Oregon','Oregon','Oregon','N. Virginia','N. Virginia','N. Virginia','N. Virginia']
image1_list = [1,3,5,7,9,11,13,15]
image2_list = [2,4,6,8,10,12,14,16]
GETIMAGE1_list = [9,10,11,12,1,2,3,4]
GETIMAGE2_list = [13,14,15,16,5,6,7,8]
KEY = '../key/aws_keys/id_rsa'

def main():
    with open('dest_ips.txt', 'r') as fr:
            for ip in fr:
                e_ips.append(ip.strip('\n'))
    ips = e_ips[:8] 
    print ips

    with open('../server_info/server_ips_SHUFFLE_US.csv', 'w') as csvwritefile:
        fieldnames = ['nodename','instanceid', 'zone','publicip','privateip','ipfsid', 'ipfsaddress', 'image1', 'image2', 'ipfsimage1', 'ipfsimage2', 'GETIMAGE1', 'GETIMAGE2', 'GETIPFSIMAGE1', 'GETIPFSIMAGE2']
        writer = csv.DictWriter(csvwritefile, delimiter=',',lineterminator='\n', fieldnames=fieldnames)
        writer.writeheader()
        for idx, val in enumerate (ips):
            # for grabbing the private ip of node so only receive files from other nodes.
            nodename = 'N' + str(idx+1)
            zone = zone_list[idx]
            public_ip = val
            command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " ubuntu@" + ips[idx] + " /home/ubuntu ifconfig eth0 | grep 'inet\ addr' | cut -d: -f2 | cut -d' ' -f1"
            f = os.popen(command)
            private_ip=f.read().strip('\n')
            command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " ubuntu@" + ips[idx] + " /home/ubuntu/go/bin/ipfs id | grep 'ID' | cut -d' ' -f2 | cut -d',' -f1"
	    ipfsid = os.popen(command)
            ipfsaddress = '/ip4/' + private_ip + '/tcp/4001/ipfs/' + str(ipfsid)
            img1 = image1_list[idx]
            img2 = image2_list[idx]
            command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " ubuntu@" + ips[idx] + " /home/ubuntu/go/bin/ipfs add /home/ubuntu/" + str(img1)
            ipfsimg1 = os.popen(command)
            command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " ubuntu@" + ips[idx] + " /home/ubuntu/go/bin/ipfs add /home/ubuntu/" + str(img2)
            ipfsimg2 = os.popen(command)
            getimg1 = GETIMAGE1_list[idx]
            getimg2 = GETIMAGE2_list[idx]
            command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " ubuntu@" + ips[idx] + " /home/ubuntu/go/bin/ipfs add /home/ubuntu/" + str(getimg1)
            getipfsimg1 = os.popen(command)
            command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " ubuntu@" + ips[idx] + " /home/ubuntu/go/bin/ipfs add /home/ubuntu/" + str(getimg2)
            getipfsimg2 = os.popen(command)
            writer.writerow({'nodename': nodename,'zone': zone,'publicip': public_ip,'privateip': private_ip,'ipfsid': ipfsid, 'ipfsaddress': ipfsaddress, 'image1': img1, 'image2': img2, 'ipfsimage1': ipfsimg1, 'ipfsimage2': ipfsimg2, 'GETIMAGE1': getimg1, 'GETIMAGE2': getimg2, 'GETIPFSIMAGE1': getipfsimg1, 'GETIPFSIMAGE2': getipfsimg2})

if __name__ == "__main__":
   main()
