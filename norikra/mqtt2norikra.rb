require('yaml')


conf = File.read('conf.yml')
CONF=YAML.load(conf)

API_URL='http://%s:%s/api/send' % [CONF['norikraHost'],CONF['norikraPort']]

def post url,data
	
end


post 1,2
