echo "ls"
ssh root@smartcity.rbccps.org -p 5151 ls /esbackup
echo "rm"
ssh root@smartcity.rbccps.org -p 5151 rm -rf /esbackup

#echo "mkdir"
#ssh root@smartcity.rbccps.org -p 5151 mkdir /esbackup

echo "ls"
ssh root@smartcity.rbccps.org -p 5151 ls esback*/ -R


rsync -arvz -e 'ssh -p 5151' --progress /home/richard/esbackup root@smartcity.rbccps.org:/

