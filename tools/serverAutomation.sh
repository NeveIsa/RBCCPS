#MOVING
echo ""
echo "moving from /esbackup to /home/richard/esbackup"
mv /esbackup/* /home/richard/esbackup

# RESTORING
thisDir=$(dirname $(realpath "$0"))

cd "$thisDir/../python/tools"
sudo sh esrestore.sh
INDEX=`cat tempIndex.txt`

echo ""
echo "FOUND INDEX.......... $INDEX"

#WAIT AFTER RESTORE
echo ""
echo "Waiting 30s"
sleep 30



dest="/mnt/extHD/VINYAS_DATA/$INDEX"

#if ls succeeds, means folder arleady present, hence exit.
ls $dest && exit 1

echo ""
echo "Creating folder... $dest"
mkdir $dest

if [ $? -eq 0 ]
then
 echo "Created.."
 rsync -arv /esbackup $dest
 rsync -arv /esbackup $dest
 rsync -arv /esbackup $dest
else
echo "Failed to create folder."
fi


cd /mnt/extHD/RAW/
sh dump.sh $INDEX

echo ""
echo "Completed dowloading RAW DATA"
sleep 10



echo ""
echo "CDing into $thisDir"
cd $thisDir
sleep 2

echo ""
echo "STARTING SEGREGATION..."
sh fragmentation.sh $INDEX
