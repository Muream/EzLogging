def check_path(path):
    path = path.replace('\\', '/')
    if path[-1:] == '/':
        path = path[:-1]
    return path


def convert_string(string):
    newString = ""
    for index, char in enumerate(string):
        if char.isalpha() or char.isdigit():
            newString = newString + char

    return newString
