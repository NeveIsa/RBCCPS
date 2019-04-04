require('norikra-client')
require('yaml')
require('time')

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


def getAllQueryNames
	qnames=[]
	$nkclient.queries.each do |q|
		qnames << q['name']
	end
	return qnames
end


queries= getAllQueryNames

while true
	sleep 1
	queries.each { |q|
		events = $nkclient.event(q)
		events.each { |e|
			ts,namedevent = e[0],e[1]
			if namedevent["LOADER_EVENT"]
				puts "%s - %s" % [Time.at(ts),namedevent]
			end
		}
		
	}
end
