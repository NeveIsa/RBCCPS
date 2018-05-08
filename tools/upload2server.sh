
. yesterdayIndex.sh

cd ../python/tools
python esbackup.py $LASTINDEX 

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
	echo ""
	rsync -arvz -e 'ssh -p 5151' --progress /home/richard/esbackup root@smartcity.rbccps.org:/
	
	if [ $? -eq 0]
	then
		echo "SUCCESSFULLY UPLOADED..."
		break
	else
		echo "CONNECTION BROKEN.... RETRYING IN 10s"
		sleep 10
	fi
done


echo ""
echo "CALLING SERVER AUTOMATION... in 10s"
sleep 10

ssh root@smartcity.rbccps.org -p 5151 sh /home/richard/Desktop/rbc/RBCCPS/tools/serverAutomation.sh

