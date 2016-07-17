# import pyhk
import time
import os.path
import glob
from Config import Settings
from pyhooked import hook


# TODO:50 reorganize the shit out of it
# TODO:10 change hotkey Libary
# TODO:20 check what's going on "Careful! you have 1 temp file that have not been deleted, it might contain some sweet timings for one of your videos!"

mySettings = Settings()
mySettings.set_config()
mySettings.read_config()


class TextFile(object):

    def __init__(self):
        self.state = 0
        self.tempfile = ''
        self.filename = ''
        self.filepath = ''
        self.startTime = 0
        self.logCount = 0

    # Creates Time Logging file and starts a stopwatch in sync with the
    # recording software
    def createfile(self):
        if self.state == 0:  # If we ARE NOT recording
            # Stores the time of the beginning of the recording
            self.startTime = time.time()
            # Creates a temporary text file
            tempname = 'Temp.txt'
            self.tempfile = '{}/{}'.format(mySettings.videoPath, tempname)
            f = open(self.tempfile, 'a')
            f.close()
            print '\n\n---------'
            print '\nRecording...'
            print 'A temporary file has been created, do not delete it.\n'
            print 'IMPORTANT: Do not press {} until your recording software'\
                'created the video file (a few seconds at most).\n'\
                .format(mySettings.stopRecord)
            # Switches to a Recording state
            self.state = 1
        else:
            print "File already open."

    # Logs the current recording time
    def writetime(self):
        if self.state == 1:  # If we ARE recording
            # Substracts the currentTime to the startTime to get the elapsed
            # time since the start of the recording. Converts it to a hh:mm:ss
            # format.
            seconds = int(time.time() - self.startTime)
            currenttime = time.strftime('%H:%M:%S', time.gmtime(seconds))

            # Writes the time on a new line in the text file
            f = open(self.tempfile, 'a')
            f.write(currenttime + '\n')
            f.close()

            self.logCount += 1
            print "Entry {0:0>2} : ".format(self.logCount)  + currenttime

        else:
            print "You are not recording, press {} to start recording.".format(mySettings.startRecord)

    # Makes sure the file is closed when the recording stops and renames it to
    # the same name as the recording
    def closefile(self):
        if self.state == 1:  # If we ARE recording
            # Gets the name of the latest video file of the directory in order
            # to rename the temporary text file with the same name
            newestfile = os.path.basename(
                max(glob.iglob(mySettings.videoPath + '/*.' +
                               mySettings.videoFormat), key=os.path.getctime))
            newname = newestfile.split('.')[0] + '.txt'

            # Checks if there already is a file with this name to prevent
            # overwriting an existing file
            for f in os.listdir(mySettings.videoPath):
                if f == newname:
                    newname = '{}_v2'.format(newname)

            # Renames the temporary text file
            os.rename(self.tempfile, mySettings.videoPath + '/' + newname)
            f = open(self.tempfile, 'a')
            f.close()

            # reset the log Count
            self.logCount = 0
            # Removes the temporary text file in case it still exists (Not sure
            # if needed, to lazy to test)
            try:
                os.remove(self.tempfile)
            except OSError as e:  # name the Exception `e`
                print "Failed with:", e.strerror  # look what it says
            print "\nRecording is over.\n"
            self.state = 0

        else:
            print "You are not recording, press {} to start recording."\
                .format(mySettings.startRecord)


# Using Pyhk ---> can't press multiple keys at once
# def main():
#     hot = pyhk.pyhk()
#     f = TextFile()
#     hot.addHotkey([mySettings.startRecord], f.createfile)
#     hot.addHotkey([mySettings.logTime], f.writetime)
#     hot.addHotkey([mySettings.stopRecord], f.closefile)
#     hot.start()

# using pyhooked ---> CAN press multiple keys at once
def main():
    hk = hook()
    f = TextFile()
    hk.Hotkey([mySettings.startRecord], f.createfile)
    hk.Hotkey([mySettings.logTime], f.writetime)
    hk.Hotkey([mySettings.stopRecord], f.closefile)
    hk.listen()

if __name__ == '__main__':
    main()
