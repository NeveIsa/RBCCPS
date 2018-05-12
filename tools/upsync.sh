while true
do
	echo ""
	rsync -arvz -e 'ssh -p 5151' --progress /home/richard/esbackup root@smartcity.rbccps.org:/
	
	if [ $? -eq 0 ]
	then
		echo "SUCCESSFULLY UPLOADED..."
		break
	else
		echo "CONNECTION BROKEN.... RETRYING IN 10s"
		sleep 10
	fi
done


