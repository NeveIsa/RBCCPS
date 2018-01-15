
require_relative 'model'
require 'json'
require 'sinatra'


conf=File.open("mosconf.json").read
conf=JSON.parse(conf)
model=Model.new(conf['passwordfile'],conf['aclsfile'])

puts "==========="*7
puts conf
puts "==========="*7

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
