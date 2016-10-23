import ConfigParser
import os
import utils

# TODO: deal with dumb fucks who enter the wrong type of variable


class Settings(object):

    def __init__(self,
                 videoPath=None,
                 videoFormat=None,
                 ffmpeg=None,
                 cutBefore=None,
                 cutAfter=None,
                 startRecord=None,
                 stopRecord=None,
                 logTime=None):

        self.videoPath = videoPath
        self.videoFormat = videoFormat
        self.ffmpeg = ffmpeg
        self.cutBefore = cutBefore
        self.cutAfter = cutAfter
        self.startRecord = startRecord
        self.stopRecord = stopRecord
        self.logTime = logTime

    def set_config(self):
        cfg = ConfigParser.ConfigParser()

        cfgfile = open('Config.cfg', 'w')
        cfg.add_section('File')
        cfg.add_section('Hotkeys')

        # path to the videos
        videoPath = utils.check_path(self.videoPath)

        # format of the videos
        videoformat = self.videoFormat

        # path to ffmpeg.exe
        ffmpeg = utils.check_path(self.ffmpeg)

        # Time before and after timing
        cutBefore = self.cutBefore
        cutAfter = self.cutAfter

        # Hotkeys
        startRecord = self.startRecord
        stopRecord = self.stopRecord
        logTime = self.logTime

        # Writes in the config file.
        cfg.set('File', 'video path', videoPath)
        cfg.set('File', 'video format', videoformat)
        cfg.set('File', 'ffmpeg path', ffmpeg)
        cfg.set('File', 'cut before', cutBefore)
        cfg.set('File', 'cut after', cutAfter)
        cfg.set('Hotkeys', 'start record', startRecord)
        cfg.set('Hotkeys', 'stop record', stopRecord)
        cfg.set('Hotkeys', 'log time', logTime)

        cfg.write(cfgfile)
        cfgfile.close()

    def read_config(self):
        config = {}
        cfg = ConfigParser.ConfigParser()
        cfg.read('Config.cfg')

        # Puts all the settings in a dictionary
        for section in cfg.sections():
            options = cfg.options(section)
            for option in options:
                try:
                    config[option] = cfg.get(section, option)
                    if config[option] == -1:
                        print ("skip: %s" % option)
                except:
                    print("exception on %s!" % option)
                    config[option] = None

        # convert the directory to attributes
        self.videoPath = config['video path']
        self.videoFormat = config['video format']
        self.ffmpeg = config['ffmpeg path']
        self.cutBefore = int(config['cut before'])
        self.cutAfter = int(config['cut after'])
        self.startRecord = config['start record']
        self.stopRecord = config['stop record']
        self.logTime = config['log time']
