#!/usr/bin/python2
import sys
import os
from raf import RafCollection
from utils import mkdir_p, convert_lol_path

basepath = "extracted"

collection = RafCollection(sys.argv[1])
files = collection.search("hud2012")
for raf_file in files:
	data = raf_file.extract()
	raf_file_path = convert_lol_path(raf_file.path)
	mkdir_p(basepath + os.pathsep + os.path.dirname(raf_file_path))
	with open(basepath + os.pathsep + raf_file_path, 'wb') as target_file:
		target_file.write(data)