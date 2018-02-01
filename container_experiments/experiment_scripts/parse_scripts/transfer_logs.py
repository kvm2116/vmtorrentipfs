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

SERV_INFO_ATTACK_US = '../server_info/server_ips_UNDER_ATTACK_US.csv'
SERV_INFO_ATTACK_WO = '../server_info/server_ips_UNDER_ATTACK_world.csv'
SERV_INFO_SHUFFLE_US = '../server_info/server_ips_SHUFFLE_US.csv'
SERV_INFO_SHUFFLE_WO = '../server_info/server_ips_SHUFFLE_world.csv'
LOGS_DIR = '/home/ubuntu/logs'
KEY = '~/Downloads/id_rsa'
LOCAL_DIR = '../../'
NUM_TRANSFERS = 16

# region : us/world
# mode: ua/shuffle
# type: ipfs/rsync
def plot(rsync_results, ipfs_results, region, mode):
    # steps = 1.0/NUM_TRANSFERS
    # ind = np.arange(0,1,steps)  # the x locations for the groups
    ind = np.linspace(0.0625,1,NUM_TRANSFERS)
    # print len(ind)
    # print len(rsync_results)
    # print len(ipfs_results)
    r_res = np.array(rsync_results)
    i_res = np.array(ipfs_results)
    # print r_res
    fig = plt.figure()
    plt.plot(r_res, ind, marker='o')
    plt.plot(i_res, ind, marker='s')
    plt.legend(['Rsync', 'VMTorrent(dht/ipfs)'], loc='upper left')
    # plt.legend(['VMTorrent(dht/ipfs)', 'Rsync'], loc='upper left')
    title = region + " " + mode
    fig.suptitle(title)
    plt.xlabel('Time (in seconds)')
    plt.ylabel('Fraction of completed transfers')
    filename = region + '_' + mode + '.png'
    plt.savefig(filename)

def get_end_time(start_time, file, timeslist):
    with open(file, 'rU') as csvfile:
        end_time = 0
        reader = csv.DictReader(csvfile)
        for row in reader:
            end_time = row.get('end time')
            print end_time
            timeslist.append(float(end_time) - float(start_time))
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

    ip_ua = iplist[4]
    ip_shuffle = iplist[0]
    # get start times
    for ip in iplist:
        directory = LOCAL_DIR + ip + '_logs'
        for path, dirs, files in os.walk(directory):
            for file in files:
                fullpath = os.path.join(path, file)
                if 'UNDER_ATTACK' in file and 'ipfs' in file and ip_ua in file:
                    start_time_ua_ipfs = get_start_time(fullpath)
                elif 'UNDER_ATTACK' in file and 'rsync' in file and ip_ua in file:
                    start_time_ua_rsync = get_start_time(fullpath)
                elif 'SHUFFLE' in file and 'ipfs' in file and ip_shuffle in file:
                    start_time_shuffle_ipfs = get_start_time(fullpath)
                elif 'SHUFFLE' in file and 'rsync' in file and ip_shuffle in file:
                    start_time_shuffle_rsync = get_start_time(fullpath)
    
    # get all times
    for ip in iplist:
        directory = LOCAL_DIR + ip + '_logs'
        for path, dirs, files in os.walk(directory):
            for file in files:
                print file
                fullpath = os.path.join(path, file)
                if 'UNDER_ATTACK' in file and 'ipfs' in file:
                    ua_times_ipfs = get_end_time(start_time_ua_ipfs, fullpath, ua_times_ipfs)
                elif 'UNDER_ATTACK' in file and 'rsync' in file:
                    ua_times_rsync = get_end_time(start_time_ua_rsync, fullpath, ua_times_rsync)
                elif 'SHUFFLE' in file and 'ipfs' in file:
                    shuffle_times_ipfs = get_end_time(start_time_shuffle_ipfs, fullpath, shuffle_times_ipfs)
                elif 'SHUFFLE' in file and 'rsync' in file:
                    shuffle_times_rsync= get_end_time(start_time_shuffle_rsync, fullpath, shuffle_times_rsync)
    plot(ua_times_rsync, ua_times_ipfs, region, 'Under Attack')
    plot(shuffle_times_rsync, shuffle_times_ipfs, region, 'Shuffle')

def getIPlist():
    ips = []
    us_ips = []
    world_ips = []

    with open(SERV_INFO_SHUFFLE_US, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ips.append(row.get('publicip'))
            us_ips.append(row.get('privateip'))

    with open(SERV_INFO_SHUFFLE_WO, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ips.append(row.get('publicip'))
            world_ips.append(row.get('privateip'))
    return us_ips, world_ips, ips

def main():
    num_args = len(sys.argv)
    if num_args != 1:
        print "USAGE: python transfer_logs.py"
        return
    us_ips, world_ips, iplist = getIPlist()

    for i in range(len(iplist)):
        address = 'ubuntu@' + iplist[i] + ':' + LOGS_DIR
        directory = ''
        if i > 7:
            directory = LOCAL_DIR + world_ips[i-8] + '_logs'
        else:
            directory = LOCAL_DIR + us_ips[i] + '_logs'
        # subprocess.call(['scp', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no','-i', KEY, '-r', address, directory])
        command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + address + " " + directory 
        os.popen(command) 

    create_graphs(us_ips, 'US')
    create_graphs(world_ips, 'WORLD') 

if __name__ == '__main__':
    main()
