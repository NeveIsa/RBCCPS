### This is MUSCLE - A Mosquitto ACL control interface over HTTP REST.


#### Requirements - Ruby and Sinatra

#### Steps to get Muscle running
---

* Install Ruby on your system
* Install Sinatra using `gem install sinatra`
* Configure the authentication parameters by editing the file `muscleconf.json`
* Run the server using `ruby app.rb`

* Go to the link http://localhost:9292 to check everything is working and for the info on how to consume the API
	
#### GET	
* 0	"/users"
* 1	"/acls"
#### POST	
* 0	"/user/{username}/{password}"
* 1	"/acl/{username}/{topic}/{access(read/write/readwrite)}"
DELETE	
* 0	"/user/{username}"
* 1	"/acls/{username}/{topic}"
#### PUT	
* 0	"/sighup"


