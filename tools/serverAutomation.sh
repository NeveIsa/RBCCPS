
# RESTORING
#cd ../python/tools
#sudo sh esrestore.sh


#WAIT AFTER RESTORE
#sleep 30


DATE=`date +%Y-%b-%d`
dest="/mnt/extHD/VINYAS_DATA/$DATE"

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

