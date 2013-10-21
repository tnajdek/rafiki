#!/usr/bin/python2
import os
import unittest
import shutil
from utils import mkdir_p
from raf import RafArchive

class TestExporting(unittest.TestCase):
	def setUp(self):
		self.archive = RafArchive(os.path.join("test", "Archive_194801136.raf"))
		# self.archive = RafArchive(os.path.join("test", "Archive_206999760.raf"))
		self.tmp_dir = os.path.join(os.getcwd(), 'tmp')
		mkdir_p(self.tmp_dir)
		self.exported_raf_file = os.path.join(self.tmp_dir, 'exported.raf')
		for path, raf_file in self.archive.index.iteritems():
			data = raf_file.extract()
			data = data[:len(data)/2] + "testword" + data[:len(data)/2]
			raf_file.insert(data)
		self.archive.export(self.exported_raf_file)

	def tearDown(self):
		shutil.rmtree(self.tmp_dir)


	def test_dogfood(self):
		exported_archive = RafArchive(self.exported_raf_file)
		for path, raf_file in exported_archive.index.iteritems():
			data = raf_file.extract()
			self.assertEqual(data[len(data)/2-4:(len(data)/2)+4], 'testword')


if __name__ == '__main__':
	unittest.main()