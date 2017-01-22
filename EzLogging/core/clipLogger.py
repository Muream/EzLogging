import os
from glob import glob
from utils.config import Settings
from utils import utils


def clipLogger():
    settings = Settings()

    os.chdir(settings.videoPath)

    # create the "clips" folder
    if not os.path.exists('Clips'):
        os.makedirs('Clips')

    # creates the "Processed" folder
    if not os.path.exists('Processed'):
        os.makedirs('Processed')

    # remove the videos with no associated text files
    videoFiles = glob('*.{}'.format(settings.videoFormat))

    if not os.path.exists('NoTextFile'):
        os.makedirs('NoTextFile')

    for video in videoFiles:
        if not utils.has_text_file(video):
            utils.move_file(video, 'NoTextFile')

    # loop through the remaining videos and creates a dictionary of this form:
    # {timeLog1 : duration1, timeLog2, duration2}
    videoFiles = glob('*.{}'.format(settings.videoFormat))

    for video in videoFiles:
        textFile = video.partition('.')[0] + '.txt'
        timeLogs = utils.get_timings(textFile)

        for i, timeLog in enumerate(timeLogs):
###############################################################################
