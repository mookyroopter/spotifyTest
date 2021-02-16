#-*- coding: iso-8859-1 -*-
import pandas as pd
import spotipy, os, sys, json
import pprint
import matplotlib.pyplot as plt
import numpy as np
import basehash
import xml.etree.ElementTree as ET
#import simplejson as json
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


os.environ['SPOTIPY_CLIENT_ID']= "112e06fb02684d23bb38be7994196e77"
os.environ['SPOTIPY_CLIENT_SECRET']= "882f2ed4564141829088545677551566"
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost'
os.environ['USERNAME']='kwyld4u23'
scope = "user-read-recently-played user-top-read playlist-read-private playlist-read-collaborative"

#sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="YOUR_APP_CLIENT_ID",client_secret="YOUR_APP_CLIENT_SECRET"))
x=SpotifyOAuth(scope=scope)
token = x.get_authorize_url
client_credentials_manager = SpotifyClientCredentials()
cc = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp = spotipy.Spotify(oauth_manager=x)
hash_fn = basehash.base62()

class Playlist:
    def __init__(self, id, name, uri, total):
        self.id = id
        self.name = name
        self.uri = uri
        self.total = total
        songs = {}

class Song:
    def __init__(self, dictionary):
        self.spotifyPlaylists = []
        if str(type(dictionary)) == "<class 'str'>":
            dictionary = json.loads(dictionary)
        for key in dictionary.keys():
            setattr(self, key, dictionary[key])
    def extract_features(self):
        self.key = self.features['key']
        self.tempo = self.features['tempo']
        self.mode = self.features['mode']

def jsonifyDict(dictOfObjects):
    newdict = {}
    for key, item in dictOfObjects.items():
        info = item.__dict__
        newdict[key] = info
    return newdict

def jsonify(song):
    song = song.__dict__
    return song


current_songs = {}
def get_songs_from_playlist(playlist):
    print('getting songs from playlist: ' + playlist)
    all_songs = {}
    playlist_songs = sp.playlist_items(playlist,fields="items.track.id,total,tracks,uri",additional_types=['track'])
    total_songs = playlist_songs['total']
    if total_songs >= 50:
        length_of_last = 50
        offset = 0
        while length_of_last == 50:
            song_list = []
            partial_songs = sp.playlist_items(playlist, limit=length_of_last, offset=offset, fields="items.track.id,total,tracs,uri",additional_types=['track'])
            this_segement_length = len(partial_songs['items'])
            for i, item in enumerate(partial_songs['items']):
                if item['track'] == None:
                    print("NoneType")
                else:
                    song_list.append(item['track']['id']) 
            trackInfo = sp.tracks(song_list)
            for num, item in enumerate(trackInfo['tracks']):
                songDict = {}
                songDict = {'title': item['name'], 'artist': item['artists'][0]['name'], 'songID': item['id'], 'artistId': item['artists'][0]['id']}
                songDict['popularity'] = item['popularity']
                songDict['features'] = sp.audio_features(item['id'])[0]
                curSong = Song(songDict)
                curSong.spotifyPlaylists.append(playlist)
                curSong.extract_features()
                all_songs[item['id']] = curSong
            offset = offset + length_of_last
            if this_segement_length <= 50:
                length_of_last = 0
            else:
                length_of_last = 50
    else:
        song_list = []
        for i, item in enumerate(playlist_songs['items']):
            if item['track'] == None:
                print("NoneType")
            else:
                song_list.append(item['track']['id']) 
        trackInfo = sp.tracks(song_list)
        for num, item in enumerate(trackInfo['tracks']):
            songDict = {}
            songDict = {'title': item['name'], 'artist': item['artists'][0]['name'], 'songID': item['id'], 'artistId': item['artists'][0]['id']}
            songDict['popularity'] = item['popularity']
            songDict['features'] = sp.audio_features(item['id'])[0]
            curSong = Song(songDict)
            curSong.spotifyPlaylists.append(playlist)
            curSong.extract_features()
            all_songs[item['id']] = curSong               
    return all_songs
        

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

def dict_to_objects(dictName, inputtype):
    newDict = {}
    if inputtype == 'songs' or inputtype == 'tracks':
        for key, item in dictName.items():
            newDict[dictName[key]['songID']] = Song(dictName[key])
    elif inputtype == 'playlists':
        for key, item in dictName.items():
            newDict[dictName[key]['id']] = Playlist(dictName[key]['id'],dictName[key]['name'],dictName[key]['uri'],dictName[key]['total'])
    return newDict 


