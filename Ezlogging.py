import pyhk
import time
import ConfigParser
import os.path
import glob
from Tkinter import Tk
r=Tk()

class TextFile(object):
    def __init__(self):
        self.state = 0
        self.tempfile = ''
        self.filename = ''
        self.path = ''
        self.filepath = ''
        self.startTime = 0
        self.config = {}
        self.path = ''
        self.startrecord = ''
        self.stoprecord = ''
        self.logtime = ''
        self.videoformat = ''

#

    # All the settings stuff
    def startup(self):
        config = {}
        cfg = ConfigParser.ConfigParser()
        numberoftemp = 0
        try:
            if not os.path.isfile('EzLogging.cfg'):  # If the config file doesn't exist, create it and ask for the user's configuration
                # Creates the config file by asking the user
                cfgfile = open('EzLogging.cfg', 'w')
                cfg.add_section('File')
                cfg.add_section('Hotkeys')
                print "This is the first time you are using EzLogging, you will need to set a few things up."
                print "This is very important, the script will not work otherwise."
                path = raw_input("Path of your recordings: ")
                path = path.replace('\\', '/')
                videoformat = raw_input("the format you use for your videos: ")
                startrecord = raw_input("Shortcut used to start the recording: ")
                stoprecord = raw_input("Shortcut used to stop the recording: ")
                logtime = raw_input("Shortcut wanted to log the time of your recording: ")
                cfg.set('File', 'Path', path)
                cfg.set('File', 'Video Format', videoformat)
                cfg.set('Hotkeys', 'Start record', startrecord)
                cfg.set('Hotkeys', 'Stop record', stoprecord)
                cfg.set('Hotkeys', 'Log time', logtime)
                cfg.write(cfgfile)
                cfgfile.close()
        except ValueError:
            print "Oops! The config file has not been created, try running the script as administrator or create a 'EzLogging.cfg' next to your 'EzLogging.py'."

        cfg.read('EzLogging.cfg')
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

        print "Settings loaded successfully."
        self.config = config
        self.path = self.config['path']
        print 'Recording Path: ' + self.path
        self.videoformat = self.config['video format']
        print 'Video Format: ' + self.videoformat
        self.startrecord = config['start record']
        print 'Start Record: ' + self.startrecord
        self.stoprecord = config['stop record']
        print 'Stop Record: ' + self.stoprecord
        self.logtime = config['log time']
        print 'Log Time: ' + self.logtime
        print '\nIf these settings are not correct, delete the "EzLogging.cfg" and restart the script\n'

        for f in os.listdir(self.path):
            if "Temp" in f:
                numberoftemp = numberoftemp+1
        if numberoftemp == 1:
            print "Careful! you have %i temp file that have not been deleted, it might contain some sweet timings for one of your videos! Please check it out and rename and/or delete it." %numberoftemp
        if numberoftemp > 1:
            print "Careful! you have %i temp files that have not been deleted, they might contain some sweet timings for one of your videos! Please check it out and rename and/or delete them." %numberoftemp
        for f in os.listdir(self.path):
            if f == "Temp.txt" :
                os.rename(self.path+"/Temp.txt", self.path+"/Temp_%i.txt" %numberoftemp)
                print "A backup of Temp.txt has been created"


        return config

    # Creates Time Logging file and starts a stopwatch in syn with the recording software
    def createfile(self):
        if self.state == 0: # If we ARE NOT recording
            # Stores the time of the beginning of the recording
            self.startTime = time.time()
            # Creates a temporary text file
            tempname = 'Temp.txt'
            self.tempfile = '%s/%s' % (self.path, tempname)
            f = open(self.tempfile, 'a')
            f.close()
            print '\n\n-----------------------------------------------------------------------------------------------------'
            print '\nRecording...'
            print 'A temporary file has been created, do not delete it.\n'
            print 'IMPORTANT: Do not press %s until your recording software created the video file.\n' % self.stoprecord
            # Switches to a Recording state
            self.state = 1
        else:
            print "File already open."

    # Logs the current recording time
    def writetime(self):
        if self.state == 1: # If we ARE recording
            # Substracts the currentTime to the startTime to get the elapsed time since the start of the recording. Converts it to a hh:mm:ss format.
            seconds = int(time.time() - self.startTime)
            currenttime = time.strftime('%H:%M:%S', time.gmtime(seconds))
            # Writes the time on a new line in the text file
            f = open(self.tempfile, 'a')
            f.write(currenttime + '\n')
            f.close()
            print 'New entry : ' + currenttime
        else:
            print "You are not recording, press %s to start recording." % self.startrecord

    # Makes sure the file is closed when the recording stops and renames it to the same name as the recording
    def closefile(self):
        if self.state == 1:# If we ARE recording
            # Gets the name of the latest video file of the directory in order to rename the temporary text file with the same name
            newestfile = os.path.basename(max(glob.iglob(self.path + '/*.' + self.videoformat), key=os.path.getctime))
            newname = newestfile.split('.')[0] + '.txt'
            # Checks if there already is a file with this name to prevent overwriting an existing file
            for f in os.listdir(self.path):
                if f == newname:
                    newname = '%s_v2' %newname
            # Renames the temporary text file
            os.rename(self.tempfile, self.path + '/' + newname)
            f = open(self.tempfile, 'a')
            f.close()
            # Removes the temporary text file in case it still exists (Not sure if needed, to lazy to test)
            try:
                os.remove(self.tempfile)
            except OSError as e:  # name the Exception `e`
                print "Failed with:", e.strerror  # look what it says
            print "\nRecording is over.\n"
            self.state = 0

        else:
            print "You are not recording, press %s to start recording." % self.startrecord


def main():
    hot = pyhk.pyhk()
    f = TextFile()
    config = f.startup()
    startrecord = config['start record']
    stoprecord = config['stop record']
    logtime = config['log time']
    hot.addHotkey([startrecord], f.createfile)
    hot.addHotkey([logtime], f.writetime)
    hot.addHotkey([stoprecord], f.closefile)
    hot.start()


main()

