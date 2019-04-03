pkill screen

echo "Starting norikra..."
./norikra_start.sh
sleep 2
screen -ls

echo "Starting fakesensor..."
cd ../python
screen -dmS fakesensor python fakesensor.py
sleep 2
cd ../norikra
screen -ls

sleep 10

echo "Starting mqtt2norikra..."
screen -dmS mqtt2norikra ruby mqtt2norikra.rb
sleep 2
screen -ls

echo "Registering queries..."
ruby registerQueries.rb ok

echo "Listening..."
ruby listen.rb

