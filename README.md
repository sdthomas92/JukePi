# JukePi

This is a music-playing program made for the Raspberry Pi.

## Features
* Plays music in shuffle mode
* Group specific songs together
* Can play music from a removable flash drive
* Keeps the same playlist and currently-playing song if stopped, and resumes when turned back on

## How To Use
1. This is designed to run on a Raspberry Pi with Raspbian installed. I don't know how or if this program will run on other operating systems or machines.<br><br>
2. Change the directory in the program to where you're storing your music
   * Default: ```songPath = "/media/pi/39A2-CB0B" ```
3. Add any additional music formats that the program can recognize
   * Default: ```audioFormats = [".flac", ".mp3", ".wav"] ```
   * I've only tested these three formats, but the program may be able to play other formats too.
4. OPTIONAL: Make a file where your music is stored titled <i>joined_tracks.dat</i>
   * This file stores all the tracks that will play together when shuffled
   * The proper format is shown below:
   ```
   Sgt. Pepper's Lonely Hearts Club Band.flac, With a Little Help from My Friends.flac
   Heartbreaker.flac, Living Loving Maid (She's Just A Woman).flac
   ```
   * The songs in a particular sequence are separated by commas.
   * The song names in this file must match the titles of the songs exactly, including the file type.
   * Sequences are separated by a new line.
