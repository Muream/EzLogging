import os
import ConfigParser
import utils

# TODO: deal with dumb fucks who enter the wrong type of variable


class Settings(object):

    def __init__(self):

        self.videoPath = None
        self.videoFormat = None
        self.ffmpeg = None
        self.cutBefore = None
        self.cutAfter = None
        self.startRecord = None
        self.stopRecord = None
        self.logTime = None
        if os.name == 'posix' and os.getenv("USER") == "root":
            sudoUser = os.getenv("SUDO_USER")
            self.configPath = "/home/{}/EzLogging/config.cfg".format(sudoUser)
        else:
            self.configPath = os.path.expanduser("~/EzLogging/config.cfg")
        self.read_config()

    def set_config(self):
        cfg = ConfigParser.ConfigParser()
        cfgfile = open(self.configPath, 'w')
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
        cfg.read(self.configPath)

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

        # convert the config file to attributes
        self.videoPath = config['video path']
        self.videoFormat = config['video format']
        self.ffmpeg = config['ffmpeg path']
        self.cutBefore = int(config['cut before'])
        self.cutAfter = int(config['cut after'])
        self.startRecord = config['start record']
        self.stopRecord = config['stop record']
        self.logTime = config['log time']
