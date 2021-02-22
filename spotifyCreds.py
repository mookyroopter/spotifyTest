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
scope = "user-read-recently-played user-top-read playlist-read-private playlist-read-collaborative user-read-currently-playing playlist-modify-private user-read-playback-state user-modify-playback-state"

x=SpotifyOAuth(scope=scope)
token = x.get_authorize_url
client_credentials_manager = SpotifyClientCredentials()
cc = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp = spotipy.Spotify(oauth_manager=x)

#gets info for a specific song ID
def features(songID):
    features = sp.audio_features(songID)
    pprint.pprint(features)

#gets info for a specific artist ID
def artist(artistID):
    artist = sp.artist(artistID)
    pprint.pprint(artist)

#returns all playlists as a dictionary
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

#returns a song based on title and artist - searches for songs with 10 results then matches artist
def search_song(name, inputartist):
    songDict = {}
    output = {}
    results = sp.search(q=name, type='track', limit=10)
    for key in results['tracks']['items']:
        song = create_song_fields(key)
        song = Song(song)
        songDict[song.songID] = song
    for key, item in songDict.items():
        if item.artist == inputartist:
            output[key] = item
            return output
        else:
            print ("artist not found")
        #for key in results['tracks']['items']:
        #    pprint.pprint(key['name'])
        #    pprint.pprint(key['artists'][0]['name'])


#returns a Dict of a given song (formatted for objectification)
def create_song_fields(songDict):
    song = {}
    try: 
        song['songID'] = songDict['id']
        song['title'] = songDict['name']
        if "Remix" in song['title']:
            song['artist'] = songDict['artists'][0]['name']
            song['remixer'] = songDict['artists'][1]['name']
            song['remixerID'] = songDict['artists'][1]['id']
        else:
            song['artist'] = songDict['artists'][0]['name']
        features = sp.audio_features(songDict['id'])[0]
        song['artistId'] = songDict['artists'][0]['id']
        song['features'] = features
        song['key'] = features['key']
        song['tempo'] = features['tempo']
        song['mode'] = features['mode']
    except KeyError:
        song['songID'] = songDict['item']['id']
        song['title'] = songDict['item']['name']
        if "Remix" in song['title']:
            song['artist'] = songDict['item']['artists'][0]['name']
            song['remixer'] = songDict['item']['artists'][1]['name']
            song['remixerID'] = songDict['item']['artists'][1]['id']
        else:
            song['artist'] = songDict['item']['artists'][0]['name']
        features = sp.audio_features(songDict['item']['id'])[0]
        song['artistId'] = songDict['item']['artists'][0]['id']
        song['features'] = features
        song['key'] = features['key']
        song['tempo'] = features['tempo']
        song['mode'] = features['mode']
    return song
