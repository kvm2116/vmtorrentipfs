"""
Transfer logs and generate graphs
Run this file from the receive_scripts folder

python transfer_logs.py

"""

import os
import subprocess
import sys
from datetime import datetime
import time
import csv
import shutil
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

# FORMAT OF LOGS : logs/trial1/process_files/UNDER_ATTACK_US/vmt_ipfs172.31.16.126.csv’

SERV_INFO_ATTACK_US = '../server_info/server_ips_UNDER_ATTACK_US.csv'
SERV_INFO_ATTACK_WO = '../server_info/server_ips_UNDER_ATTACK_world.csv'
SERV_INFO_SHUFFLE_US = '../server_info/server_ips_SHUFFLE_US.csv'
SERV_INFO_SHUFFLE_WO = '../server_info/server_ips_SHUFFLE_world.csv'
LOGS_DIR = '/home/ubuntu/logs'
KEY = '~/Downloads/id_rsa'
LOCAL_DIR = '../../'
us_ips = []
world_ips = []
NUM_TRANSFERS = 16

# region : us/world
# mode: ua/shuffle
# type: ipfs/rsync
def plot(rsync_results, ipfs_results, region, mode):
    steps = 1/NUM_TRANSFERS
    ind = np.arange(0,1,steps)  # the x locations for the groups
    r_res = np.array(rsync_results)
    i_res = np.array(ipfs_results)
    # print r_res
    plt.figure()
    plt.plot(ind, r_res)
    plot.plot(ind, i_res)
    plt.legend(['Rsync', 'VMTorrent(dht/ipfs)'], loc='upper left')
    title = region + " " + mode
    fig.suptitle(title)
    plt.xlabel('Time (in seconds)')
    plt.ylabel('Fraction of completed transfers')
    filename = region + '_' + mode + '.png'
    plt.savefig(filename)

def get_end_time(start_time, file, timeslist):
    with open(file, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            timeslist.append(row.get('end time') - start_time)
    return timeslist

def get_start_time(file):
    with open(file, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
             return row.get('start time')

# region : us/world
def create_graphs(iplist, region):
    start_time_ua_ipfs = 0
    start_time_shuffle_ipfs = 0
    start_time_ua_rsync = 0
    start_time_shuffle_rsync = 0
    ua_times_ipfs = []
    shuffle_times_ipfs = []
    ua_times_rsync = []
    shuffle_times_rsync = []

    ip = iplist[0]

    # get start times
    for ip in iplist:
        directory = LOCAL_DIR + ip + '_logs'
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.contains('UNDER_ATTACK') and file.contains('ipfs') and file.contains(ip):
                    start_time_ua_ipfs = get_start_time(file)
                elif file.contains('UNDER_ATTACK') and file.contains('rsync') and file.contains(ip):
                    start_time_ua_rsync = get_start_time(file)
                elif file.contains('SHUFFLE') and file.contains('ipfs') and file.contains(ip):
                    start_time_shuffle_ipfs = get_start_time(file)
                elif file.contains('SHUFFLE') and file.contains('rsync') and file.contains(ip):
                    start_time_shuffle_rsync = get_start_time(file)
    
    # get all times
    for ip in iplist:
        directory = LOCAL_DIR + ip + '_logs'
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.contains('UNDER_ATTACK') and file.contains('ipfs'):
                    ua_times_ipfs = get_end_time(start_time_ua_ipfs, file, ua_times_ipfs)
                elif file.contains('UNDER_ATTACK') and file.contains('rsync'):
                    ua_times_rsync = get_end_time(start_time_ua_rsync, file, ua_times_rsync)
                elif file.contains('SHUFFLE') and file.contains('ipfs'):
                    shuffle_times_ipfs = get_end_time(start_time_shuffle_ipfs, file, shuffle_times_ipfs)
                elif file.contains('SHUFFLE') and file.contains('rsync'):
                    shuffle_times_rsync= get_end_time(start_time_shuffle_rsync, file, shuffle_times_rsync)
    plot(ua_times_rsync, ua_times_ipfs, region, 'Under Attack:')
    plot(shuffle_times_rsync, shuffle_times_ipfs, region, 'Shuffle:')

def getIPlist():
    ips = []
    with open(SERV_INFO_SHUFFLE_US, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        ips = [row.get('publicip') for row in reader]
        us_ips = ips

    with open(SERV_INFO_SHUFFLE_WO, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ips.append(row.get('publicip'))
            world_ips.append(row.get('publicip'))
    return ips

def main():
    num_args = len(sys.argv)
    if num_args != 1:
        print "USAGE: python transfer_logs.py"
        return
    iplist = getIPlist()

    for i in range(len(iplist)):
        address = 'ubuntu@' + ip[i] + ':' + LOGS_DIR
        directory= LOCAL_DIR + ip[i] + '_logs'
        subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, '-r', address, directory])
    
    create_graphs(us_ips, 'US')
    create_graphs(world_ips, 'WORLD') 

if __name__ == '__main__':
    main()
