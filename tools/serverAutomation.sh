
# RESTORING
cd ../python/tools
sudo sh esrestore.sh
INDEX=`cat tempIndex.txt`

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
else
echo "Failed to create folder."
fi


cd /mnt/extHD/RAW/
sh dump.sh $INDEX
