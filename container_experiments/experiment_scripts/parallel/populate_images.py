"""

Transfer images to the testbed

python populate_images.py 'US' ~/Desktop/images
python populate_images.py 'WORLD' ~/Desktop/images
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
    if num_args != 3:
        print "USAGE: python populate_images.py <MODE> <images_dir>"
        print "<MODE> is either US or WORLD"
        print "<images_dir> : directory where the container images are stored"
        return

    images_dir = sys.argv[2]
    file = ""
    if sys.argv[1] == "US":
        file = SERV_INFO_SHUFFLE_US
    elif sys.argv[1] == "WORLD":
        file = SERV_INFO_SHUFFLE_WO
    else:
        print "Incorrect Mode: US/WORLD"
        return

    with open(file, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        iplist = [row.get('publicip') for row in reader]

    # send 2 container images to each machine
    for i in range(5,9):
        address = 'ubuntu@' + iplist[i-1] + ':'
        image1 = images_dir + '/' + str(2*i - 1)
        image2 = images_dir + '/' + str(2*i)
        command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + image1 + " " + address
        os.popen(command)
        command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + image2 + " " + address
        os.popen(command)
        # subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, image1, address])
        # subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, image2, address])

    # send 4 container images to each machine
    for i in range(1,5):
        address = 'ubuntu@' + iplist[i-1] + ':'
        image1 = images_dir + '/' + str(2*i + 7) 
        image2 = images_dir + '/' + str(2*i + 8)
        image3 = images_dir + '/' + str(2*i - 1)
        image4 = images_dir + '/' + str(2*i) 
        command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + image1 + " " + address
        os.popen(command)
        command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + image2 + " " + address
        os.popen(command)
        command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + image3 + " " + address
        os.popen(command)
        command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + image4 + " " + address
        os.popen(command)
        # subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, image1, address])
        # subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, image2, address])
        # subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, image3, address])
        # subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, image4, address])
    
if __name__ == '__main__':
    main()