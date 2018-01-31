# container_experiments

Transfer scripts folder to the machines 
python populate_scripts.py <directory>

Transfer images to setup the experiments for rsync, vmtorrent(file)
python populate_images.py 'US' ~/Desktop/images
python populate_images.py 'WORLD' ~/Desktop/images

An additional step is required to setup the experiment for vmtorrent (ipfs):
python setup_ipfs_local_store.py <MODE> <EXPERIMENT> 'ADD'

To clear the local store for vmtorrent (ipfs):
python setup_ipfs_local_store.py <MODE> <EXPERIMENT> 'DEL'
Example: 
python setup_ipfs_local_store.py 'US' 'SHUFFLE' 'DEL'
python setup_ipfs_local_store.py 'WORLD' 'SHUFFLE' 'DEL'

Run rsync, ipfs experiments for US and WORLD topology in 2 modes: Under Attack and Shuffle:
python run_experiments.py <TRIAL_NUM>
python run_experiments.py 1

Transfer logs and generate graphs:
python transfer_logs.py

CLEANUP ALL FILES:
./exec.sh