def get_items_from_file(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file, object_hook=dict)
    return data

def object_to_dict(item):
    item = item.__dict__
    return item

def write_songs(songs, file):
    new_output = {}
    for key, item in songs.items():
        if isinstance(item, Song):
            new_output[key] = jsonify(item) 
        if isinstance(item, dict):
            new_output[key] = item
    with open (file, 'w') as outfile:
        json.dump(new_output,outfile,indent=4)

def check_for_updates(playlistFile, spotifyPlaylists):
    playlists_to_update = []
    for key,item in playlistFile.items():
        if key in spotifyPlaylists and spotifyPlaylists[key]['total'] == playlistFile[key].total:
            print("same")
        else:
            playlists_to_update.append(key)
    return playlists_to_update


def update_playlists():
    myplaylists = get_all_playlists_from_spotify()
    with open ('playlists.json', 'w') as outfile:
        json.dump(myplaylists, outfile, indent=4)



########Returns all playlists in playlists.json id, name, uri, total
def get_playlists_from_file(playlistFile):
    myplaylists = get_items_from_file('playlists.json')
    playlistDict = {}
    for key, value in myplaylists.items():
        playlistDict[value['id']] = Playlist(value['id'], value['name'], value['uri'], value['total'])
    return playlistDict

#Need to figure out how to make this more efficient
def refresh_songs_from_spotify(input):
    try:
        current_songs = get_items_from_file('songs.json')
    except:
        current_songs = {}
    current_playlists = get_playlists_from_file('playlists.json')
    myplaylists = get_all_playlists_from_spotify()
    if input == "reset":
        num = 0
        for playlistID in myplaylists:
            print (playlistID + ":  " + str(myplaylists[playlistID]['total']) + " tracks")
            songs_to_write = get_songs_from_playlist(playlistID)
            for songID, values in songs_to_write.items():
                if songID in current_songs:
                    if playlistID in values.spotifyPlaylists:
                        pass
                    else:
                        current_songs[songID]['spotifyPlaylists'].append(playlistID)
                else:
                    current_songs[songID] = songs_to_write[songID] 
            num += 1
            if num % 10 == 0:
                write_songs(current_songs, 'songs.json')         
        write_songs(current_songs, 'songs.json')
    elif input == "all":
        playlists_to_update = check_for_updates(current_playlists, myplaylists)
        for playlistID in playlists_to_update:
            print (playlistID + ":  " + str(current_playlists[playlistID].total) + " tracks")
            songs_to_write = get_songs_from_playlist(playlistID)
            for songID,values in songs_to_write.items():
                if songID in current_songs:
                    if playlistID in current_songs[songID]['spotifyPlaylists']:
                        print ("already exists")
                    else:
                        current_songs[songID]['spotifyPlaylists'].append(playlistID)
                else:
                    current_songs[songID] = songs_to_write[songID]
        write_songs(current_songs, 'songs.json')
    elif type(input) == list:
        for item in input:
            songs_to_write = get_songs_from_playlist(item)
            for songID,values in songs_to_write.items():
                if songID in current_songs:
                    try:
                        if item in current_songs[songID]['spotifyPlaylists']:
                            print ("already exists")
                        else:
                            current_songs[songID]['spotifyPlaylists'].append(item)
                    except TypeError:
                        if item in current_songs[songID].spotifyPlaylists:
                            print("already exists")
                        else:
                            current_songs[songID].spotifyPlaylists.append(item)
                else:
                    current_songs[songID] = songs_to_write[songID]
        write_songs(current_songs, 'songs.json')
        
        print ("it's a list!")
    else:
        print("Not sure what's happening")

    

####USUALLY WILL HAVE THIS UNCOMMENTED TO AUTO GET PLAYLISTS    
#myplaylists = get_playlists_from_file('playlists.json')



