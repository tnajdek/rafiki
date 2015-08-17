#!/usr/bin/env python
import os
import unittest
import shutil
from rafiki import RafFile, RafArchive, RafCollection
from rafiki.rafiki import BaseRafArchive
from rafiki.utils import mkdir_p, convert_lol_path

TEST_ROOT = os.path.dirname(os.path.realpath(__file__))


class TestExporting(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = os.path.join(TEST_ROOT, 'tmp')
        self.archive = RafArchive(os.path.join(TEST_ROOT, "data", '0.0.0.0', "Archive_194801136.raf"))
        mkdir_p(self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_writes_identical_dat_files(self):
        exported_raf_file = os.path.join(self.tmp_dir, 'exported.raf')
        self.archive.save(exported_raf_file)

        src_dat_file_bin = open("{}.dat".format(self.archive.path), "rb").read()
        dest_dat_file_bin = open("{}.dat".format(exported_raf_file), "rb").read()

        self.assertEqual(len(src_dat_file_bin), len(dest_dat_file_bin))

    def test_dogfooding(self):
        data_store = dict()
        for path, raf_file in self.archive.index.iteritems():
            data = raf_file.extract()
            data = data[:len(data) / 2] + "testword" + data[:len(data) / 2]
            data_store[path] = data
            raf_file.insert(data)
        exported_raf_file_path = os.path.join(self.tmp_dir, 'exported.raf')
        self.archive.save(exported_raf_file_path)
        for path, raf_file in self.archive.index.iteritems():
            raf_file.unload()
        self.archive = None

        modified_raf_archive = RafArchive(exported_raf_file_path)
        for path, raf_file in modified_raf_archive.index.iteritems():
            data = raf_file.extract()
            target_data = data_store[path]
            self.assertEqual(data[len(data) / 2 - 4:(len(data) / 2) + 4], 'testword')
            self.assertEqual(data, target_data)

    def test_read_fake_raf(self):
        fakeContent = "Aloha world."
        fakeRafPath = os.path.join(self.tmp_dir, 'fake.raf')
        fakeArchive = BaseRafArchive(fakeRafPath)
        fakefile = RafFile(fakeArchive)
        fakefile.path = "DATA/Trolls/Are/funny.txt"
        fakefile.insert(fakeContent)
        fakeArchive.addRafFile(fakefile)
        fakeArchive.save()

        archive = RafArchive(fakeRafPath)
        self.assertEqual(len(archive.index.keys()), 1)
        self.assertIn(fakefile.path, archive.index.keys())
        self.assertEqual(archive.index[fakefile.path].extract(), fakeContent)

    def test_read_real_raf(self):
        file_name = "DATA/Menu/fontconfig_pl_PL.txt"
        self.assertIn(file_name, self.archive.index)
        raf_file = self.archive.index[file_name]
        raf_data = raf_file.extract()
        self.assertIn("karze wyzwiska homofobiczne czy rasowe", raf_data)

    def test_content_write(self):
        dummy_contents = "Hello Word"
        exported_raf_file = os.path.join(self.tmp_dir, 'minimap_export.raf')
        for path, raf_file in self.archive.index.iteritems():
            if(path.find("fontconfig_pl_PL") > -1):
                data = raf_file.extract()
                with open(os.path.join(self.tmp_dir, os.path.basename(convert_lol_path(path))), 'w') as f:
                    f.write(dummy_contents)
                with open(os.path.join(self.tmp_dir, os.path.basename(convert_lol_path(path))), 'rb') as f:
                    raf_file.insert(f.read())

        self.archive.save(exported_raf_file)
        exported_archive = RafArchive(exported_raf_file)
        for path, raf_file in exported_archive.index.iteritems():
            if(path.find("fontconfig_pl_PL") > -1):
                data = raf_file.extract()
                self.assertEqual(data, dummy_contents)

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
