import os
import subprocess
from EzLogging.utils import utils
import EzLogging.core.config


class Clip(object):

    def __init__(self, timeLog, originalFile=None, index=None):
        self.timeLog = timeLog
        self.index = index
        if originalFile:
            self.originalFile = os.path.join(config.video_path, originalFile)
            originalFileName = originalFile.partition('.')[0]
            self.name = "{}_clip{}.{}".format(
                originalFileName,
                str(index),
                config.video_format
            )
            self.exportPath = os.path.join(
                config.video_path,
                "Clips",
                self.name
            )

        self.set_seconds()
        self.start = self.seconds - config.cut_before
        if self.start < 0:
            self.start = 0
        self.end = self.seconds + config.cut_after

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

        if not os.path.exists(os.path.join(config.video_path, 'Clips')):
            os.mkdir(config.video_path, 'Clips')

        command = [
            "ffmpeg",
            "-ss", str(self.start),
            "-t", str(self.length),
            "-i", self.originalFile,
            "-map", "0:0",
            "-map", "0:1",
            "-map", "0:2",
            "-map", "0:3",
            "-map", "0:4",
            "-vcodec", "copy",
            "-acodec", "copy",
            "-avoid_negative_ts", "1",
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
