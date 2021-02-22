#-*- coding: iso-8859-1 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import basehash

from spotifyCreds import *
from recs import *
from readWrite import *

NoneType = type(None)
myplaylists = get_items_from_file('playlists.json')

###### not sure if being used
def jsonifyDict(dictOfObjects):
    newdict = {}
    for key, item in dictOfObjects.items():
        info = item.__dict__
        newdict[key] = info
    return newdict

#Refreshes all playlist lengths - USE AFTER FINDING DIFFERENCES
def update_playlists():
    myplaylists = get_all_playlists_from_spotify()
    with open ('playlists.json', 'w') as outfile:
        json.dump(myplaylists, outfile, indent=4)
####################################


####THIS SEEMS GOOD FOR MANUAL CONVERSIONS#####
def dict_to_objects(dictName, inputtype):
    newDict = {}
    if inputtype == 'songs' or inputtype == 'tracks':
        for key, item in dictName.items():
            try:
                newDict[dictName[key]['songID']] = Song(dictName[key])
            except:
                # tempID = hash(dictName[key]['title'] + dictName[key]['artist'])
                newDict[key] = Song(dictName[key])
    elif inputtype == 'playlists':
        for key, item in dictName.items():
            newDict[dictName[key]['id']] = Playlist(dictName[key]['id'],dictName[key]['name'],dictName[key]['uri'],dictName[key]['total'])
    return newDict 

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


#Finds all playlists of a certain length
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
        
#Creates a list of the lengths of all playlists
def all_playlists_lengths(playlistDict):
    output = []
    for key, item in playlistDict.items():
        output.append(item['total'])
    output.sort()
    return output


#savedSongs = get_items_from_file('songs.json')
#traktorSongs = get_items_from_file('traktor_songs.json')

#returns the currently playing song as a Song object
def currently_playing_to_song():
    test = sp.currently_playing()
    song = create_song_fields(test)
    song = Song(song)
    return song

#adds comments as value on song object
def add_comments(songDict, songId, comments):
    songDict[songId].comments = [comments]





