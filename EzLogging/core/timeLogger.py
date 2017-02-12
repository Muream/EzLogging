import time
import os.path
from glob import glob


class TimeLogger:

    def __init__(self, cfg):
        self.cfg = cfg
        self.isRecording = False
        self.starTime = None
        self.tempFile = None
        self.logCount = 0

    def create_file(self, ui):
        """Creates a temp.txt file and starts a stopwatch."""
        if not self.isRecording:
            self.starTime = time.time()
            tempName = 'Temp.txt'
            self.tempFile = '{}/{}'.format(self.cfg["video path"], tempName)
            f = open(self.tempFile, 'a')
            f.close()
            self.isRecording = True
            ui.print_log_output("Recording")
        else:
            ui.print_log_output("File already open.")

    def log_time(self, ui):
        """Logs the current time in the temp.txt file."""
        if self.isRecording:
            seconds = int(time.time() - self.starTime)
            currentTime = time.strftime('%H:%M:%S', time.gmtime(seconds))

            with open(self.tempFile, 'a') as f:
                f.write(currentTime + '\n')
            self.logCount += 1
            ui.print_log_output("Entry {0:0>2}: ".format(self.logCount) + currentTime)
        else:
            ui.print_log_output("You are not recording.")

    def close_file(self, ui):
        if self.isRecording:
            os.chdir(self.cfg["video path"])
            newestVideo = None
            try:
                newestVideo = max(glob('*.{}'.format(self.cfg["video format"])),
                                  key=os.path.getctime)
            except ValueError:
                ui.print_log_output("no video found. couldn't rename the temp file.")

            if newestVideo:
                newName = ''.join((newestVideo.split('.')[0], '.txt'))
                os.rename(self.tempFile, newName)

            self.isRecording = False
            ui.print_log_output("Recording over")