######Getting songs from a file with specific features
def get_songs_with_params(songlist, **kwargs):
    all_songs = get_items_from_file(songlist)
    checkParams = {}
    for key, value in kwargs.items(): 
        checkParams[key] = value
    song_output = {}
    for key, song in all_songs.items():
        if song['features']['valence'] <= 0.2 and song['features']['energy'] >= checkParams['energy'] and song['features']['danceability'] >= checkParams['danceability']:
            song_output[song['songID']] = Song(song['title'],song['artist'],song['songID'],song['artistId'])
            song_output[song['songID']].features = song['features']
            song_output[song['songID']].playlists = song['playlists'] 
    return song_output



 #####RECOMMENDATIONS###### 
#song_selection = get_songs_with_params('songs.json', energy=0.7, danceability=0.7)
#for i, song in song_selection.items():
#    print(song.artist + ": " + song.title + "(" + i + "):  Playlist = " + str(myplaylists[song.playlists[0]].name) + " and Dance = " + str(song.features['danceability']))


##SETS VARIABLES FOR RECOMMENDATIONS ---- #############################
#artists = ["spotify:artist:7GZGpDZcYVX1wrbaOoDWOH","spotify:artist:04jj7dljPI0ixtNsz2pXWK"]
genres = ['tech-house', 'bass-house','techno']
#genres: 'techno' 'deep-house' 'detroit-techno' 'chicago-house' 'dance' 'house' 'bass house' 
#'microhouse' 'deep groove house' 'tech house' 'uk tech house' 'tech-house' 'minimal-techno'
songs = ['1NuESUfZC4PMUwW81tqWsu','5Jvvh8MN1joJjxFxfMWpSN']
minnrg = 0.78
targnrg = 0.88
mindance = 0.685
targdance = 0.8
minstrument = 0.77
targstrument = 0.9
maxval = 0.65
targval = 0.03
maxtempo = 140
targtempo = 127
targmode = 0
maxpop = 5
songCount = 50
checkCount = 0
def get_recs(*kwargs):
    #seed_artists=artists    ===  Add artists to recommendation seeds
    recs = cc.recommendations(seed_genres=genres,seed_tracks=songs,limit=songCount,min_energy=minnrg, target_energy=targnrg, mim_danceability=mindance, target_danceability=targdance, min_instrumentalness=minstrument,target_instrumentalness=targstrument, max_valence=maxval, target_valence=targval, max_popularity=maxpop, target_time_signature=4,max_tempo=maxtempo, target_tempo=targtempo, target_mode=targmode)
    print (minnrg)
    i = 0
    for key in recs['tracks']:
        print (key['name']+ " --" + key['artists'][0]['name'] + " (songID: " + key['id'] + "  |  artistID: " + key['artists'][0]['id'])
        i += 1


############################################################
#####
#Song Name, info, BPM, Album are all separate
#Can I put into list, and then associate them? 



############################################################

### from Spotify
def features(songID):
    features = sp.audio_features(songID)
    pprint.pprint(features)

def artist(artistID):
    artist = sp.artist(artistID)
    pprint.pprint(artist)

def playlist_songs(playlist):
    playlistSongs = get_songs_from_playlist(playlist)
    for key,value in playlistSongs.items():
         print(value['title'] + "(" + value['songID'] + ") -- " + value['artist'] + ":  " + value['artistId'])
        #test ID = get_songs_from_playlist("1VKxmwEM7134yZGpE3speX")

def playlists_by_length(length=1, operation="="):
    output = []
    all_playlists = get_items_from_file('playlists.json')
    
    if operation == "=":  
        for key, item in all_playlists.items():
            if item['total'] == length:
                output.append(item['id'])
    elif operation == ">":
        for key, item in all_playlists.items():
            if item['total'] >= length:
                output.append(item['id'])
    elif operation == "<":
        for key, item in all_playlists.items():
            if item['total'] <= length:
                output.append(item['id'])
    elif operation == 'between':
        for key, item in all_playlists.items():
            if item['total'] >= length[0] and item['total'] <= length[1]:
                output.append(item['id'])
    else:
        print ('uh oh')
    return output
        




#### - From dict
def print_all_playlists(playlistDict):
    for key, value in playlistDict.items():
        print(value.name + ":  " + value.id)

def get_playlist_id(playlistName, playlistDict):
    output = "None"
    for key, value in playlistDict.items():
        if value.name == playlistName:
            output = value.id
    print (output)


#################################################################


myplaylists = get_items_from_file('playlists.json')
#savedSongs = get_items_from_file('songs.json')
#traktorSongs = get_items_from_file('traktor_songs.json')



