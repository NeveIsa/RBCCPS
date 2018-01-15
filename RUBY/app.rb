
require_relative 'model'
require 'json'
require 'sinatra'


conf=File.open("mosconf.json").read
conf=JSON.parse(conf)
mosquitto_conf_file=conf["mosquitto_conf_file"]

puts "========"*7
puts "MOSQUITTO CONF. FILE: " + mosquitto_conf_file
puts "========"*7

aclsfile=""
passwordfile=""

File.open(mosquitto_conf_file).each do |line|
	if /password_file (.+)/.match(line)
		passwordfile,=/password_file (.+)/.match(line).captures
		#puts passwordfile
	end	
	if /acl_file (.+)/.match(line)
		aclsfile,=/acl_file (.+)/.match(line).captures
		#puts aclsfile
	end
end

if aclsfile=="" or passwordfile==""
	puts "============="
	puts mosquitto_conf_file + " doesn't contain acl_file or password_file entry in it"		
	puts "============="
	exit
end



puts "==========="*7
puts "Found ==> \n #{passwordfile}\n #{aclsfile} \n"
puts "==========="*7


model=Model.new(passwordfile,aclsfile)

get '/' do
	content_type :json
	
	{
		"GET"=>["/users","/acls"],
		"POST"=>["/user/{username}/{password}","/acl/{username}/{topic}/{access(read/write/readwrite)}"],
		"DELETE"=>["/user/{username}","/acls/{username}/{topic}"]
	}.to_json
end

get '/users' do 
	content_type :json
	model.getUsers.to_json
end

post '/user/:username/:password' do |u,p|
	content_type :json
	model.putUser(u,p).to_json	
end

delete '/user/:username' do
	content_type :json
	u=params['username']
	model.delUser(u).to_json
end


get '/acls' do
	content_type :json
	model.getAcls.to_json
end

put '/acl/:username/:topic/:access' do |u,t,a|
	content_type :json
	model.putAcls(u,t,a).to_json
end

delete '/acl/:username/:topic' do |u,t|
	content_type :json
	model.delAcls(u,t).to_json
end
