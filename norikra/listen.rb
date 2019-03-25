require('norikra-client')
require('yaml')

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
		puts $nkclient.event(q).to_s
	}
end
