
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
../bin/es2csv -i $1 -r -q @queryfile -o static/output.csv

echo   
echo ---------------------------------------------------------------------
echo "Results are stored @ $pwd/static/output.csv"
echo ---------------------------------------------------------------------
echo   

#wait for user input
#read xxx

sleep 3

