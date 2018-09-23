import time
import os
import shutil
from glob import glob

from EzLogging.core.config import config
import EzLogging.utils.csgo as csgo


class TimeLogger:

    def __init__(self, ui):
        self.isRecording = False
        self.starTime = None
        self.tempFile = None
        self.temp_csgo_demo = None
        self.logCount = 0
        self.ui = ui

    def create_file(self):
        """Creates a temp.txt file and starts a stopwatch."""
        if not self.isRecording:
            self.starTime = time.time()
            tempName = 'Temp.txt'
            self.tempFile = '{}/{}'.format(config.video_path, tempName)
            open(self.tempFile, 'w').close()
            self.isRecording = True
            self.ui.print_log_output("Recording")
            if config.csgo_manage_demos:
                self.ui.print_log_output("Waiting for the CS:GO demo to be available")
                self.temp_csgo_demo = csgo.get_matching_demo(self.starTime)
                if self.temp_csgo_demo:
                    self.ui.print_log_output("CS:GO demo found!")
                else:
                    self.ui.print_log_output("Couldn't find the CS:GO demo")
        else:
            self.ui.print_log_output("File already open.")

    def log_time(self):
        """Logs the current time in the temp.txt file."""
        if self.isRecording:
            seconds = int(time.time() - self.starTime)
            currentTime = time.strftime('%H:%M:%S', time.gmtime(seconds))

            with open(self.tempFile, 'a') as f:
                f.write(currentTime + '\n')
            self.logCount += 1
            self.ui.print_log_output(
                "Entry {0:0>2}: ".format(self.logCount) + currentTime
            )
        else:
            self.ui.print_log_output("You are not recording.")

    def close_file(self):
        if self.isRecording:
            os.chdir(config.video_path)
            newestVideo = None
            try:
                newestVideo = max(
                    glob('*.{}'.format(config.video_format)),
                    key=os.path.getctime
                )
            except ValueError:
                self.ui.print_log_output(
                    "no video found. couldn't rename the temp file."
                )

            if newestVideo:
                newName = ''.join((newestVideo.split('.')[0], '.txt'))
                os.rename(self.tempFile, newName)

            self.isRecording = False
            self.logCount = 0
            self.ui.print_log_output("Recording over")

            if config.csgo_manage_demos:
                if newestVideo:
                    demo_basename = os.path.basename(self.temp_csgo_demo)
                    demo_new_name = ''.join([
                        os.path.basename(newestVideo).rpartition('.')[0],
                        '.dem'
                    ])
                    demo_new_path = os.path.join(config.csgo_demos_path, demo_new_name)
                    os.rename(self.temp_csgo_demo, demo_new_path)
                    self.temp_csgo_demo = demo_new_path
                if config.csgo_copy_demos:
                    demos_folder = os.path.join(config.video_path, 'demos')
                    if not os.path.exists(demos_folder):
                        os.makedirs(demos_folder)
                    shutil.copy(self.temp_csgo_demo, demos_folder)
                    self.ui.print_log_output("Saved CS:GO demo.")


