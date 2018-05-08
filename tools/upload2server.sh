echo "ls"
ssh root@smartcity.rbccps.org -p 5151 ls /esbackup
echo "rm"
ssh root@smartcity.rbccps.org -p 5151 rm -rf /esbackup

#echo "mkdir"
#ssh root@smartcity.rbccps.org -p 5151 mkdir /esbackup

echo "ls"
ssh root@smartcity.rbccps.org -p 5151 ls esbackup/ -R

while true
do
	rsync -arvz -e 'ssh -p 5151' --progress /home/richard/esbackup root@smartcity.rbccps.org:/
	
	if [ $? -eq 0]
	then
		break
	fi
done
