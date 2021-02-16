import spotipy, os, sys
import pprint
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from classes import *


###This file has the functions to get spotify creds (currently hardcoded)
###also contains a handful of quick methods:
    #features of a song
    #artist info by id
    #gets a list of all user playlists
    #searches for song by name and number of results desired



os.environ['SPOTIPY_CLIENT_ID']= "112e06fb02684d23bb38be7994196e77"
os.environ['SPOTIPY_CLIENT_SECRET']= "882f2ed4564141829088545677551566"
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost'
os.environ['USERNAME']='kwyld4u23'
scope = "user-read-recently-played user-top-read playlist-read-private playlist-read-collaborative"

x=SpotifyOAuth(scope=scope)
token = x.get_authorize_url
client_credentials_manager = SpotifyClientCredentials()
cc = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp = spotipy.Spotify(oauth_manager=x)

def features(songID):
    features = sp.audio_features(songID)
    pprint.pprint(features)

def artist(artistID):
    artist = sp.artist(artistID)
    pprint.pprint(artist)

def get_all_playlists_from_spotify():
    length_of_last = 50
    offset = 0
    all_playlists = {}
    while length_of_last > 0:
        playlists = sp.current_user_playlists(limit=length_of_last,offset=offset)
        offset = offset + length_of_last
        for i, item in enumerate(playlists['items']):
            curPlaylist = Playlist(item['id'],item['name'],item['uri'],item['tracks']['total'])
            all_playlists[item['id']] = curPlaylist.__dict__
        length_of_last = len(playlists['items'])
    return all_playlists

def search_song(name, numResults):
    song = {}
    results = sp.search(q=name, type='track', limit=numResults)
    if numResults == 1:
        features = sp.audio_features(results['tracks']['items'][0]['id'])[0]
        song['title'] = results['tracks']['items'][0]['name']
        if "Remix" in song['title']:
            song['artist'] = results['tracks']['items'][0]['artists'][0]['name']
            song['remixer'] = results['tracks']['items'][0]['artists'][1]['name']
            song['remixerID'] = results['tracks']['items'][0]['artists'][1]['id']
        else:
            song['artist'] = results['tracks']['items'][0]['artists'][0]['name']
        song['songID'] = results['tracks']['items'][0]['id']
        song['artistId'] = results['tracks']['items'][0]['artists'][0]['id']
        song['features'] = features
        song['key'] = features['key']
        song['tempo'] = features['tempo']
        song['mode'] = features['mode']
    return song

