import os
import subprocess
from utils import utils


class Clip(object):

    def __init__(self, cfg, timeLog, originalFile=None, index=None):
        self.cfg = cfg
        self.timeLog = timeLog
        self.index = index
        if originalFile:
            self.originalFile = os.path.join(self.cfg.videoPath, originalFile)
            originalFileName = originalFile.partition('.')[0]
            self.name = "{}_clip{}.{}".format(
                originalFileName,
                str(index),
                self.cfg.videoFormat
            )
            self.exportPath = os.path.join(
                self.cfg.videoPath,
                "Clips",
                self.name
            )

        self.set_seconds()
        self.start = self.seconds - self.cfg.cutBefore
        if self.start < 0:
            self.start = 0
        self.end = self.seconds + self.cfg.cutAfter

        self.set_range()
        self.set_seconds()
        self.set_length()

    def set_new_start(self, newStart):
        self.start = newStart
        if self.start < 0:
            self.start = 0
        self.set_length()

    def set_new_end(self, newEnd):
        self.end = newEnd
        self.set_length()

    def set_range(self):
        self.range = [self.start, self.end]

    def set_seconds(self):
        self.seconds = utils.timelog_to_seconds(self.timeLog)

    def set_length(self):
        self.length = self.end - self.start

    def export(self):
        print "exporting : " + self.timeLog
        print "length = " + str(self.length)

        if not os.path.exists(os.path.join(self.cfg.videoPath, 'Clips')):
            os.mkdir(self.cfg.videoPath, 'Clips')

        command = [
            "ffmpeg",
            "-i", self.originalFile,
            "-map", "0:0",
            "-map", "0:1",
            "-map", "0:2",
            "-map", "0:3",
            "-map", "0:4",
            "-vcodec", "copy",
            "-acodec", "copy",
            "-ss", str(self.start),
            "-t", str(self.length),
            self.exportPath
        ]
        open(os.devnull, 'w')
        p = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # output = p.communicate('S/nL/n')[0]
        output, error = p.communicate()
        # print output
