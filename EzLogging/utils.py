def check_path(path):
    path = path.replace('\\', '/')
    if path[-1:] == '/':
        path = path[:-1]
    return path
