require('yaml')
require('faraday')
require('json')
require('mqtt')
require('awesome_print')
require('time')
require('norikra-client')



trap "SIGINT" do
	puts "Exiting..."
	exit 130
end



conf = File.read('conf.yml')
CONF=YAML.load(conf)




$nkclient = Norikra::Client.new(
    CONF['norikraHost'],
    CONF['norikraRPCPort'],
    connect_timeout: 3, send_timeout: 1, receive_timeout: 3
)



API_URL='http://%s:%s/api/send' % [CONF['norikraHost'],CONF['norikraHTTPPort']]
#API_URL="http://httpbin.org/post"

def post target,data
	if data==[]
		puts "Target: %s | However empty data: %s" % [target,data.to_s]
		return 700,""
	end
	print "\n---> Posting -> %s | status: " % target
	conn = Faraday.new(:url => API_URL)
	result=conn.post do |req|
		req.headers['Content-Type'] = 'application/json'
		req.body = JSON.dump({"target":target, "events":data})
	end
	puts result.status
	return result.status,result.body
end






################### HELPERS ########################

def nkCreateTarget(target)
	puts "\n---> Creating target: %s" % target
	$nkclient.open(target)
end


BUFFER={}
def buffer_insert(k,v)
	if BUFFER.has_key? k
		BUFFER[k] << v
	else
		BUFFER[k]=[v]
		nkCreateTarget(k)
	end
end


def extract_sensor_data(message)
	msg=JSON.load(message)
	devID = msg['deviceid']
	ts = msg['timestamp']
	ts = ts + " UTC"
	msec = (Time.parse(ts).to_f * 1000).to_i
	msg["msecEpoch"] = msec
	#ap msg
	return devID,ts,msg
end


def sort_buffer
	for device in BUFFER.keys
		data = BUFFER[device]
		data=data.sort_by { |x| x["timestamp"]}
		#ap data
	end
end



TIME_DELTA_THRESHOLD = 5 #seconds
def post_buffer
	for device in BUFFER.keys
		# check if data exists for device
		if BUFFER[device].length!=0 

			#puts BUFFER[device][0]['timestamp']
			#return
			
			oldest_entry_ts = BUFFER[device][0]["timestamp"]
			oldest_entry_utc = oldest_entry_ts + " UTC" # provide timezone, else gets converted to system timezone

			oldest_entry_utc = Time.parse oldest_entry_utc

			now = Time.now.getutc # Time.now will also work, the subration is carried out ony after converting both timstamps into UTC
			delta = now - oldest_entry_utc
			print "\r"," "*12,"\r"
			print delta
			if delta > TIME_DELTA_THRESHOLD 
				#puts	
				Thread.new(device,BUFFER[device]) { |dev,data| 
					status,body=post dev,data
					#puts body
				}
				
				BUFFER[device]=[]
			end
		end
	end
end


################### HELPERS ########################

puts "\n---> Subscribing to MQTT topic #{CONF['mqttTopic']}\n"
# Subscribe example
MQTT::Client.connect('localhost') do |c|
  # If you pass a block to the get method, then it will loop
  c.get(CONF['mqttTopic']) do |topic,message|
    #puts "#{topic}: #{message}"
	  
    device,timestamp,msgjson = extract_sensor_data(message)
    #ap msgjson
    buffer_insert(device,msgjson)
    
    sort_buffer
    post_buffer
    
  end
end
