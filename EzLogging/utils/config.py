import os
import utils
from ConfigParser import SafeConfigParser


class Config(object):
    """Base config Class."""

    def __init__(self):
        self.videoPath = ''
        self.videoFormat = ''
        self.ffmpegPath = ''
        self.startRecord = ''
        self.stopRecord = ''
        self.logTime = ''
        self.cutBefore = 0
        self.cutAfter = 0

        if os.name == 'posix' and os.getenv("USER") == "root":
            SUDOUSER = os.getenv("SUDO_USER")
            self.configFolder = "/home/{}/EzLogging/".format(SUDOUSER)
        else:
            self.configFolder = os.path.expanduser("~/EzLogging/")

        # read the config if we can
        try:
            self.read_config()
        except:
            pass

    @property
    def check_config(self):
        """
        Checks if the config file exists.
        if so, returns the config as a dictionnary.
        else, returns None
        """
        configExists = False

        # Create the config folder and config file
        if self.configFolder:
            if not os.path.exists(self.configFolder):
                os.makedirs(self.configFolder)

            self.configFile = os.path.join(self.configFolder, "config.cfg")
            self.configFile = utils.normalize_path(self.configFile)

            if os.path.isfile(self.configFile):
                configExists = True
                self.read_config()
            else:
                open(self.configFile, 'a').close()
        return configExists

    def set_config(
        self,
        videoPath='',
        videoFormat='',
        ffmpegPath='',
        startRecord='',
        stopRecord='',
        logTime='',
        cutBefore=0,
        cutAfter=0,
    ):

        parser = SafeConfigParser()
        parser.add_section('Hotkeys')
        parser.add_section('Recordings')
        parser.add_section('Trimming')
        parser.add_section('Misc')

        parser.set('Recordings', 'video path', str(videoPath))
        parser.set('Recordings', 'video format', str(videoFormat))
        parser.set('Misc', 'ffmpeg path', str(ffmpegPath))
        parser.set('Hotkeys', 'start record', str(startRecord))
        parser.set('Hotkeys', 'stop record', str(stopRecord))
        parser.set('Hotkeys', 'log time', str(logTime))
        parser.set('Trimming', 'cut before', str(cutBefore))
        parser.set('Trimming', 'cut after', str(cutAfter))

        with open(self.configFile, 'w') as f:
            parser.write(f)

        self.read_config()

    def read_config(self):
        parser = SafeConfigParser()
        parser.read(self.configFile)

        self.videoPath = parser.get('Recordings', 'video path')
        self.videoFormat = parser.get('Recordings', 'video format')
        self.ffmpegPath = parser.get('Misc', 'ffmpeg path')
        self.startRecord = parser.get('Hotkeys', 'start record')
        self.stopRecord = parser.get('Hotkeys', 'stop record')
        self.logTime = parser.get('Hotkeys', 'log time')
        self.cutBefore = parser.get('Trimming', 'cut before')
        self.cutAfter = parser.get('Trimming', 'cut after')
