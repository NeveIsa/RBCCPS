require 'sinatra'
require "json"

set :public_folder, File.dirname(__FILE__) + '/static'


get '/' do
	headers "Access-Control-Allow-Origin"=>"*"
  	"You shouldn't be here, get lost."
end

post '/:indexPattern' do
	headers "Access-Control-Allow-Origin"=>"*"
	
	query=request.body.read
  	query=query.split.join

  	indexPattern=params["indexPattern"]
  	
  	puts indexPattern
  	puts query

  	File.open("queryfile", 'w') { |file| file.write(query) }

  	Dir.chdir(Dir.pwd){
		cmd="xterm -e sh getcsv.sh #{indexPattern}"

		puts cmd
	  	system(cmd)

	}
  	
	request.body.rewind
  	request.body


	

end
