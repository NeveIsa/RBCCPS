index=$1 

cd /mnt/extHD/RAW_SEGREGATED/


mkdir $index
if [ $? -ne 0 ]
then
echo "Folder exists already..."
exit 1
fi

cd $index

sort -t, -nk2 /mnt/extHD/RAW/data/$index -o "$index_sorted"

for device in "screenprinter"
header=$(head -1 $index_sorted) > "$device.csv"
awk "/$device/" $index_sorted >>  "$device.csv"


