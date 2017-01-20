from __future__ import absolute_import
import time
import os.path
from glob import glob
from utils.config import Settings


class TimeLogger:

    def __init__(self):
        self.settings = Settings()
        self.isRecording = False
        self.starTime = None
        self.tempFile = None
        self.logCount = 0

    def create_file(self):
        """Creates a temp.txt file and starts a stopwatch."""
        if not self.isRecording:
            self.starTime = time.time()
            tempName = 'Temp.txt'
            self.tempFile = '{}/{}'.format(self.settings.videoPath, tempName)
            f = open(self.tempFile, 'a')
            f.close()
            self.isRecording = True
            print "Recording"
        else:
            print "File already open."

    def log_time(self):
        """Logs the current time in the temp.txt file."""
        if self.isRecording:
            seconds = int(time.time() - self.starTime)
            currentTime = time.strftime('%H:%M:%S', time.gmtime(seconds))

            with open(self.tempFile, 'a') as f:
                f.write(currentTime + '\n')
            self.logCount += 1
            print "Entry {0:0>2}: ".format(self.logCount) + currentTime
        else:
            print "You are not recording."

    def close_file(self):
        if self.isRecording:
            os.chdir(self.settings.videoPath)
            newestVideo = max(glob('*.{}'.format(self.settings.videoFormat)),
                              key=os.path.getctime)
            newName = ''.join((newestVideo.split('.')[0], '.txt'))
            os.rename(self.tempFile, newName)
            self.isRecording = False
            print "Recording over"
