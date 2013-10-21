#!/usr/bin/python2
import os
import unittest
import shutil
from utils import mkdir_p, convert_lol_path
from raf import RafArchive, RafCollection

class TestExporting(unittest.TestCase):
	def setUp(self):
		self.archive = RafArchive(os.path.join("test", "Archive_194801136.raf"))
		# self.archive = RafArchive(os.path.join("test", "Archive_206999760.raf"))
		self.tmp_dir = os.path.join(os.getcwd(), 'tmp')
		mkdir_p(self.tmp_dir)


	def tearDown(self):
		pass
		# shutil.rmtree(self.tmp_dir)


	def test_dogfood(self):
		exported_raf_file = os.path.join(self.tmp_dir, 'exported.raf')
		for path, raf_file in self.archive.index.iteritems():
			data = raf_file.extract()
			data = data[:len(data)/2] + "testword" + data[:len(data)/2]			
			raf_file.insert(data)
		self.archive.export(exported_raf_file)

		exported_archive = RafArchive(exported_raf_file)
		for path, raf_file in exported_archive.index.iteritems():
			data = raf_file.extract()
			self.assertEqual(data[len(data)/2-4:(len(data)/2)+4], 'testword')
			self.assertEqual(data, self.archive.index[path].data)


	def test_file(self):
		dummy_contents = "/////////////////////\nHello Word"
		exported_raf_file = os.path.join(self.tmp_dir, 'minimap_export.raf')
		for path, raf_file in self.archive.index.iteritems():
			if(path.find("fontconfig_pl_PL")>-1):
				data = raf_file.extract()
				with open(os.path.join(self.tmp_dir, os.path.basename(convert_lol_path(path))), 'w') as f:
					f.write(dummy_contents)
				with open(os.path.join(self.tmp_dir, os.path.basename(convert_lol_path(path))), 'rb') as f:
					raf_file.insert(f.read())

		self.archive.export(exported_raf_file)
		exported_archive = RafArchive(exported_raf_file)
		for path, raf_file in exported_archive.index.iteritems():
			if(path.find("fontconfig_pl_PL")>-1):
				data = raf_file.extract()
				self.assertEqual(data, dummy_contents)

	# def test_minimap(self):
	# 	collection = RafCollection('../lol_game_client/filearchives')
	# 	files = collection.search("hud2012")
	# 	for raf_file in files:
	# 		if(raf_file.path.find("MinimapRight.ini") > -1):
	# 			raf_file_path = convert_lol_path(raf_file.path)
	# 			data = raf_file.extract()
	# 			data = data[:20] + "test word 1234" + data[20:]
	# 			raf_file.insert(data)
	# 			# mkdir_p(os.path.join(self.tmp_dir, os.path.dirname(raf_file_path)))
	# 			# with open(os.path.join(self.tmp_dir, raf_file_path)) as f:
	# 			# 	f.write(data)
	# 			# with open

	# 	for raf_file in files:
	# 		mkdir_p(os.path.join(self.tmp_dir, 'minimaptest'))
	# 		archive_export_path = os.path.join(self.tmp_dir, 'minimaptest', raf_file.archive.lol_patch_string+".raf")
	# 		raf_file.archive.export(archive_export_path)
	# 		imported_archive = RafArchive(archive_export_path)
	# 		for path, imported_raf_file in imported_archive.index.iteritems():
	# 			if(path.find("MinimapRight.ini")>-1):
	# 				import ipdb; ipdb.set_trace()


if __name__ == '__main__':
	unittest.main()