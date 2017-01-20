import time
import os.path
import glob
import utils


class TextFile(object):

    def __init__(self, settings):
        self.state = 0
        self.tempfile = ''
        self.filename = ''
        self.filepath = ''
        self.startTime = 0
        self.logCount = 0

        self.settings = settings

    def createfile(self, ui):
        """Creates Time Logging file and starts a stopwatch."""
        # If we ARE NOT recording
        if self.state == 0:
            # Stores the time of the beginning of the recording
            self.startTime = time.time()
            # Creates a temporary text file
            tempname = 'Temp.txt'
            self.tempfile = '{}/{}'.format(self.settings.videoPath, tempname)
            f = open(self.tempfile, 'a')
            f.close()
            ui.logOutput.append('Recording...')
            ui.logOutput.append('A temporary file has been created, do not delete it.')
            ui.logOutput.append('IMPORTANT: Do not press {} until your recording software created the video file (a few seconds at most).\n'.format(self.settings.stopRecord))

            # Switches to a Recording state
            self.state = 1
        else:
            ui.logOutput.append('File already open.')

        return

    def writetime(self, ui):
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
            ui.logOutput.append("Entry {0:0>2} : ".format(self.logCount) + currenttime)

        else:
            ui.logOutput.append("You are not recording, press {} to start recording.".format(self.settings.startRecord))

        return

    def closefile(self, ui):
        """
        Makes sure the file is closed when the recording stops and renames it to
        the same name as the recording.
        """
        if self.state == 1:  # If we ARE recording

            # Gets the name of the latest video file of the directory in order to rename the temporary text file with the same name
            newestfile = os.path.basename(max(glob.iglob(self.settings.videoPath + '/*.' + self.settings.videoFormat),
                                              key=os.path.getctime))
            newName = utils.convert_string(ui.currentGame) + "_" + newestfile.split('.')[0] + '.txt'
            newVideoName = utils.convert_string(ui.currentGame) + "_" + newestfile.split('.')[0] + '.' + self.settings.videoFormat

            # Checks if there already is a file with this name to prevent overwriting an existing file
            for f in os.listdir(self.settings.videoPath):
                if f == newName:
                    newName = '{}_v2'.format(newName)

            # Renames the temporary text file
            os.rename(self.tempfile, self.settings.videoPath + '/' + newName)

            # Rename the video file once the recording software is done with it.
            couldRename = False
            while not couldRename:
                try:
                    os.rename(self.settings.videoPath + '/' + newestfile, self.settings.videoPath + '/' + newVideoName)
                    couldRename = True
                except WindowsError:
                    time.sleep(0.1)

            f = open(self.tempfile, 'a')
            f.close()

            # reset the log Count
            self.logCount = 0

            # Removes the temporary text file in case it still exists (Not sure if needed, to lazy to test)
            try:
                os.remove(self.tempfile)
            except OSError as e:  # name the Exception `e`
                ui.logOutput.append("Failed with:", e.strerror)

            ui.logOutput.append("\nRecording is over.\n")
            self.state = 0

        else:
            ui.logOutput.append("You are not recording, press {} to start recording.".format(self.settings.startRecord))

        return
