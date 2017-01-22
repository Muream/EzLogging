import os


def check_path(path):
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
        print line
        timeLogs.append(line)
    return timeLogs
