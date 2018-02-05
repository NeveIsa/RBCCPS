require 'sinatra'
require "json"

set :public_folder, File.dirname(__FILE__) + '/static'


get '/' do
  'Put this in your pipe & smoke it!'
end


post '/' do
	puts request.body
  	request.body
end
