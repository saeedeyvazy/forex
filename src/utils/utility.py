import os


def path_exists(directory, start, end):
    files = os.listdir(directory)
    for file in files:
        if file == start + end:
            return directory + "/" + file

        if file.startswith(start) and file.endswith(end):
            return directory + "/" + file
    return False
