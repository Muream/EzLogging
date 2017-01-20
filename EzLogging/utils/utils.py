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
