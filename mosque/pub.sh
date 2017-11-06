count=0
while true
do
mosquitto_pub -q 1 -t hello -m world-$count
echo "Publishing... world-$count"
count=$(($count+1))
sleep 0.2

done

