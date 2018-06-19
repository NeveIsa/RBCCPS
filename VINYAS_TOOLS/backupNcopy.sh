
INDX=$1
SRC="/home/richard/esbackup"
DST="/mnt/vinyasExtHD/JuneVisit/$INDX"

cd ../python/tools
sudo python esbackup.py $INDX

mkdir $DST
rsync -arv --progress $SRC $DST


