import subprocess as sp
import os
import glob

'''
TODO :
- Make sure the timings are correctly merged
- Make sure the range of the clip is the right one
- Do something to properly tell the user how many timings there are for the
current video and which timings is currently processed
- Use the same settings as EzLogging, maybe create another file that handles
    the config and call it in both scripts?
- Make a variable containing the video format instead of blindly guessing it's
    mp4
'''

'''
Dependencies
FFMPEG : https://ffmpeg.org/download.html
'''
# Temporary until I have handled settings change this depending on your configuration.

# Windows
# FFMPEG_BIN = "C:/Program Files/ffmpeg-20160522-git-566be4f-win64-static/bin/ffmpeg.exe"
# sourceFolder = "D:/Videos/__Youtube/__Rushes_to_sort/test/"

# Linux
FFMPEG_BIN = "/usr/bin/ffmpeg"
sourceFolder = "/home/muream/Videos/test/"

# In seconds
fps = 30
before = 20
after = 10


def convert_time(timing):
    '''
    Converts the timing in seconds
    :param timing: the timing with a format hh:mm:ss
    :return: time in seconds
    '''
    hour = int(timing[0:2])
    minute = int(timing[3:5])
    second = int(timing[6:8])
    hour = hour*60*60
    minute = minute*60
    second = second
    seconds = hour+minute+second
    return seconds


def get_range(seconds, before, after):
    '''
    Gets the range of the clip
    :param seconds: the timing in seconds
    :param before: number of seconds before the timing
    :param after: number of seconds after the timing
    :return: the range in a list
    '''
    start = seconds - before
    if start < 0:
        start = 0
    end = seconds + after
    length = end - start
    clipRange = {'Start': start,'End': end,'Length': length}
    return clipRange


def get_timings(textFile):
    '''
    Puts the content of a textfile in a list
    :param textFile: path to the text file
    :param line: line to read
    :return: list of all the timings
    '''
    f = open(textFile, 'r')
    lines = f.readlines()
    timings = []
    for line in lines:
        line = line[:-1]
        seconds = convert_time(line)
        timings.append(seconds)
    return timings


def export_clip(filename, start, length, targetname):
    '''
    :param filename: path to the original file
    :param start: start of the clip
    :param end: end of the clip
    :param targetname: path to the exported file
    '''
    command  = ["ffmpeg",
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

'''
def can_merge(timings, currentIndex, after):
    \'''
    checks if the timing can be merged (not if they should)
    need to know if:
    - we are at the last timing
    -
    \'''
    # Do some work here
    if currentIndex + 1 == len(timings):
        lastTiming = True
    else:
        lastTiming = False
'''

def clip_informations(timings, currentIndex, after):
    # Compares current timing to the next one, if they are to close : Merges them and extends the range
    currentTiming = timings[currentIndex]

    if currentIndex + 1 == len(timings):
        lastTiming = True
        difference = 0
        extended = False
    else:
        lastTiming = False
    # Merge timings until two are to far appart or if there's nothing to merge
    while lastTiming is False:
        currentTiming = timings[currentIndex]
        nextTiming = timings[currentIndex + 1]
        difference = nextTiming - currentTiming
        if difference <= after:
            # merge the timings here
            afterTemp = after + difference  # used to add some time to the range if timings are too close to each other
            del nextTiming  # remove the merged timing so that it's not processed twice
            clipRange = get_range(currentTiming, before, afterTemp)
            extended = True
        else:
            # break the loop here
            extended = False
            break

        currentIndex += 1
    clipRange = get_range(currentTiming, before, after)
    start = clipRange['Start']
    end = clipRange['End']
    length = clipRange['Length']
    clipInfo = {'Difference': difference, 'Extended': extended, 'Start': start, 'End': end, 'Length': length, 'Last Timer': lastTiming}
    return clipInfo


def Main():
    # Creates the "Derush" Folder
    exportPath = sourceFolder + "Derush"
    if not os.path.exists(exportPath):
        os.makedirs(exportPath)

    # Loops through all the video files in said folder
    videoFiles = glob.glob(sourceFolder+"*.mp4")
    for videoFile in videoFiles:
        currentFile = videoFiles.index(videoFile) + 1
        numberOfFiles = len(videoFiles)
        name = os.path.basename(videoFile.rsplit('.', 1)[0])  # Gets the name of the file
        textFile = sourceFolder+name+".txt"
        timings = get_timings(textFile)
        #Loops through all the timings for the Video file
        for timing in timings:
            currentIndex = timings.index(timing)
            numberOfTimings = len(timings)
            print "Processing file " + str(currentFile) + "/" + str(numberOfFiles)
            print "Processing Timing " + str(currentIndex+1) + "/" + str(numberOfTimings)
            print "Timing: " + str(timing) +"s"
            # Compares current timing to the next one, if they are to close : Merges them and extends the range
            clipInfo = clip_informations(timings, currentIndex, after)

            print "Seconds until next Timing : %is" % clipInfo['Difference']

            if clipInfo['Last Timer'] == False:
                if clipInfo['Extended'] == True:
                    print "The clip has been extended by %is" % clipInfo['Difference']
                else:
                    print "The clip has not been extended"
            else:
                print "This is the last timing"

            print "Clip Start: " + str(clipInfo['Start']) + "s"
            print "Clip End: " + str(clipInfo['End']) + "s"
            print "Clip Duration: " + str(clipInfo['Length']) + "s"

            print "\n"
            # clip = export_clip(videoFile, clipInfo['Start'], clipInfo['Length'], exportPath+"/%s_Clip_%s.mp4" % (name, str(currentTiming+1).zfill(2)))

Main()
