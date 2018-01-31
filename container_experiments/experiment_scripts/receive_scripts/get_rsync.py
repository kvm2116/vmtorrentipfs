import os
import subprocess
import sys
from datetime import datetime
import time
import csv

USERNAME = "ubuntu"
IP_LIST = '/home/ubuntu/experiment_scripts/server_info/server_ips_' + sys.argv[5] + '.csv'
KEY = '/home/ubuntu/experiment_scripts/key/aws_keys/id_rsa'
LOG_SCREEN = '/home/ubuntu/screen.log'
csvtemp = []

def write_list_to_file(fd, imagelist):
    for item in imagelist:
        fd.write(item)
        fd.write(', ')

def main():
    num_args = len(sys.argv)
    if num_args != 7:
        print "USAGE: python get_rsync.py <SRC_DIR> <DST_DIR> <TRIAL_NUM> <FILE_TYPE> <EXP_TYPE> <SCRIPT_TYPE>"
        return
    fd = open(LOG_SCREEN, 'w')

    # for grabbing the private ip of node so only receive files from other nodes.
    f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    private_ip=f.read().strip('\n')
    
    src_directory= sys.argv[1]
    dst_directory = sys.argv[2]
    trial_num = 'trial' +sys.argv[3]
    file_type = sys.argv[4]
    exp_type = sys.argv[5]
    script_type = sys.argv[6]
    fd.write('Parsed arguments\n')
    log_dir_path = '/home/ubuntu/logs/' + trial_num + '/' + file_type + '/' + exp_type + '/'
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)
        fd.write('Creating LOG directory\n')
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)
        fd.write('Creating IMAGES directory\n')

    with open(log_dir_path + exp_type + script_type + private_ip + '.csv', 'a+') as csvwritefile:
        fieldnames = ['trial#','from nodename', 'image','from ip','datestamp','start time', 'end time']
        writer = csv.DictWriter(csvwritefile, delimiter=',',lineterminator='\n', fieldnames=fieldnames)
        writer.writeheader()

    with open(IP_LIST, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        nodes = list(reader)
       
        for row in nodes:
            ip = row["privateip"]
            now = datetime.now()
            if private_ip == ip:
                if 'SHUFFLE' in exp_type:               # in SHUFFLE need to pull 2 files from other servers based on csv file
                    get_image1 = row["GETIMAGE1"]
                    get_image2 = row["GETIMAGE2"]
                    get_image_list = [get_image1, get_image2]
                    fd.write('starting Shuffle\n')
                    for get_image in get_image_list:
                        csvtemp.append(trial_num)       # for writing to csv file   
                        for line in nodes:
                            if (get_image == line["image1"]):
                                csvtemp.append(line["nodename"])
                                csvtemp.append(line["image1"])
                                csvtemp.append(line["privateip"])
                                csvtemp.append(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                                pub_ip = line["publicip"]
                                get_files(pub_ip, src_directory, dst_directory, csvtemp, get_image, private_ip, log_dir_path, script_type) 
                            elif (get_image == line["image2"]):
                                csvtemp.append(line["nodename"])
                                csvtemp.append(line["image2"])
                                csvtemp.append(line["privateip"])
                                csvtemp.append(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                                pub_ip = line["publicip"]
                                get_files(pub_ip, src_directory, dst_directory, csvtemp, get_image, private_ip, log_dir_path, script_type) 
                elif 'UNDER_ATTACK' in exp_type:        # in UNDER_ATACK need to push 4 files to other servers based on csv file
                    get_image1 = row["GETIMAGE1"]
                    get_image2 = row["GETIMAGE2"]
                    get_image3 = row["GETIMAGE3"]
                    get_image4 = row["GETIMAGE4"]
                    get_image_list = [get_image1, get_image2, get_image3, get_image4]
                    write_list_to_file(fd, get_image_list)
                    for get_image in get_image_list:
                        if get_image:
                            csvtemp.append(trial_num)       # for writing to csv file
                            fd.write('starting UA\n')
                            for line in nodes:
                                if (get_image == line["image1"]):
                                    csvtemp.append(line["nodename"])
                                    csvtemp.append(line["image1"])
                                    csvtemp.append(line["privateip"])
                                    csvtemp.append(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                                    pub_ip = line["publicip"]
                                    get_files(pub_ip, src_directory, dst_directory, csvtemp, get_image, private_ip, log_dir_path, script_type) 
                                elif (get_image == line["image2"]):
                                    csvtemp.append(line["nodename"])
                                    csvtemp.append(line["image2"])
                                    csvtemp.append(line["privateip"])
                                    csvtemp.append(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                                    pub_ip = line["publicip"]
                                    get_files(pub_ip, src_directory, dst_directory, csvtemp, get_image, private_ip, log_dir_path, script_type)  
                                elif (get_image == line["image3"]):
                                    csvtemp.append(line["nodename"])
                                    csvtemp.append(line["image3"])
                                    csvtemp.append(line["privateip"])
                                    csvtemp.append(now.strftime("%Y-%m-%d %H:%M:%S.%f"))
                                    pub_ip = line["publicip"]
                                    get_files(pub_ip, src_directory, dst_directory, csvtemp, get_image, private_ip, log_dir_path, script_type) 
                                elif (get_image == line["image4"]):
                                    csvtemp.append(line["nodename"])
                                    csvtemp.append(line["image4"])
                                    csvtemp.append(line["privateip"])
                                    csvtemp.append(now.strftime("%Y-%m-%d %H:%M:%S.%f")) 
                                    pub_ip = line["publicip"]
                                    get_files(pub_ip, src_directory, dst_directory, csvtemp, get_image, private_ip, log_dir_path, script_type)
    fd.close()

def get_files(ip, src_directory, dst_directory, csvtemp, image, private_ip, log_dir_path, script_type):
    address = USERNAME+'@'+ip+':'+src_directory+image
    command = "rsync -avzhe \"ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i " + KEY + "\" " + address + " " + dst_directory 
    start_time = time.time()
    os.popen(command)   
    end_time = time.time()
    exp_type = sys.argv[5]

    with open(log_dir_path + exp_type + script_type + private_ip + '.csv', 'a+') as csvwritefile:
        fieldnames = ['trial#','from nodename', 'image','from ip', 'datestamp','start time', 'end time']
        writer = csv.DictWriter(csvwritefile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
        writer.writerow({'trial#': csvtemp[0],'from nodename': csvtemp[1],
                         'image': csvtemp[2],'from ip': csvtemp[3],
                         'datestamp': csvtemp[4],
                         'start time': start_time, 'end time': end_time})
        del csvtemp[:]
                 
if __name__ == "__main__":
   main()
