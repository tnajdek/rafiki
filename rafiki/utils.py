"""
This module contains utlities to support Rafiki library
This module contains the following functions:
    * mkdir_p - create directory and all intermediate directories as required
    * convert_lol_path - converts path from raf archive to filesystem
    * riot_hash - calculates riot hash
"""
import os
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def convert_lol_path(path):
    if(os.sep != '/'):
        path = path.replace("/", os.sep)
    return path


def ver_to_int(ver):
    version_int = ver.split('.')
    version_int = (int(version_int[0]) << 24) | (int(version_int[1]) << 16) | (int(version_int[2]) << 8) | int(version_int[3])
    return version_int

def int_to_ver(n):
    version_str = str((n >> 24) & 0xff)
    version_str = version_str + '.' + str((n >> 16) & 0xff)
    version_str = version_str + '.' + str((n >> 8) & 0xff)
    version_str = version_str + '.' + str(n & 0xff)
    return version_str

def riot_hash(string):
    hash = 0
    temp = 0

    for char in string:
        hash = (hash << 4) + ord(char.lower())
        temp = hash & 0xf0000000
        if(temp != 0):
            hash = hash ^ (temp >> 24)
            hash = hash ^ temp
    return hash
