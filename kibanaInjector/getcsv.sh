
#query is present in the 'queryfile' file

#indexPattern in $1

echo ------
echo ------

echo INDEX_PATTERN ---> $1
echo QUERY ---> `cat queryfile`

echo ------
echo ------

#run es2csv 
../bin/es2csv -i $1 -r -q @queryfile -o static/output.csv

#wait for user input
read xxx

