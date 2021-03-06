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


def removeAllQueries
	$nkclient.queries.each { |q|
		qname = q['name']
		puts "Removing Query: %s" % qname
		$nkclient.deregister(qname)

	}
end

### JUST FOR TEST ###

def registerCountQuery
	$nkclient.targets.each { |dev|
		devname = dev['name']
		queryID=devname + "_Q"
		query= "select data.temperature * data.temperature from %s.win:time_batch(5 sec,\"FORCE_UPDATE, START_EAGER\")" % devname
		puts "Registering query: %s | %s" % [queryID,query]
		$nkclient.register(queryID,nil,query)
	}
end

### JUST FOR TEST ###

def registerYAMLQueries(filename)
	rawyaml = File.read(filename)
	queries = YAML.load(rawyaml)

	queries.each { |queryhash|
		queryhash.each { |qname,query| 
			puts "%s => %s" % [qname,query]
			$nkclient.register(qname,nil,query)
		}
	}
end

removeAllQueries

if ARGV.length!=0
	#registerCountQuery
	registerYAMLQueries ARGV[0]
end
