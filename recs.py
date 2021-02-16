from spotifyCreds import *



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