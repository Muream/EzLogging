import os
from glob import glob
from utils import utils
from core.clip import Clip


def clipLogger(cfg):
    os.chdir(cfg.videoPath)

    # create the "clips" folder
    if not os.path.exists('Clips'):
        os.makedirs('Clips')

    # creates the "Processed" folder
    if not os.path.exists('Processed'):
        os.makedirs('Processed')

    # remove the videos with no associated text files
    videoFiles = glob('*.{}'.format(cfg.videoFormat))

    if not os.path.exists('NoTextFile'):
        os.makedirs('NoTextFile')

    for video in videoFiles:
        if not utils.has_text_file(video):
            utils.move_file(video, 'NoTextFile')

    # loop through the remaining videos and creates a dictionary of this form:
    # {timeLog1 : duration1, timeLog2, duration2}
    videoFiles = glob('*.{}'.format(cfg.videoFormat))

    for video in videoFiles:
        textFile = video.partition('.')[0] + '.txt'
        timeLogs = utils.get_timings(textFile)
        print video

        merged_clips = merge_clips(timeLogs, cfg, video)

        for clip in merged_clips:
            clip.export()
            print
            print "----------------------------------------------------"
            print
        # break here to test on only one video
        # break


def merge_clips(timeLogs, cfg, video):
    """
    seems to not merge all the timings it should merge for some reason
    """
    clips = []
    skipTimelogs = []
    newTimeLogs = []
    for i, timeLog in enumerate(timeLogs):
        # skip the timelog if it has been merged
        if timeLog in skipTimelogs:
            continue

        clip = Clip(cfg, timeLog, video, i)

        print " ------------------ current timeLog : {} ------------------".format(timeLog)
        shouldMerge = True

        mergeAttempts = 1
        while shouldMerge:
            try:
                nextClip = Clip(cfg, timeLogs[i+mergeAttempts])
                print "trying with " + nextClip.timeLog
                shouldMerge = utils.should_merge(
                    clip,
                    nextClip,
                    cfg,
                )
                if shouldMerge:
                    skipTimelogs.append(nextClip.timeLog)
                    print "merging {} with {}".format(
                        clip.timeLog,
                        nextClip.timeLog
                    )
                    clip.set_new_end(newEnd=nextClip.end+cfg.cutAfter)
                    print 'clip now lasts {}'.format(clip.length)
                    mergeAttempts += 1
                else:
                    print "not merging"
                    clips.append(clip)
                    newTimeLogs.append(clip.timeLog)
            except IndexError:
                print "No more timelogs to merge"
                break

    return clips
