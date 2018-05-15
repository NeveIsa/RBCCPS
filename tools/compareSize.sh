sizeServer=$(ssh -p 5151 richard@smartcity.rbccps.org du -s /esbackup | awk '{ print $1 }')
sizeLocal=$(du -s /home/richard/esbackup)
echo $sizeServer 
echo $sizeLocal
