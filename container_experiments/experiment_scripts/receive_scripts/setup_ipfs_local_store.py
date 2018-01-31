"""

Perform operation on local store of ipfs

python setup_ipfs_local_store.py <MODE> <EXPERIMENT> <ACTION>
                 <MODE> is either 'US' or 'WORLD'
                 "<EXPERIMENT> is either 'SHUFFLE' or 'UNDER_ATTACK'"
                 <ACTION> is either 'ADD' or  'DEL'
                 For 'DEL', doesn't matter what <EXPERIMENT> is set to
"""


import os
import subprocess
import sys
from datetime import datetime
import time
import csv
import shutil

SERV_INFO_SHUFFLE_US = '../server_info/server_ips_SHUFFLE_US.csv'
SERV_INFO_SHUFFLE_WO = '../server_info/server_ips_SHUFFLE_world.csv'
KEY = '../key/aws_keys/id_rsa'

def exec_command(address, image):
    command = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " " + address + " /home/ubuntu/go/bin/ipfs add " + image
    os.popen(command)

def main():
    num_args = len(sys.argv)
    if num_args != 4:
        print "USAGE: python setup_ipfs_local_store.py <MODE> <EXPERIMENT> <ACTION>"
        print "<MODE> is either 'US' or 'WORLD'"
        print "<EXPERIMENT> is either 'SHUFFLE' or 'UNDER_ATTACK'"
        print "<ACTION> is either 'ADD' or  'DEL'"
        return

    experiment = sys.argv[2]
    action = sys.argv[3]
    file = ""
    if sys.argv[1] == "US":
        file = SERV_INFO_SHUFFLE_US
    elif sys.argv[1] == "WORLD":
        file = SERV_INFO_SHUFFLE_WO
    else:
        print "Incorrect Mode: use either US/WORLD"
        return

    with open(file, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        iplist = [row.get('publicip') for row in reader]

    # setup ipfs
    if action == 'ADD':
        if experiment == 'SHUFFLE':
            for i in range(1,9):
                address = 'ubuntu@' + iplist[i-1]
                image1 = str(2*i - 1)
                image2 = str(2*i) 
                exec_command(address, image1)
                exec_command(address, image2)
        elif experiment == 'UNDER_ATTACK':
            for i in range(1,5):
                address = 'ubuntu@' + iplist[i-1]
                image1 = str(4*i - 3) 
                image2 = str(4*i - 2)
                image3 = str(4*i - 1)
                image4 = str(4*i) 
                exec_command(address, image1)
                exec_command(address, image2)
                exec_command(address, image3)
                exec_command(address, image4)
        else:
            print "Incorrect EXPERIMENT: use either SHUFFLE/UNDER_ATTACK"
    elif action == 'DEL':
        for ip in iplist:
            address= 'ubuntu@' + ip
            unpin = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " " + address + " /home/ubuntu/go/bin/ipfs pin ls --type recursive | cut -d' ' -f1 | xargs -n1 /home/ubuntu/go/bin/ipfs pin rm"
            os.popen(unpin)
            gc = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + " " + address + " /home/ubuntu/go/bin/ipfs repo gc"
            os.popen(gc)
    else:
        print "Incorrect ACTION: use either ADD/DEL"

if __name__ == '__main__':
    main()