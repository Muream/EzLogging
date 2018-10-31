import os
from glob import glob
from EzLogging.utils import utils
from EzLogging.core.clip import Clip
from EzLogging.core.config import config


def clipLogger(ui):
    os.chdir(config.video_path)

    # create the "clips" folder
    if not os.path.exists('Clips'):
        os.makedirs('Clips')

    # creates the "Processed" folder
    if not os.path.exists('Processed'):
        os.makedirs('Processed')

    # remove the videos with no associated text files
    videoFiles = glob('*.{}'.format(config.video_format))

    if not os.path.exists('NoTextFile'):
        os.makedirs('NoTextFile')

    for video in videoFiles:
        if not utils.has_text_file(video):
            utils.move_file(video, 'NoTextFile')

    # loop through the remaining videos and creates a dictionary of this form:
    # {timeLog1 : duration1, timeLog2, duration2}
    videoFiles = glob('*.{}'.format(config.video_format))

    for video in videoFiles:

        textFile = video.partition('.')[0] + '.txt'
        export_clips(ui, video, textFile)

        utils.move_file(video, 'Processed')
        utils.move_file(textFile, 'Processed')
        ui.logOutput.append("Done!")


def export_clips(ui, video, textFile):
    timeLogs = utils.get_timings(textFile)
    ui.logOutput.append("Logging {}".format(str(video)))

    merged_clips = merge_clips(timeLogs, video)

    for i, clip in enumerate(merged_clips):
        clip.index = i
        ui.logOutput.append("Exporting clip {}".format(str(clip.index).zfill(3)))

        clip.export()


def merge_clips(timeLogs, video):
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

        clip = Clip(timeLog, originalFile=video, index=i)

        shouldMerge = True

        mergeAttempts = 1
        while shouldMerge:
            nextIndex = i + mergeAttempts
            print("Next Index", nextIndex)
            # break if there's no more timestamps
            if nextIndex >= len(timeLogs):
                break

            nextClip = Clip(timeLogs[nextIndex], originalFile=video, index=nextIndex)
            shouldMerge = utils.should_merge(
                clip,
                nextClip,
            )
            if shouldMerge:
                skipTimelogs.append(nextClip.timeLog)
                clip.set_new_end(newEnd=nextClip.end)
            mergeAttempts += 1

        clips.append(clip)
        newTimeLogs.append(clip.timeLog)

    return clips
