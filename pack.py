#!/usr/bin/python2
import sys
import os
from raf import RafCollection
from utils import mkdir_p, convert_lol_path

collection = RafCollection(sys.argv[1])
overrides_path = sys.argv[2]

assert len(overrides_path) > 0

if(not overrides_path[-1] == os.sep):
	overrides_path = overrides_path + os.sep

archives = set()

files = collection.search("hud2012")
for raf_file in files:
	raf_file_path = convert_lol_path(raf_file.path)
	file_path = overrides_path + raf_file_path 
	try:
		with open(file_path, 'rb') as f:
			raf_file.insert(f.read())
		# print("Creating override for %s in %s" % (raf_file.path, raf_file.archive.path))
	except IOError:
		# print("NOT FOUND: %s" % file_path)
		pass

	archives.add(raf_file.archive)

for archive in archives:
	archive_override_path = "overrides" + os.sep + archive.path
	mkdir_p(os.path.dirname(archive_override_path))
	archive.export(archive_override_path)