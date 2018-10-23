import os
import subprocess
from EzLogging.utils import utils
from EzLogging.core.config import  config


class Clip(object):

    def __init__(self, timeLog, originalFile=None, index=None):
        self.timeLog = timeLog
        self.index = index
        if originalFile:
            self.originalFile = os.path.join(config.video_path, originalFile)

        self.set_seconds()
        self.start = self.seconds - config.cut_before
        if self.start < 0:
            self.start = 0
        self.end = self.seconds + config.cut_after

        self.set_range()
        self.set_seconds()
        self.set_length()

    @property
    def name(self):
        originalFileName = os.path.basename(self.originalFile.partition('.')[0])
        name = "{}_clip{}.{}".format(
            originalFileName,
            str(self.index).zfill(3),
            config.video_format
        )
        return name

    @property
    def exportPath(self):
        exportPath = os.path.join(
            config.video_path,
            "Clips",
            self.name
        )
        # exportPath = config.video_path + "/Clips/" + self.name
        return exportPath

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
            "-metadata:s:a:0", "title=Mic",
            "-map", "0:2",
            "-metadata:s:a:1", "title=VOIP",
            "-map", "0:3",
            "-metadata:s:a:2", "title=Computer",
            "-map", "0:4",
            "-metadata:s:a:3", "title=All",
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
        print("{}'s length should be {}".format(self.name, self.length))
