#!/usr/bin/env python
import os
import unittest
import shutil
from raf.utils import mkdir_p, convert_lol_path
from raf.raf import RafCollection

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))


class TestCollections(unittest.TestCase):
	def setUp(self):
		self.collection = RafCollection(os.path.join(TEST_ROOT, "data", ))
		self.tmp_dir = os.path.join(TEST_ROOT, 'tmp')
		mkdir_p(self.tmp_dir)

	def tearDown(self):
		shutil.rmtree(self.tmp_dir)

	def test_includes_all_raf_archives(self):
		self.assertEqual(len(self.collection.index.keys()), 3)

	def test_returns_all_raffiles(self):
		raffiles = self.collection.raffiles()
