
#query is present in the 'queryfile' file

#indexPattern in $1
echo ----------------------------------------------------------------------

echo INDEX_PATTERN --- 
echo $1
echo QUERY --- 
cat queryfile

echo   
echo ---------------------------------------------------------------------
echo   

#run es2csv 
../bin/es2csv -i $1 -r -q @queryfile -o static/output.csv -u http://$2:9200

echo   
echo ---------------------------------------------------------------------
echo "Results are stored @ $pwd/static/output.csv"
echo ---------------------------------------------------------------------
echo   

#wait for user input
#read xxx

sleep 7

