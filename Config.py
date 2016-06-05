import ConfigParser
import os

# TODO deal with dumb fucks who enter the wrong type of variable

class Settings(object):

    def __init__(self):
        
        self.videoPath = None
        self.videoFormat = None
        self.ffmpegPath = None
        self.cutBefore = None
        self.cutAfter = None
        self.fps = None
        self.startRecord = None
        self.stopRecord = None
        self.logTime = None

    def set_config(self):

        cfg = ConfigParser.ConfigParser()
        numberoftemp = 0
        try:
            # If the config file doesn't exist, create it and ask for the
            # user's configuration
            if not os.path.isfile('EzLogging.cfg'):
                # Creates the config file by asking the user
                cfgfile = open('EzLogging.cfg', 'w')
                cfg.add_section('File')
                cfg.add_section('Hotkeys')

                # ask the user the settings he wants to use
                print
                print "This is the first time you are using EzLogging, you will need to set a few things up."
                print "This is VERY IMPORTANT, otherwise nothing will work."
                videoPath = raw_input("Path of your recordings: ")
                videoPath = videoPath.replace('\\', '/')
                videoformat = raw_input(
                    "Format of your recording (ex: mp4, avi, etc.): ")
                print
                print (
                    'If you do not have ffmpeg insalled: https://ffmpeg.org/download.html')
                ffmpegPath = raw_input(
                    "Path of your ffmpeg (similar to this: installationFolder/ffmpeg/bin/ffmpeg.exe): ")
                ffmpegPath = ffmpegPath.replace('\\', '/')
                cutBefore = raw_input(
                    'How long before the timing should AutoLog cut? (in seconds): ')
                cutAfter = raw_input(
                    'How long after the timing should AutoLog cut? (in seconds): ')
                fps = raw_input('fps of your videos: ')

                print
                print 'List of possible hotkeys (at the bottom of the page) : http://schurpf.com/python/python-hotkey-module/pyhk-end-user-documentation/'
                startRecord = raw_input(
                    "Shortcut used to start the recording: ")
                stopRecord = raw_input(
                    "Shortcut used to stop the recording: ")
                logTime = raw_input(
                    "Shortcut wanted to log the time of your recording: ")

                # writes in the config file.
                cfg.set('File', 'video path', videoPath)
                cfg.set('File', 'video format', videoformat)
                cfg.set('File', 'ffmpeg path', ffmpegPath)
                cfg.set('File', 'cut before', cutBefore)
                cfg.set('File', 'cut after', cutAfter)
                cfg.set('File', 'fps', fps)
                cfg.set('Hotkeys', 'start record', startRecord)
                cfg.set('Hotkeys', 'stop record', stopRecord)
                cfg.set('Hotkeys', 'log time', logTime)
                cfg.write(cfgfile)
                cfgfile.close()
        except ValueError:
            print "Oops! The config file has not been created, try running the script as administrator or create a 'EzLogging.cfg' next to your 'EzLogging.py'."

    def read_config(self):
        config={}
        cfg=ConfigParser.ConfigParser()
        cfg.read('EzLogging.cfg')
        # Puts all the settings in a dictionary in order to re-use it later
        for section in cfg.sections():
            options=cfg.options(section)
            for option in options:
                try:
                    config[option]=cfg.get(section, option)
                    if config[option] == -1:
                        print ("skip: %s" % option)
                except:
                    print("exception on %s!" % option)
                    config[option]=None

        self.videoPath = config['video path']
        self.videoFormat = config['video format']
        self.ffmpegPath = config['ffmpeg path']
        self.cutBefore = int(config['cut before'])
        self.cutAfter = int(config['cut after'])
        self.fps = float(config['fps'])
        self.startRecord = config['start record']
        self.stopRecord = config['stop record']
        self.logTime = config['log time']
