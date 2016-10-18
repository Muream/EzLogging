# import pyhk
import time
import os.path
import glob
from Config import Settings
from pyhooked import Hook, KeyboardEvent

# TODO: reorganize the shit out of it

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

    def createfile(self):
        """Creates Time Logging file and starts a stopwatch."""
        # If we ARE NOT recording
        if self.state == 0:
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
            print 'IMPORTANT: Do not press {} until your recording software created the video file (a few seconds at most).\n'.format(mySettings.stopRecord)
            # Switches to a Recording state
            self.state = 1
        else:
            print "File already open."

    def writetime(self):
        """Logs the current recording time."""
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
            print "Entry {0:0>2} : ".format(self.logCount) + currenttime

        else:
            print "You are not recording, press {} to start recording.".format(mySettings.startRecord)

    def closefile(self):
        """
        Makes sure the file is closed when the recording stops and renames it to
        the same name as the recording.
        """
        if self.state == 1:  # If we ARE recording
            # Gets the name of the latest video file of the directory in order to rename the temporary text file with the same name
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
            # Removes the temporary text file in case it still exists (Not sure if needed, to lazy to test)
            try:
                os.remove(self.tempfile)
            except OSError as e:  # name the Exception `e`
                print "Failed with:", e.strerror  # look what it says
            print "\nRecording is over.\n"
            self.state = 0

        else:
            print "You are not recording, press {} to start recording.".format(mySettings.startRecord)

    def handle_events(self, args):
        if isinstance(args, KeyboardEvent):
            if args.current_key == mySettings.startRecord and args.event_type == 'key down':

                self.createfile()
            if args.current_key == mySettings.logTime and args.event_type == 'key down':
                self.writetime()
            if args.current_key == mySettings.stopRecord and args.event_type == 'key down':
                self.closefile()


def main():
    f = TextFile()
    hk = Hook()
    hk = Hook()
    hk.handler = f.handle_events
    hk.hook()

if __name__ == '__main__':
    main()
