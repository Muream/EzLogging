'''
TODO :
- Make sure the timers are correctly merged
- Make sure the range of the clip is the right one
- Do something to properly tell the user how many timers there are for the current video and which timers is currently processed
- Use the same settings as EzLogging, maybe create another file that handles the config and call it in both scripts?
- Make a variable containing the video format instead of blindly guessing it's mp4
'''

'''
Dependencies
FFMPEG : https://ffmpeg.org/download.html

'''

import subprocess as sp
import os
import glob

#Temporary until I have handled settings change this depending on your configuration.

#Windows
#FFMPEG_BIN = "C:/Program Files/ffmpeg-20160522-git-566be4f-win64-static/bin/ffmpeg.exe"
#sourceFolder = "D:/Videos/__Youtube/__Rushes_to_sort/test/"

#linux
FFMPEG_BIN = "/usr/bin/ffmpeg"
sourceFolder = "/home/muream/Videos/test/"

# In seconds
fps = 30
before = 20
after = 10

def ConvertTime(timer):
    '''
    Converts the timer in seconds
    :param timer: the timer with a format hh:mm:ss
    :return: time in seconds
    '''
    hour = int(timer[0:2])
    minute = int(timer[3:5])
    second = int(timer[6:8])
    hour = hour*60*60
    minute = minute*60
    second = second
    seconds = hour+minute+second
    return seconds

def GetRange(seconds, before, after):
    '''
    Gets the range of the clip
    :param seconds: the timer in seconds
    :param before: number of seconds before the timer
    :param after: number of seconds after the timer
    :return: the range in a list
    '''
    start = seconds - before
    if start < 0:
        start = 0
    end = seconds + after
    length = end - start
    clipRange = [start, end, length]
    return clipRange

def GetTimings(textFile):
    '''
    Puts the content of a textfile in a list
    :param textFile: path to the text file
    :param line: line to read
    :return: list of all the timings
    '''
    f = open(textFile, 'r')
    lines = f.readlines()
    timers = []
    for line in lines:
        line = line[:-1]
        seconds = ConvertTime(line)
        timers.append(seconds)
        #print timers
    return timers

def ExportClip(filename, start, length, targetname):
    '''
    :param filename: path to the original file
    :param start: start of the clip
    :param end: end of the clip
    :param targetname: path to the exported file
    '''
    command = ["ffmpeg",
            "-i", filename,
            "-map", "0:0",
            "-map", "0:1",
            "-map", "0:2",
            "-map", "0:3",
            "-map", "0:4",
            "-ss", "%0.2f" % start,
            "-t", "%0.2f" % length,
            "-codec", "copy",
            targetname]

    p = sp.Popen(command,
                 stdin=sp.PIPE,
                 stdout=sp.PIPE)
    output = p.communicate('S\nL\n')[0]
    print output



def Main():
    #Creates the "Derush" Folder
    exportPath = sourceFolder+"Derush"
    if not os.path.exists(exportPath):
        os.makedirs(exportPath)

    #loops through all the video files in said folder
    videoFiles = glob.glob(sourceFolder+"*.mp4")
    for videoFile in videoFiles:
        currentFile = videoFiles.index(videoFile) + 1
        numberOfFiles = len(videoFiles)
        name = os.path.basename(videoFile.rsplit('.',1)[0]) #Gets the name of the file
        textFile = sourceFolder+name+".txt"
        timers = GetTimings(textFile)
        #Loops through all the timers for the Video file
        for timing in timers:
            afterTemp = after
            currentTimer = timers.index(timing)
            numberOfTimers = len(timers)
            print "Processing file " + str(currentFile) + "/" + str(numberOfFiles)
            print "Processing Timer " + str(currentTimer+1) + "/" + str(numberOfTimers)
           
            
            print "Timer: " + str(timing) +"s"
            #Compares current timer to the next one, if they are to close : Merges them and extends the range
            while True and currentTimer < len(timers)-1:
                difference = timers[currentTimer+1] - timers[currentTimer]
                print "Time until next timer = %is" % difference
                if difference <= after:
                    #merge the timers here
                    afterTemp = after + difference # used to add some time to the range if timers are too close to each other
                    del timers[currentTimer+1] #remove the merged timer so that it's not processed twice
                    print "Extended by %is" % difference
                else:
                    #break the loop here
                    print "Not extended"
                    break #should be stopping the loop (maybe it is working and the for loop makes the while restart where it was)
                print "\n"
                currentTimer += 1
            if afterTemp > after:
                clipRange = GetRange(timing, before, afterTemp)
            else:
                clipRange = GetRange(timing, before, after)
            start = clipRange[0]
            end = clipRange[1]
            length = clipRange[2]
            print "Start: " + str(start) +"s"
            print "End: " + str(end) +"s"
            print "Length: " + str(length) +"s"
            print "\n"
            clip = ExportClip(videoFile, start, length, exportPath+"/%s_Clip_%s.mp4" % (name, str(currentTimer+1).zfill(2)))

Main()
