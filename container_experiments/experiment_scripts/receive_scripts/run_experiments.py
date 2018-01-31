""""

Run rsync, ipfs experiments for US and WORLD topology in 2 modes: Under Attack and Shuffle
python run_experiments.py <TRIAL_NUM>
python run_experiments.py 1
"""


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
src_dir = '/home/ubuntu/'
dest_dir = '/home/ubuntu/images/' 
key = '../key/aws_keys/id_rsa'
trial_num = 0
RSYNC_SCRIPT = '/home/ubuntu/experiment_scripts/receive_scripts/get_rsync.py'
IPFS_SCRIPT = '/home/ubuntu/experiment_scripts/receive_scripts/get_ipfs.py'
SETUP_IPFS_SCRIPT = 'setup_ipfs_local_store.py'
GRAPHS_SCRIPT = '../parse_scripts/transfer_logs.py'

# nodes: csv file read
# region: 'US/WORLD'
# mode: 'UNDER_ATTACK/SHUFFLE'
def exec_exp(nodes, mode_region, exp_type, code_script):
    stdoutfile = exp_type + '_' + mode_region + '.out'
    stderrfile = exp_type + '_' + mode_region + '.err'
    for row in nodes:
        ip = row["publicip"]
        command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ' + key + ' ubuntu@' + ip + ' \"sudo python ' + code_script + ' ' +  src_dir + ' ' + dest_dir + ' ' + str(trial_num) + ' container ' + mode_region + ' ' + exp_type + ' > ' + stdoutfile + ' 2>' + stderrfile + '\"'
        # print command
        os.popen(command)

def dump_images(nodes):
    for row in nodes:
        ip = row["publicip"]
        command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ' + key + ' ubuntu@' + ip + ' \"sudo screen -d -m rm -rf ' + dest_dir + '\"'
        os.popen(command)

def local_store_operation(region, mode, action):
    # command = 'screen -d -m python ' + SETUP_IPFS_SCRIPT + ' ' + region + ' ' + mode + ' ' + action
    command = 'python ' + SETUP_IPFS_SCRIPT + ' ' + region + ' ' + mode + ' ' + action
    os.popen(command)

def generate_graphs():
    command = 'python ' + GRAPHS_SCRIPT
    os.popen(command)

def main():
    num_args = len(sys.argv)
    if num_args != 2:
        print "USAGE: python run_experiments.py <TRIAL_NUM>"
        return
    trial_num = sys.argv[1]
    print 'trial #:' +  trial_num

    us_nodes = []
    world_nodes = []

    with open(SERV_INFO_ATTACK_US, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        us_nodes = list(reader)
    with open(SERV_INFO_ATTACK_WO, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        world_nodes = list(reader)
    
    # print 'running rsync UNDER_ATTACK'            # Under Attack
    # exec_exp(us_nodes, 'UNDER_ATTACK_US', 'rsync', RSYNC_SCRIPT)
    # exec_exp(world_nodes, 'UNDER_ATTACK_world', 'rsync', RSYNC_SCRIPT)
    # time.sleep(1200)            # wait (time in seconds)

    # print 'dumping images after rsync UNDER_ATTACK'
    # dump_images(us_nodes)
    # dump_images(world_nodes)

    # print 'adding images to local store before vmt_ipfs, UNDER_ATTACK'
    # local_store_operation('US', 'UNDER_ATTACK', 'ADD')
    # local_store_operation('WORLD', 'UNDER_ATTACK', 'ADD')
    # time.sleep(600)            # wait (time in seconds)

    print 'running vmt_ipfs, UNDER_ATTACK'
    exec_exp(us_nodes, 'UNDER_ATTACK_US', 'vmt_ipfs', IPFS_SCRIPT)          #- run vmtorrent(ipfs)
    exec_exp(world_nodes, 'UNDER_ATTACK_world', 'vmt_ipfs', IPFS_SCRIPT)          #- run vmtorrent(ipfs)
    time.sleep(1200)           #wait (time in seconds)

    print 'dumping images after vmt_ipfs, UNDER_ATTACK'
    dump_images(us_nodes)
    dump_images(world_nodes)

    print 'deleting images to local store before vmt_ipfs, UNDER_ATTACK'
    local_store_operation('US', 'UNDER_ATTACK', 'DEL')
    local_store_operation('WORLD', 'UNDER_ATTACK', 'DEL')
    
    # SHUFFLE 
    print 'running rsync SHUFFLE'
    exec_exp(us_nodes, 'SHUFFLE_US', 'rsync', RSYNC_SCRIPT)
    exec_exp(world_nodes, 'SHUFFLE_world', 'rsync', RSYNC_SCRIPT)
    time.sleep(1200)            # wait (time in seconds)

    print 'dumping images after rsync SHUFFLE'
    dump_images(us_nodes)
    dump_images(world_nodes)

    print 'adding images to local store before vmt_ipfs, SHUFFLE'
    local_store_operation('US', 'SHUFFLE', 'ADD')
    local_store_operation('WORLD', 'SHUFFLE', 'ADD') 
    time.sleep(600)            # wait (time in seconds)

    print 'running vmt_ipfs, SHUFFLE'
    exec_exp(us_nodes, 'SHUFFLE_US', 'vmt_ipfs', IPFS_SCRIPT)          #- run vmtorrent(ipfs)
    exec_exp(world_nodes, 'SHUFFLE_world', 'vmt_ipfs', IPFS_SCRIPT)          #- run vmtorrent(ipfs)
    time.sleep(1200)           #wait (time in seconds)

    print 'dumping images after vmt_ipfs, SHUFFLE'
    dump_images(us_nodes)
    dump_images(world_nodes)

    print 'deleting images to local store before vmt_ipfs, SHUFFLE'
    local_store_operation('US', 'SHUFFLE', 'DEL')
    local_store_operation('WORLD', 'SHUFFLE', 'DEL')

    print 'generating graphs'
    generate_graphs()

if __name__ == '__main__':
    main()   # Script should have been populated alread using populate_scripts.py and images should have been populated using populate_images.py
