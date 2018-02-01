#!/bin/bash

# script to recursively travel a dir and create docker images 
# save the docker images in /images/local

dirlist=$(find $1 -mindepth 1 -maxdepth 1 -type d)
i=1
path="/images/local/"

for dir in $dirlist
do
	echo $i
	sudo docker stop $(sudo docker ps -a -q)
	sudo docker rm $(sudo docker ps -a -q)
	sudo docker rmi $(sudo docker images -a -q)
	echo $dir
	cd $dir
	OUTPUT="$(sudo docker build . | tail -n 1)"
	stringarray=($OUTPUT)
	arraylen=${#ArrayName[@]}
	imageid="${stringarray[2]}"
	imagepath=$path$i
	sudo docker save -o $imagepath $imageid
	i=$(($i+1))
	cd ..
done
