'''
require "uri"
require "net/http"

url = URI("https://accounts.spotify.com/api/token")

https = Net::HTTP.new(url.host, url.port)
https.use_ssl = true

request = Net::HTTP::Post.new(url)
request["Authorization"] = "Basic MTEyZTA2ZmIwMjY4NGQyM2JiMzhiZTc5OTQxOTZlNzc6ODgyZjJlZDQ1NjQxNDE4MjkwODg1NDU2Nzc1NTE1NjY="
request["Content-Type"] = "application/x-www-form-urlencoded"
request["Cookie"] = "__Host-device_id=AQC_jNYXGevONt1x9q4en70B5Q3tkpPu2jcCVbY9WyOoaajfISZg922setFWjxATPZ1ErCMcUFPepG0I9l_V6ZT8iPRA921_2Xg"
request.body = "grant_type=client_credentials"

response = https.request(request)
puts response.read_body

{"access_token":"BQDYrc1eZZDoe5YeKO4aKs06g091R000m0aM9EMKeW3293dsjiZIgLRcqY3rsFoRhILaB0pNuLI6fItLwDI","token_type":"Bearer","expires_in":3600,"scope":""}
'''
require 'rspotify'
require 'rspotify/oauth'

client_id = "112e06fb02684d23bb38be7994196e77"
client_secret = "882f2ed4564141829088545677551566"
RSpotify.authenticate(client_id, client_secret)
Rails.application.config.middleware.use OmniAuth::Builder do
    provider :spotify, client_id, client_secret, scope: 'user-read-recently-played user-top-read playlist-read-private playlist-read-collaborative'
  end
me = RSpotify::User.find('kylewilliams')
puts me.playlists #=> (Playlist array)