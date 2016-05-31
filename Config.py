import ConfigParser
import os.path

def set_config():
    config = {}
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
            print "This is the first time you are using EzLogging, you will need to set a few things up."
            print "This is very important, the script will not work otherwise."
            videoPath = raw_input("Path of your recordings: ")
            videoPath = path.replace('\\', '/')
            videoformat = raw_input("the format you use for your videos: ")
            ffmpegPath = raw_input("Path of your ffmpeg: ")
            ffmpegPath = path.replace('\\', '/')
            startrecord = raw_input(
                "Shortcut used to start the recording: ")
            stoprecord = raw_input("Shortcut used to stop the recording: ")
            logtime = raw_input(
                "Shortcut wanted to log the time of your recording: ")
            cfg.set('File', 'Videos Path', videoPath)
            cfg.set('File', 'Video Format', videoformat)
            cfg.set('File', 'FFmpeg Path', ffmpegPath)
            cfg.set('Hotkeys', 'Start record', startrecord)
            cfg.set('Hotkeys', 'Stop record', stoprecord)
            cfg.set('Hotkeys', 'Log time', logtime)
            cfg.write(cfgfile)
            cfgfile.close()
    except ValueError:
        print "Oops! The config file has not been created, try running the script as administrator or create a 'EzLogging.cfg' next to your 'EzLogging.py'."

set_config()
