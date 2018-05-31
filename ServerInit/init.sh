sudo yum install python-pip python-dev

sudo pip install requests
sudo pip install es2csv


wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.4.rpm
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.4.rpm.sha512
shasum -a 512 -c elasticsearch-6.2.4.rpm.sha512
sudo rpm --install elasticsearch-6.2.4.rpm
