import subprocess as sp
import os
import glob


def transcode(source, target):
    if not os.path.exists(target):
        os.makedirs(target)
    for video in os.listdir(source):
        videoPath = source + '/' + video
        targetVideoPath = target + '/' + video[:-3] + "mov"
        if os.path.isfile(videoPath):
            print video
            command = ["ffmpeg",
                       "-i", videoPath,
                       "-map", "0:0",
                       "-map", "0:1",
                       "-map", "0:2",
                       "-map", "0:3",
                       "-map", "0:4",
                       "-vcodec", "copy",
                       "-acodec", "copy",
                       "-f", "mp4",
                       targetVideoPath]
            FNULL = open(os.devnull, 'w')
            p = sp.Popen(command,
                         # shell=True,
                         stdin=sp.PIPE,
                         stdout=sp.PIPE,
                         stderr=sp.PIPE
                         )
            # output = p.communicate('S/nL/n')[0]
            output, error = p.communicate()
            # print output
        else:
            print "Clip already logged delete it if you want to log it again."


def main():
    source = raw_input("folder containing videos to transcode: ")
    target = raw_input("target folder: ")
    transcode(source, target)

if __name__ == '__main__':
    main()
