#!/bin/bash

# install go, ipfs
# Run this from this folder
# ~/vmtorrent/p2pfs/p2p

KEY="/Users/kunalmahajan/Downloads/id_rsa"
IPs="/Users/kunalmahajan/vmtorrent/p2pfs/p2p/dest_ips.txt"
USER="ubuntu"
element=$1

address=$USER@$element
scpaddress="$address:"
sshcommand="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $KEY $address"
scpcommand="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $KEY"

$scpcommand /Users/kunalmahajan/Downloads/go1.9.2.linux-amd64.tar.gz $scpaddress		# copy go and install ipfs
$sshcommand "sudo tar -C /usr/local -xzf go1.9.2.linux-amd64.tar.gz"
$scpcommand /Users/kunalmahajan/Downloads/.profile $scpaddress
$sshcommand "source .profile"
$sshcommand "mkdir /home/ubuntu/go"
$sshcommand "/usr/local/go/bin/go get -u -d github.com/ipfs/go-ipfs"
$sshcommand "sudo apt-get update"
$sshcommand "sudo apt-get install make"
$sshcommand "sudo apt-get install -y gcc"
$sshcommand "source .profile;cd /home/ubuntu/go/src/github.com/ipfs/go-ipfs;make install"
$sshcommand "source .profile;/home/ubuntu/go/bin/ipfs init"
$sshcommand "/home/ubuntu/go/bin/ipfs bootstrap rm --all"
$sshcommand "/home/ubuntu/go/bin/ipfs pin ls --type recursive | cut -d' ' -f1 | xargs -n1 /home/ubuntu/go/bin/ipfs pin rm"
$sshcommand "/home/ubuntu/go/bin/ipfs repo gc"
scpaddress="$address:~/.ipfs/swarm.key"
$scpcommand /Users/kunalmahajan/Downloads/swarm.key $scpaddress

$sshcommand "/home/ubuntu/go/bin/ipfs daemon >log.out 2>error.out &"		# delete all content from ipfs node and remove bootstrap nodes

