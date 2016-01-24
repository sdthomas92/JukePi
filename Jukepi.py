#---------------------------------------------------------
# IMPORTS
#---------------------------------------------------------

from sys import argv

import filecmp
import os
from os import path
import pygame.mixer
from pygame.mixer import music
import random
import shutil
import time

#---------------------------------------------------------
# INITIALIZATIONS / EVENT CREATION
#---------------------------------------------------------

pygame.init()
pygame.mixer.init()
SONG_END = pygame.USEREVENT + 1
music.set_endevent(SONG_END)

#---------------------------------------------------------
# CONSTANTS
#---------------------------------------------------------

#The path where all of the songs are located (USB stick)
songPath = "/media/pi/39A2-CB0B"

#The file name that contains which track of the playlist
#that is currently playing
currentSong = "current_song.dat"

#The file name that contains the current shuffled track
currentShuffledList = "current_shuffled_list.dat"

#The file name that contains any joined songs, along with
#another identical file to check for any file changes
joinedTracks = "joined_tracks.dat"
joinedTracksCopy = "joined_tracks_COPY.dat"

#The file that contains the master list of songs. If the
#program starts and the song list is altered, the shuffled
#songs list is regenerated with the new list
masterList = "master_list.dat"

#A list of accepted song formats (what works with the
#program is not limited to all the formats in this list).
audioFormats = [".flac", ".mp3", ".wav"]

#---------------------------------------------------------
# FUNCTIONS
#---------------------------------------------------------

#Checks if the input file is a playable song.
def isSong(inputFile):
    for i in audioFormats:
        if inputFile.endswith(i):
            return True
    return False

#Compares the contents of two lists, order being disregarded.
def compareTwoLists(list1, list2):
    if len(list1) != len(list2):
        return False
    for i in list1:
        if i not in list2:
            return False
    return True

#Given a song directory, this method returns the song title.
def getSongNameFromDirectoryName(song):
    result = song.split('/')
    return result[len(result)-1]

#Checks if the given song is inside the "joined_tracks" file
def isSongInJoinedList(song):
    if not os.path.isfile(songPath + "/" + joinedTracks):
        return False
    result = []
    with open(songPath + "/" + joinedTracks) as f:
        for x in f:
            list = x.split(',')
            for i in list:
                result.append(i.strip())
    f.close()
    if song in result:
        return True
    return False

#Given a song in the "joined_tracks" file, this method
#returns the list of songs that the song was found in.
def findSongInJoinedSongsList(song):
    if not os.path.isfile(songPath + "/" + joinedTracks):
        return False
    with open(songPath + "/" + joinedTracks) as f:
        for x in f:
            result = []
            list = x.split(',')
            for i in list:
                result.append(i.strip())
            if song in result:
                f.close()
                return result
    f.close()
    return False

#Writes the given list to the "master_list" file
def listToFile(inputList):
    if os.path.isfile(masterList):
        os.remove(masterList)
    masterListFile = open(masterList, 'w')
    for x in inputList:
        masterListFile.write(x + "\n")
    masterListFile.close()
        
#Writes the contents of the given file to a list
def fileToList(inputFile):
    if not os.path.isfile(inputFile):
        return False
    result = []
    with open(inputFile) as f:
        for x in f:
            result.append(x.rstrip('\n'))
    f.close()
    return result

#Generates a list of songs from the song directory
def getList():
    songList = []
    for file in os.listdir(songPath):
        if isSong(file):
            songList.append(songPath + "/" + file)
    return songList

