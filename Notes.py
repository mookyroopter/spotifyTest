#1. Reorganize Spotify Playlists - Need to figure out parameters
#2. Make Spotify playlist out of DJ set/Traktor Playlist - Currently no writing to Spotify
#3. Get recommendations based on music of a criteria - Hardcoded - write function to update values
#4. Generate Playlists based on criteria (smart playlists in traktor)
#5. Create Playlist of DJ Library
    #5a. Compare Traktor library to spotify playlists
        #find songs with matching artist
        #find songs with matching song title
#6. Get recommendations based on averages from playlist
#7. Make real-time notes on songs, to add to traktor info


#IN TRAKTOR NML
#Rating = Comment 2 = Free text
#KEY_LYRICS in INFO = Free Text
#CATALOG_NO = Free Text - Use for Traktor Song ID - Check for this on import


#Ranking = stars increases by 51 each time (1=51, 2=102, 3=153, etc)
#nmltest = root[2].findall('./ENTRY/[@ARTIST]') --- Gets list of all items with an artist
#           root[2].findall('./ENTRY/INFO[@KEY]')  --- List of all items with a Key

#Traktor import - Rather than calling out fields individually, import as Dict for what exists, excluding if needed

#Ideas:
    #Spotify Song ID in field for quick lookup
    #Playlist ID in field for quick creation
    #dict in field for both?
    #update tags in comment


#things to address:
    #search_song only finds match on exact song name
    #DONE ---#add artist to function pull a list of (#?) of songs and match artist
    #DONE ---#search_song will print these with more than 1 given --- Default to 10 and match artist

#Functions to build
    #Check if spotify song exists in traktor (Title, artist, bpm) --- Reading NML Files (see notes above)
    #Average features from playlist 
    #Group songs - Genres, BPM, InTraktor, 
    #check if new playlist or playlist was updated
    #Get Genre from Traktor and apply to Spotify version
    #get common song tags - diplay **This will be way later**

#When pulling songs from spotify, check if song exists before adding.  If it does, just add playlist it's on 


#Get currently playing song, and write notes to track
#add those notes to Rating Field in NML