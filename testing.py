#-*- coding: iso-8859-1 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import basehash
import xml.etree.ElementTree as ET
from spotifyCreds import *
from recs import *
from readWrite import *



###### not sure if being used
def jsonifyDict(dictOfObjects):
    newdict = {}
    for key, item in dictOfObjects.items():
        info = item.__dict__
        newdict[key] = info
    return newdict

def jsonify(item):
    item = item.__dict__
    return song
####################################



def dict_to_objects(dictName, inputtype):
    newDict = {}
    if inputtype == 'songs' or inputtype == 'tracks':
        for key, item in dictName.items():
            newDict[dictName[key]['songID']] = Song(dictName[key])
    elif inputtype == 'playlists':
        for key, item in dictName.items():
            newDict[dictName[key]['id']] = Playlist(dictName[key]['id'],dictName[key]['name'],dictName[key]['uri'],dictName[key]['total'])
    return newDict 






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


#Need to figure out how to make this more efficient

    

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





def playlist_songs(playlist):
    playlistSongs = get_songs_from_playlist(playlist)
    for key,value in playlistSongs.items():
        try:
            print(value['title'] + "(" + value['songID'] + ") -- " + value['artist'] + ":  " + value['artistId'])
        except TypeError:
            print(value.title + "(" + value.songID + ") -- " + value.artist + ":  " + value.artistId)

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





#################################################################


myplaylists = get_items_from_file('playlists.json')
#savedSongs = get_items_from_file('songs.json')
#traktorSongs = get_items_from_file('traktor_songs.json')



