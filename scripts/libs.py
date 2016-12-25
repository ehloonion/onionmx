import sys


def cross_input(text):
    if sys.version_info[0] < 3:
        return raw_input(text)
    return input(text)
