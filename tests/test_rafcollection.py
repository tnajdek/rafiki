#!/usr/bin/env python
import os
import unittest
import shutil
from raf.utils import mkdir_p, convert_lol_path
from raf.raf import RafCollection, BaseRafArchive, RafFile

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

	def test_search(self):
		raffiles = self.collection.search("pl_PL")
		self.assertEqual(len(raffiles), 1)
		self.assertEqual(raffiles[0].path, "DATA/Menu/fontconfig_pl_PL.txt")


class TestOverridesInCollections(unittest.TestCase):
	def setUp(self):
		self.tmp_dir = os.path.join(TEST_ROOT, 'tmp')
		mkdir_p(self.tmp_dir)

	def tearDown(self):
		shutil.rmtree(self.tmp_dir)

	def build_fake_archive(self, version, content):
		version_dir = os.path.join(self.tmp_dir, "0.0.0.{}".format(version))
		mkdir_p(version_dir)
		fakeArchive = BaseRafArchive(os.path.join(version_dir, 'Archive.raf'))
		fakefile = RafFile(fakeArchive)
		fakefile.path = "DATA/Trolls/Are/funny.txt"
		fakefile.insert(content)
		fakeArchive.addRafFile(fakefile)
		fakeArchive.save()

	def test_overrides(self):
		badContent = "bad"
		goodContent = "good"

		for i in range(10):
			self.build_fake_archive(i, badContent)

		self.build_fake_archive(11, goodContent)
		collection = RafCollection(self.tmp_dir)
		raffiles = collection.raffiles()
		rf = raffiles.pop()
		data = rf.extract()
		self.assertEqual(data, goodContent)

