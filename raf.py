import struct
import zlib
import os
import fnmatch
import re

class RafFile():
	pass		


class RafArchive():
	def __init__(self, path):
		files = list()
		paths = list()
		self.index = dict()
		self.path = path

		with open(path, "rb") as f:
			self.magic_number = f.read(4)
			self.version = struct.unpack("<I", f.read(4))[0]
			self.manager_index = struct.unpack("<I", f.read(4))[0]
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

			f.seek(4,1) #skip path_list_size
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

			for raffile in files:
				raffile.path = paths[raffile.path_list_index]
				self.index[raffile.path] = raffile

	def extract(self, raf_file):
		with open(self.path + '.dat', 'rb') as fd:
			fd.seek(raf_file.data_offset)
			raw_data = fd.read(raf_file.data_size)
			try:
				data = zlib.decompress(raw_data)
			except:
				raf_file.uncompressed = True
				data = raw_data
		return data


class RafCollection():
	def __init__(self, path):
		self.index = dict()
		items = os.listdir(path)
		for item in items:
			for filename in os.listdir(os.path.join(path, item)):
				if fnmatch.fnmatch(filename, '*.raf'):
					self.index[item] = RafArchive(os.path.join(path, item, filename))

	def search(self, text):
		matching_archives = list()
		for item,raf in self.index.iteritems():
			for path,archive in raf.index.iteritems():
				if(re.search(text, path, re.IGNORECASE)):
					matching_archives.append(archive)
		return matching_archives


					

 