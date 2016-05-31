
import subprocess as sp
import os
import glob
from Config import set_config


# TODO Do something to properly tell the user how many timings there are
# for the current video and which timings is currently processed

'''
Dependencies
FFMPEG : https://ffmpeg.org/download.html
'''
# TODO Use the same settings as EzLogging, maybe create another script that
# handles the config and call it in both scripts?

# Windows
FFMPEG_BIN = "C:/Program Files/ffmpeg-20160522-git-566be4f-win64-static/bin/ffmpeg.exe"
sourceFolder = "D:/Videos/__Youtube/__Rushes_to_sort/test/"

# Linux
# FFMPEG_BIN = "/usr/bin/ffmpeg"
# sourceFolder = "/home/muream/Videos/test/"

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
    hour = hour * 60 * 60
    minute = minute * 60
    second = second
    seconds = hour + minute + second
    return seconds


def get_range(seconds, before, after):
    # TODO Make sure the range of the clip is the right one
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
    clipRange = {'Start': start, 'End': end, 'Length': length}
    return clipRange


def get_timings(textFile, videoFile):
    '''
    Puts the content of a textfile in a list
    :param textFile: path to the text file
    :param videoFile: path to the videoFile
    :param line: line to read
    :return: list of all the timings
    '''
    try:
        f = open(textFile, 'r')
    except:
        print 'There is no associated text file, moving the video in a "NoTextFile" directory so that you can take a look'
        noTextFile = sourceFolder + "NoTextFile"
        sort_files(videoFile, noTextFile)
        timings = []
        return timings
    lines = f.readlines()
    timings = []
    for line in lines:
        line = line[:-1]
        seconds = convert_time(line)
        timings.append(seconds)
    return timings


def sort_files(fileToSort, destination):
    basename = os.path.basename(fileToSort)
    if not os.path.exists(destination):
        os.makedirs(destination)
    destination = destination + "/" + basename
    os.rename(fileToSort, destination)



def export_clip(filename, start, length, targetname):
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
    FNULL = open(os.devnull, 'w')
    p = sp.Popen(command,
                 #shell=True,
                 stdin=sp.PIPE,
                 stdout=sp.PIPE)
    output = p.communicate('S\nL\n')[0]
    #print output

def is_last_timing(currentIndex, timings):
    if currentIndex + 1 == len(timings):
        lastTiming = True
        difference = 0
        extended = False
    else:
        lastTiming = False
    return lastTiming


def clip_informations(timings, currentIndex, after):
    # TODO Make sure the timings are correctly merged
    # Compares current timing to the next one, if they are to close : Merges
    # them and extends the range
    currentTiming = timings[currentIndex]
    lastTiming = is_last_timing(currentIndex,timings)
    difference = None
    extended = None
    # Merge timings until two are to far appart or if there's nothing to merge
    while lastTiming is False:

        currentTiming = timings[currentIndex]
        nextTiming = timings[currentIndex + 1]
        difference = nextTiming - currentTiming
        if difference <= before + after:
            # merge the timings here
            # used to add some time to the range if timings are too close to
            # each other
            afterTemp = after + difference
            del nextTiming  # remove the merged timing so that it's not processed twice
            clipRange = get_range(currentTiming, before, afterTemp)
            extended = True
        else:
            # break the loop here
            extended = False
            break

        currentIndex += 1
        lastTiming = is_last_timing(currentIndex,timings)
    clipRange = get_range(currentTiming, before, after)
    start = clipRange['Start']
    end = clipRange['End']
    length = clipRange['Length']
    clipInfo = {'Difference': difference, 'Extended': extended,
                'Start': start, 'End': end, 'Length': length,
                'Last Timer': lastTiming, 'Current Index': currentIndex + 1}

    return clipInfo


def main():
    # Creates the "Derush" Folder
    exportPath = sourceFolder + "Derush"
    if not os.path.exists(exportPath):
        os.makedirs(exportPath)

    # Loops through all the video files in said folder
    videoFiles = glob.glob(sourceFolder + "*.mp4")
    for videoFile in videoFiles:
        currentFile = videoFiles.index(videoFile) + 1
        numberOfFiles = len(videoFiles)
        # Gets the name of the file
        name = os.path.basename(videoFile.rsplit('.', 1)[0])
        textFile = sourceFolder + name + ".txt"
        timings = get_timings(textFile, videoFile)
        print "----------------------"
        print "Processing file " + str(currentFile) + "/" + str(numberOfFiles)
        print name
        print "\n"
        # Loops through all the timings for the Video file
        for timing in timings:
            currentIndex = timings.index(timing)
            numberOfTimings = len(timings)
            print "Processing Timing " + str(currentIndex + 1) + "/" + str(numberOfTimings)
            print "Timing: " + str(timing) + "s"
            # Compares current timing to the next one, if they are to close :
            # Merges them and extends the range
            clipInfo = clip_informations(timings, currentIndex, after)

            if clipInfo['Last Timer'] == False:
                print "Seconds until next Timing : %is" % clipInfo['Difference']
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
            #clip = export_clip(videoFile, clipInfo['Start'], clipInfo[
            #                   'Length'], exportPath + "/%s_Clip_%s.mp4" % (name, str(clipInfo['Current Index']).zfill(2)))

main()
