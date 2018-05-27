server=10.156.14.143


curl $server/dataLNK/ > .temp
cat .temp | grep -Po "helloworld-\d+-\d+-\d+" | sort -u 


echo ""


if [ "$1" = "" ]
then
echo "Pass a filename to download"
else
wget $server/dataLNK/$1
fi

rm .temp
