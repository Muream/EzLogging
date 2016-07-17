import ConfigParser
import os

# TODO:40 deal with dumb fucks who enter the wrong type of variable


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

    def check_path(self, path):
        path = path.replace('\\', '/')
        if path[-1:] == '/':
            path = path[:-1]
        return path

    def set_config(self):
        cfg = ConfigParser.ConfigParser()
        numberoftemp = 0
        try:
            # If the config file doesn't exist, create it and ask for the
            # user's configuration
            if not os.path.isfile('Config.cfg'):
                # Creates the config file by asking the user
                cfgfile = open('Config.cfg', 'w')
                cfg.add_section('File')
                cfg.add_section('Hotkeys')

                # ask the user the settings he wants to use
                print

                # path to the videos
                print "This is the first time you are using Config, you will need to set a few things up."
                print "This is VERY IMPORTANT, otherwise nothing will work."
                videoPath = raw_input("Path of your recordings: ")
                videoPath = self.check_path(videoPath)

                # format of the videos
                videoformat = raw_input("Format of your recording (ex: mp4, avi, etc.): ")
                print

                # path to ffmpeg.exe
                print ('If you do not have ffmpeg insalled: https://ffmpeg.org/download.html')
                check = True
                while check:
                    ffmpeg = raw_input("Path to ffmpeg.exe (similar to this: /ffmpeg/bin): ")
                    ffmpeg = self.check_path(ffmpeg)
                    if os.path.isfile('{}/ffmpeg.exe'.format(ffmpeg)) is False:
                        print 'ffmpeg.exe was not found here.'
                    else:
                        ffmpeg = '{}/ffmpeg.exe'.format(ffmpeg)
                        check = False
                    print

                # Time before and after timing
                cutBefore = raw_input('How long before the timing should AutoLog cut? (in seconds): ')
                cutAfter = raw_input('How long after the timing should AutoLog cut? (in seconds): ')
                print

                # Hotkeys
                print "List of possible hotkeys (at the bottom of the page) :"
                print "http://schurpf.com/python/python-hotkey-module/pyhk-end-user-documentation/"
                print "if you want to use the F keys, you have to write 'F7' manually instead of simply pressing F7"
                startRecord = raw_input("Shortcut used to start the recording: ")
                stopRecord = raw_input("Shortcut used to stop the recording: ")
                logTime = raw_input("Shortcut wanted to log the time of your recording: ")

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
        except ValueError:
            print "Oops! The config file has not been created, try running the script as administrator"
            print "or create a 'Config.cfg' in the same folder as EzLogging and AutoLog."

    def read_config(self):
        config = {}
        cfg = ConfigParser.ConfigParser()
        cfg.read('Config.cfg')
        # Puts all the settings in a dictionary in order to re-use it later
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

        self.videoPath = config['video path']
        self.videoFormat = config['video format']
        self.ffmpeg = config['ffmpeg path']
        self.cutBefore = int(config['cut before'])
        self.cutAfter = int(config['cut after'])
        self.startRecord = config['start record']
        self.stopRecord = config['stop record']
        self.logTime = config['log time']

        print "Press {} to start recording".format(self.startRecord)
        print "Press {} to log time".format(self.logTime)
        print "Press {} to stop recording".format(self.stopRecord)
