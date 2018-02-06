"""

Transfer scripts to the machines 
python populate_scripts.py <directory>
python populate_scripts.py ../../experiment_scripts
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

def main():
    num_args = len(sys.argv)
    if num_args != 2:
        print "USAGE: python populate_scripts.py <directory>"
        print "<directory> : directory where the scripts are stored"
        return

    directory = sys.argv[1]
    
    with open(SERV_INFO_SHUFFLE_US, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        iplist = [row.get('publicip') for row in reader]

    with open(SERV_INFO_SHUFFLE_WO, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            iplist.append(row.get('publicip'))

    # send scripts
    for ip in iplist:
        address = 'ubuntu@' + ip + ':'
        command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + directory + " " + address 
        os.popen(command)   
        # subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, '-r', directory, address])
    
if __name__ == '__main__':
    main()