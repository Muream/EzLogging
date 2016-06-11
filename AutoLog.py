import subprocess as sp
import os
import glob
from Config import Settings

# TRASH: give some indication of how many merges there have been for each Clip
# maybe in the name of the file?

mySettings = Settings()
mySettings.set_config()
mySettings.read_config()


class Clip:

    def __init__(self, timing, originalFile):

        self.timing = timing
        self.path = None
        self.originalFile = originalFile
        self.timingSeconds = None
        self.start = None
        self.end = None
        self.length = None

    def timing_to_seconds(self):
        '''
        Converts the hh:mm:ss format in seconds
        '''
        hour = int(self.timing[0:2])
        minute = int(self.timing[3:5])
        second = int(self.timing[6:8])
        hour = hour * 60 * 60
        minute = minute * 60
        timingSeconds = second
        self.timingSeconds = hour + minute + second

    def get_range(self):
        # #DONE:0 Make sure the range of the clip is the right one
        '''
        Gets the range of the clip
        '''
        self.start = self.timingSeconds - mySettings.cutBefore
        if self.start < 0:
            self.start = 0
        self.end = self.timingSeconds + mySettings.cutAfter
        self.length = self.end - self.start

    def should_merge(self, nextStart):
        '''
        Defines if a clip should be merged with the one before
        '''
        if self.start <= nextStart <= self.end:
            shouldMerge = True
        else:
            shouldMerge = False

        return shouldMerge

    def merge_clips(self, nextEnd, timingsList, nextIndex):
        '''
        Merge clips
        '''
        self.end = nextEnd
        self.length = self.end - self.start
        del timingsList[nextIndex]

    def print_infos(self):
        print "Clip infos:"
        print "Timing: {}".format(self.timing)
        # print "Seconds: {}s".format(self.timingSeconds)
        print "start: {}".format(seconds_to_timing(self.start))
        print "end: {}".format(seconds_to_timing(self.end))
        print "length: {}s".format(self.length)
        print "path : {}".format(self.path)
        print

    def export_clip(self):
        '''
        :param filename: path to the original file
        :param start: start of the clip
        :param end: end of the clip
        :param targetname: path to the exported file
        '''
        if not os.path.exists(self.path):
            command = ["ffmpeg",
                       "-i", self.originalFile,
                       "-map", "0:0",
                       "-map", "0:1",
                       "-map", "0:2",
                       "-map", "0:3",
                       "-map", "0:4",
                       "-ss", "%0.2f" % self.start,
                       "-t", "%0.2f" % self.length,
                       "-codec", "copy",
                       self.path]
            FNULL = open(os.devnull, 'w')
            p = sp.Popen(command,
                         # shell=True,
                         stdin=sp.PIPE,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE
                         )
            # output = p.communicate('S\nL\n')[0]
            output, error = p.communicate()
            # print output
        else:
            print "Clip already logged delete it if you want to log it again."


def sort_files(fileToSort, destination):
    '''
    simply moves file to said destination
    :param fileToSort: Path to the file
    :param destination: where you want the file to be moved.
    '''
    basename = os.path.basename(fileToSort)
    if not os.path.exists(destination):
        os.makedirs(destination)
    destination = destination + "/" + basename
    os.rename(fileToSort, destination)


def get_timings(textFile, videoFile):
    '''
    Puts the content of a textfile in a list
    :param textFile: path to the text file
    :param videoFile: path to the videoFile
    :param line: line to read
    :return: list of all the timings
    '''
    f = open(textFile, 'r')
    lines = f.readlines()
    timings = []
    for line in lines:
        line = line[:-1]
        timings.append(line)
    f.close()
    return timings


def textFile_exists(textFile):
    '''Checks if the file exists'''
    if os.path.isfile(textFile) is False:
        print '''There is no associated text file, moving the video in a
                "NoTextFile" directory so that you can take a look'''
        return False
    return True


def seconds_to_timing(seconds):
    '''
    Converts the seconds in hh:mm:ss format
    '''
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{0:0>2}".format(h) + ":{0:0>2}".format(m) + ":{0:0>2}".format(s)


def main():

    # Creates the "Clips" Folder
    exportPath = mySettings.videoPath + "/Clips"
    if not os.path.exists(exportPath):
        os.makedirs(exportPath)

    # Creates the "Processed" Folder
    processedPath = mySettings.videoPath + "/Processed"
    if not os.path.exists(processedPath):
        os.makedirs(processedPath)

    # checks if there's an associated textfile with the video, if not, move the
    # video elsewhere
    videoFiles = glob.glob(
        "{}/*.{}".format(mySettings.videoPath, mySettings.videoFormat))
    for videoFile in videoFiles:
        name = os.path.basename(videoFile.rsplit('.', 1)[0])
        textFile = "{}/{}.txt".format(mySettings.videoPath, name)
        textFileExists = textFile_exists(textFile)
        if textFileExists is False:
            noTextFile = "{}/NoTextFile".format(mySettings.videoPath)
            sort_files(videoFile, noTextFile)
    # Loops through all the remaining videos in said folder
    videoFiles = glob.glob(
        "{}/*.{}".format(mySettings.videoPath, mySettings.videoFormat))
    for videoFile in videoFiles:

        name = os.path.basename(videoFile.rsplit('.', 1)[0])
        textFile = "{}/{}.txt".format(mySettings.videoPath, name)
        timings = get_timings(textFile, videoFile)
        mergedClips = []

        # processes all timings in file
        for timing in timings:

            currentIndex = timings.index(timing)
            clip = Clip(timing, videoFile)
            clip.timing_to_seconds()
            clip.get_range()

            while True and currentIndex + 1 < len(timings):
                nextTiming = timings[currentIndex + 1]
                nextClip = Clip(nextTiming, videoFile)
                nextClip.timing_to_seconds()
                nextClip.get_range()
                shouldMerge = clip.should_merge(nextClip.start)

                if shouldMerge is True:
                    clip.merge_clips(nextClip.end, timings, currentIndex + 1)
                    # goes back from one index since merge_clips deletes one
                    # item from the list
                else:
                    break
                currentIndex = currentIndex + 1

            mergedClips.append(clip)

        # exports all the processed timings
        for clip in mergedClips:
            videoIndex = videoFiles.index(videoFile)
            clipIndex = mergedClips.index(clip)
            # Probably not the cleanest way to do this :
            clip.path = "{}/{}_Clip_".format(exportPath, name) + \
                "{0:0>3}".format(clipIndex + 1) + ".{}" \
                .format(mySettings.videoFormat)
            print "\n--------------\n"
            print "Video {}/{}\n".format(videoIndex + 1, len(videoFiles))
            print "Name: {}\n".format(name)
            print "Clip {}/{}".format(clipIndex + 1, len(mergedClips))
            clip.print_infos()
            clip.export_clip()

        sort_files(videoFile, processedPath)
        sort_files(textFile, processedPath)
        print "File moved to the Processd folder"
main()
