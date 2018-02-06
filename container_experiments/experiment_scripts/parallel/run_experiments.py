""""

Run rsync, ipfs experiments for US and WORLD topology in 2 modes: Under Attack and Shuffle
python run_experiments.py <TRIAL_NUM> <EXP_START_TIME> <EXP_DATE>
python run_experiments.py 1 17:00  1/31 
Note: date is month/day
Time Zone is assumed to be EST for running script
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
key = '../key/aws_keys/id_rsa'
trial_num = 3


def oregon(str_hr):
    if int(str_hr) < 3:
        return str(int(str_hr) + 21)
    elif int(str_hr) >= 3 :
        return str(int(str_hr) - 3)
        


def main():
    num_args = len(sys.argv)
    if num_args != 4:
        print "USAGE: python run_experiments.py <TRIAL_NUM> <EXP_START_TIME> <EXP_DATE>"
        return
    trial_num = sys.argv[1]
    exp_start_time = sys.argv[2]
    exp_date = sys.argv[3]
    print 'trial #:' +  trial_num
    print 'experiment start time:' + exp_start_time
    split_time = exp_start_time.split(":")
    str_hr = split_time[0]
    str_min = split_time[1]
    print 'experiment date:' + exp_date
    split_date = exp_date.split("/")
    str_month = split_time[0]
    str_day = split_time[1]
    
    us_nodes = []
    
    with open(SERV_INFO_SHUFFLE_US, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        us_nodes = list(reader)
    
    for row in us_nodes:
        ip = row['publicip']
        get_image1 = row["GETIMAGE1"]
        get_image2 = row["GETIMAGE2"]
        location = row["zone"]
        # handle time zone difference since script run from EST
        if location == 'Oregon':
            oregon(str_hr)
            
        # setup cron for first image
        command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ' + key + ' ubuntu@' + ip + ' \"' + str_min + ' ' + str_hr + ' ' + str_day + ' ' + str_month + ' * ' + '/home/ubuntu/experiment_scripts/parallel/job.py ' + trial_num + ' ' + get_image1
        os.popen(command)
        # setup cron for second image
        command = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ' + key + ' ubuntu@' + ip + ' \"' + str_min + ' ' + str_hr + ' ' + str_day + ' ' + str_month + ' * ' + '/home/ubuntu/experiment_scripts/parallel/job.py ' + trial_num + ' ' + get_image2
        os.popen(command)

if __name__ == '__main__':
    main()   
