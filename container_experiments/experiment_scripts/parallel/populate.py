import os
import subprocess
import sys
from datetime import datetime
import time
import csv
import shutil


SERV_INFO_ATTACK_US = '../server_info/server_ips_UNDER_ATTACK_US.csv'
SERV_INFO_ATTACK_WO = '../server_info/server_ips_UNDER_ATTACK_world.csv'
SERV_INFO_SHUFFLE_US = '../server_info/server_ips_SHUFFLE_US.csv'
SERV_INFO_SHUFFLE_WO = '../server_info/server_ips_SHUFFLE_world.csv'
src_dir = '~/'
dest_dir = '~/images/'
key = '/Users/rag2183/research/container_experiments/experiment_scripts/key/aws_keys/id_rsa'


def main():
    num_args = len(sys.argv)
    if num_args != 0:
        print "USAGE: python populate.py"
        return
    #trial_num = sys.argv[1]

    with open(SERV_INFO_ATTACK_US, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        nodes = list(reader)


        #- send scripts to machines
        for row in nodes:
            ip = row["privateip"]
            #python populate_nodes <mode>
            subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../../experiment_scripts', 'ubuntu@', ip, ':'])



        # machine 1    
        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/1', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/2', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/3', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/4', 'ubuntu@', , ':'])
        

        # machine 2
        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/5', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/6', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/7', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/8', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/3', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/4', 'ubuntu@', , ':'])


        #machine 3
        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/9', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/10', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/11', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/12', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/5', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/6', 'ubuntu@', , ':'])


        #machine 4
        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/13', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/14', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/15', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/16', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/7', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/8', 'ubuntu@', , ':'])


        #machine 5
        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/9', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/10', 'ubuntu@', , ':'])



        # machine 6
        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/11', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/12', 'ubuntu@', , ':'])

    

        # machine 7
        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/13', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/14', 'ubuntu@', , ':'])

    


        # machine 8
        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/15', 'ubuntu@', , ':'])

        subprocess.cal(['ssh', '-i', key, 'ubuntu@', ip, 'sudo', 'screen', '-d', '-m', 'scp', '-r', '-i', '../containers/16', 'ubuntu@', , ':'])

    
