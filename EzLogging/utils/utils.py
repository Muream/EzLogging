import os


def normalize_path(path):
    path = path.replace('\\', '/')
    if path[-1:] == '/':
        path = path[:-1]
    return path


def to_alpha_num(string):
    newString = ""
    for char in string:
        if char.isalpha() or char.isdigit():
            newString = newString + char

    return newString


def has_text_file(video):
    '''
    Checks if the file exists
    '''
    textFile = video.partition('.')[0] + '.txt'
    return os.path.isfile(textFile)


def move_file(fileToMove, destination):
    '''
    Moves file to said destination.
    :param fileToMove: Path to the file
    :param destination: where you want the file to be moved.
    '''
    if not os.path.exists(destination):
        os.makedirs(destination)
    destination = os.path.join(destination, fileToMove)
    os.rename(fileToMove, destination)


def get_timings(textFile):
    '''
    Puts the content of a textfile in a list.
    :param textFile: path to the text file
    :return: list of all the timings
    '''
    timeLogs = []
    with open(textFile) as f:
        lines = f.read().splitlines()

    for line in lines:
        timeLogs.append(line)
    return timeLogs


def timelog_to_seconds(timeLog):
    '''
    Converts the hh:mm:ss format in seconds
    '''
    timeLogSplit = timeLog.split(':')
    hour = int(timeLogSplit[0])
    minute = int(timeLogSplit[1])
    second = int(timeLogSplit[2])
    hour = hour * 60 * 60
    minute = minute * 60
    return hour + minute + second


def get_range(seconds, cutBefore, cutAfter):
    start = seconds - cutBefore
    if start < 0:
        start = 0
    end = seconds + cutAfter
    return (start, end)


def should_merge(clipRange, nextClipRange, cutBefore, cutAfter):
    if clipRange[0] <= nextClipRange[0] <= clipRange[1]:
        return True
    else:
        return False


def merge_clips(timeLogs, cfg):
    """
    seems to not merge all the timings it should merge for some reason
    """
    for i, timeLog in enumerate(timeLogs):
        clip = {}
        clip['seconds'] = timelog_to_seconds(timeLog)
        clip['range'] = get_range(clip['seconds'],
                                  cfg['cut before'],
                                  cfg['cut after'])
        clip['start'] = clip['range'][0]
        clip['end'] = clip['range'][1]

        print "current timeLog : {} ------------------".format(timeLog)

        while True:
            print timeLogs
            try:
                nextTimeLog = timeLogs[i+1]
                nextSeconds = timelog_to_seconds(nextTimeLog)
                nextClipRange = get_range(nextSeconds,
                                          cfg['cut before'],
                                          cfg['cut after'])
                shouldMerge = should_merge(clip['range'],
                                           nextClipRange,
                                           cfg['cut before'],
                                           cfg['cut after'])
                print shouldMerge
                if shouldMerge:
                    print "merging {} with {}".format(timeLog, nextTimeLog)
                    clip['end'] = nextSeconds + cfg['cut after']
                    clip['length'] = clip['end'] - clip['start']
                    print 'clip now lasts {}'.format(clip['length'])
                    timeLogs.remove(timeLogs[i+1])
                else:
                    print
                    break
            except IndexError:
                break
                pass
