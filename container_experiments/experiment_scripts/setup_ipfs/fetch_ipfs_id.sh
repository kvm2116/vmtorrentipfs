#!/bin/bash

# install go, ipfs
# Run this from this folder
# ~/vmtorrent/p2pfs/p2p


ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/Downloads/id_rsa ubuntu@$1 "/home/ubuntu/go/bin/ipfs id | grep 'ID' | cut -d' ' -f2 | cut -d',' -f1"
ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i ~/Downloads/id_rsa ubuntu@$1 "/home/ubuntu/go/bin/ipfs id | grep 'ip4/10'"