#Randomizes the list of songs in the given list. If any
#songs are meant to be joined together (in the
#"joined_tracks" file), those songs are put in the given
#order.
def randomizedList(list):
    if os.path.isfile(currentSong):
        os.remove(currentSong)
    currentShuffledListFile = open(currentShuffledList, 'w')
    newList = []
    y = len(list)
    for i in range(0, y):
        if list:
            song = random.choice(list)
        else:
            break

        if isSongInJoinedList(getSongNameFromDirectoryName(song)):
            joinedList = findSongInJoinedSongsList(getSongNameFromDirectoryName(song))
            for j in range(0, len(joinedList)):
                if songPath + "/" + joinedList[j] in list:
                    currentShuffledListFile.write(songPath + "/" + joinedList[j] + "\n")
                    newList.append(songPath + "/" + joinedList[j])
                    list.remove(songPath + "/" + joinedList[j])
                    y = y - 1
        else:
            currentShuffledListFile.write(song + "\n")
            newList.append(song)
            list.remove(song)
            y = y - 1
    currentShuffledListFile.close()
    return newList

#---------------------------------------------------------   
# MAIN PROGRAM
#---------------------------------------------------------

#The program pauses for five seconds before running. If the
#songs are stored on a flash drive and the program runs
#right after booting up, it's possible the flash drive won't be
#discoverable. Adding 5 seconds before looking in the directory
#ensures the flash drive is discoverable at that point.
time.sleep(5)
orderedList = getList()

#Checks if there is a master list of songs. This is used to
#check for any alterations to the song list have been made.
if os.path.isfile(masterList):
    if compareTwoLists(orderedList, fileToList(masterList)) == False:
        if os.path.isfile(currentShuffledList):
            os.remove(currentShuffledList)
        if os.path.isfile(currentSong):
            os.remove(currentSong)
        listToFile(orderedList)
else:
    listToFile(orderedList)

#Checks if there is a joined tracks list. If there is, a
#copy is either made or checked for any changes. If there are
#changes, the saved playlist and current song files are
#deleted.
if os.path.isfile(songPath + "/" + joinedTracks):
    if os.path.isfile(songPath + "/" + joinedTracksCopy):
        if not filecmp.cmp(songPath + "/" + joinedTracks, songPath + "/" + joinedTracksCopy):
            if os.path.isfile(currentShuffledList):
                os.remove(currentShuffledList)
            if os.path.isfile(currentSong):
                os.remove(currentSong)
            shutil.copy(songPath + "/" + joinedTracks, songPath + "/" + joinedTracksCopy)
    else:
        shutil.copy(songPath + "/" + joinedTracks, songPath + "/" + joinedTracksCopy)

    

while True:
    songList = []
    #Checks if a randomized playlist is already made. If there's one
    #already made, the song list is generated from it.
    if os.path.isfile(currentShuffledList):
        currentShuffledListFile = open(currentShuffledList, 'r')
        for line in currentShuffledListFile:
            songList.append(line.rstrip('\n'))
        currentShuffledListFile.close()
    else:
        songList = randomizedList(list(orderedList))

    start = 0
    #Checks the last played position of the randomized list.
    if os.path.isfile(currentSong):
        if os.path.getsize(currentSong) > 0:
            currentSongFile = open(currentSong, 'r')
            start = int(currentSongFile.read())
            currentSongFile.close()
        else:
            songList = randomizedList(list(orderedList))

    #Plays every song in the song list from the starting position.
    for x in range(start, len(songList)):
        music.load(songList[x])
        music.play()
        print("Now playing: " + getSongNameFromDirectoryName(songList[x]))
        switchSong = True

        #Writes the new position to the current song file.
        if os.path.isfile(currentSong):
            os.remove(currentSong)
        currentSongFile = open(currentSong, 'wb')
        currentSongFile.write(str(x))
        currentSongFile.close()

        #Breaks out of this loop when the song ends to play the
        #next song.
        while switchSong:
            for event in pygame.event.get():
                if event.type == SONG_END:
                    switchSong = False
                    
    #After every song in the playlist is played, the song position
    #file and playlist file are deleted so that a new list can be
    #made
    if os.path.isfile(currentSong):
        os.remove(currentSong)
    if os.path.isfile(currentShuffledList):
        os.remove(currentShuffledList)
