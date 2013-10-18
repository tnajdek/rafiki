#!/usr/bin/python2

import struct
import zlib

class RafFile():
	pass

with open("test/Archive_194801136.raf", "rb") as f:
	files = list()
	paths = list()
	index = dict()

	magic_number = f.read(4)
	version = struct.unpack("<I", f.read(4))[0]
	manager_index = struct.unpack("<I", f.read(4))[0]
	file_list_offset = struct.unpack("<I", f.read(4))[0]
	path_list_offset = struct.unpack("<I", f.read(4))[0]

	f.seek(file_list_offset);
	file_entries_count = struct.unpack("<I", f.read(4))[0]
	for i in range(file_entries_count):
		raf = RafFile()
		raf.hash = struct.unpack("<I", f.read(4))[0]
		raf.data_offset = struct.unpack("<I", f.read(4))[0]
		raf.data_size = struct.unpack("<I", f.read(4))[0]
		raf.path_list_index = struct.unpack("<I", f.read(4))[0]
		files.append(raf)

	path_list_size = struct.unpack("<I", f.read(4))[0]
	path_list_count = struct.unpack("<I", f.read(4))[0]

	path_list_start_offset = f.tell()

	for i in range(path_list_count):
		f.seek(path_list_start_offset + (i)*8)
		path_offset = struct.unpack("<I", f.read(4))[0]
		path_length = struct.unpack("<I", f.read(4))[0]
		f.seek(path_list_offset + path_offset)
		path = f.read(path_length)
		path = path.strip('\x00')
		paths.append(path)

	with open("test/Archive_194801136.raf.dat", "rb") as fd:

		for raffile in files:
			raffile.path = paths[raffile.path_list_index]
			index[raffile.path] = raffile
			fd.seek(raffile.data_offset)
			raffile.data = zlib.decompress(fd.read(raffile.data_size))

	import ipdb; ipdb.set_trace()
	



	
	
	
