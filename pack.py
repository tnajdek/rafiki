#!/usr/bin/python2
import sys
import os
from raf import RafCollection
from utils import convert_lol_path

basepath = "extracted"

collection = RafCollection(sys.argv[1])
overrides_path = sys.argv[2]

assert len(overrides_path) > 0

if(not overrides_path[-1] == os.pathsep):
	overrides_path = overrides_path + os.pathsep

archives = set()

files = collection.search("hud2012")
for raf_file in files:
	raf_file_path = convert_lol_path(raf_file.path)
	file_path = overrides_path + raf_file_path
	try:
		with open(file_path, 'rb') as f:
			raf_file.insert(f.read())
		print("Creating override for %s in %s" % (raf_file.path, raf_file.archive.path))
	except IOError:
		pass

	archives.add(raf_file.archive)

for archive in archives:
	archive.export("overrides" + os.pathsep + archive.path)