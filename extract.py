#!/usr/bin/python2

import struct

with open("test/Archive_194801136.raf", "rb") as f:
	magic_number = f.read(4)
	version = struct.unpack("<I", f.read(4))[0]
	manager_index = struct.unpack("<I", f.read(4))[0]
	file_list_offset = struct.unpack("<I", f.read(4))[0]
	path_list_offset = struct.unpack("<I", f.read(4))[0]

	f.seek(file_list_offset);
	file_entries_count = struct.unpack("<I", f.read(4))[0]
	import ipdb; ipdb.set_trace()
	
	
