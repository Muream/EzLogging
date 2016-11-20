def check_path(path):
    path = path.replace('\\', '/')
    if path[-1:] == '/':
        path = path[:-1]
    return path


def convert_string(string):
    newString = ""
    for index, char in enumerate(string):
        try:
            nextChar = string[index + 1]
        except IndexError:
            nextChar = char
        if char.isalpha() or char.isdigit():
            newString = newString + char
        elif nextChar.isalpha() or nextChar.isdigit():
            newString = newString + "_"
        else:
            continue
