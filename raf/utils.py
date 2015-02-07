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
