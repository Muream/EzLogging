import os
from glob import glob
from utils import utils


def clipLogger(cfg):
    os.chdir(cfg['video path'])

    # create the "clips" folder
    if not os.path.exists('Clips'):
        os.makedirs('Clips')

    # creates the "Processed" folder
    if not os.path.exists('Processed'):
        os.makedirs('Processed')

    # remove the videos with no associated text files
    videoFiles = glob('*.{}'.format(cfg['video format']))

    if not os.path.exists('NoTextFile'):
        os.makedirs('NoTextFile')

    for video in videoFiles:
        if not utils.has_text_file(video):
            utils.move_file(video, 'NoTextFile')

    # loop through the remaining videos and creates a dictionary of this form:
    # {timeLog1 : duration1, timeLog2, duration2}
    videoFiles = glob('*.{}'.format(cfg['video format']))

    for video in videoFiles:
        print video
        textFile = video.partition('.')[0] + '.txt'
        timeLogs = utils.get_timings(textFile)

        for i, timeLog in enumerate(timeLogs):
            # ## figure out how tow check the next timeLog if the previous one
            # ## has been merged
            seconds = utils.timelog_to_seconds(timeLog)
            clipRange = utils.get_range(seconds,
                                        cfg['cut before'],
                                        cfg['cut after'])

            try:
                nextTimeLog = timeLogs[i+1]
                nextSeconds = utils.timelog_to_seconds(nextTimeLog)
                nextClipRange = utils.get_range(nextSeconds,
                                                cfg['cut before'],
                                                cfg['cut after'])
            except IndexError:
                pass
            shouldMerge = utils.should_merge(clipRange,
                                             nextClipRange,
                                             cfg['cut before'],
                                             cfg['cut after'])
            if shouldMerge:
                timeLogs.remove(nextTimeLog)
            print "timelog: ", timeLog
            print "newxt timelog: ", nextTimeLog
            print "seconds: ", seconds
            print "next seconds: ", nextSeconds
            print "range: ", clipRange
            print "next range: ", nextClipRange
            print "should merge: ", shouldMerge
            print
        print
