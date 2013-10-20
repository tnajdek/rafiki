#!/usr/bin/python2

from raf import RafCollection, RafArchive

import os, errno

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise

basepath = "extracted"

collection = RafCollection('lol_game_client/filearchives')
# files = collection.search("hud2012")
# for raf_file in files:
# 	data = raf_file.extract()
	# mkdir_p(basepath + "/" + os.path.dirname(raf_file.path))
	# import ipdb; ipdb.set_trace()	
	# with open(basepath + "/" + raf_file.path, 'wb') as target_file:
	# 	target_file.write(data)

arch = collection.index['0.0.0.91']
arch.save("test.raf")

other_arch = RafArchive("test.raf")
import ipdb; ipdb.set_trace()
	