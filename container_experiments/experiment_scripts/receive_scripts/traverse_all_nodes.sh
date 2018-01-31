KEY="/Users/kunalmahajan/Downloads/id_rsa"
USER="ubuntu"
element=$1

address=$USER@$element
sshcommand="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $KEY $address"
$sshcommand "sudo rm -rf *.out *.err contain* image* log* Q* screen.log"
