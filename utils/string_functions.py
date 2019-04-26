import re


def find_first_apperence_by_regex(string, pattern):
    regex = re.compile(pattern)
    allGroups = regex.search(string)
    return allGroups.group(1)
