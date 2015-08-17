"""
This module contains classes to extract, change and re-pack
raf files used by Leauge of Legends client
This module contains the following classes:
    * RafFile - represents a single file inside an archive
    * BaseRafArchive - represents a single Raf Archive, can be empty
    * RafArchive - convienience class, build from existing archive file
    * RafCollection - finds and maintains all raf files within a path
    * RafInstallation - represents game installation path
"""
import struct
import zlib
import os
import fnmatch
import re
import platform

from builtins import bytes

from .utils import riot_hash


class RafFile():
    def __init__(self, archive):
        self.archive = archive
        self.dat_file_location = self.archive.path + ".dat"
        self.data = None
        self.modified = False
        self.original_file_compressed = False

    def extract(self):
        with open(self.dat_file_location, 'rb') as fd:
            fd.seek(self.data_offset)
            self.raw_data = fd.read(self.data_size)

        # some data is compressed with zlib, some is not
        try:
            self.data = zlib.decompress(self.raw_data)
            self.original_file_compressed = True
        except Exception:
            self.data = self.raw_data

        return self.data

    def insert(self, data):
        self.modified = True
        self.data = data
        if(self.original_file_compressed):
            self.raw_data = zlib.compress(data)
        else:
            self.raw_data = data
        self.data_size = len(self.raw_data)

    def unload(self):
        """
        Unloads data from the memory but keeps meta data
        """
        if(hasattr(self, 'raw_data')):
            del self.raw_data

        self.data = None
        self.modified = False
        self.original_file_compressed = False


class BaseRafArchive(object):
    MAGIC_NUMBER = b'\xf0\x0e\xbe\x18'

    def __init__(self, path):
        self.files = list()
        self.paths = list()
        self.index = dict()
        self.path = path

    def addRafFile(self, raffile):
        raffile.archive = self
        if(not raffile.path):
            raise Exception("Raf File needs to have a path in order to be appended to the archive")
        self.files.append(raffile)
        self.paths.append(raffile.path)

    def delRafFile(self, raffile):
        assert raffile in self.files
        assert raffile.path in self.paths
        self.files.remove(raffile)
        self.paths.remove(raffile.path)

    def open(self):
        with open(self.path, "rb") as f:
            magic_number = f.read(4)
            self.version = struct.unpack("<I", f.read(4))[0]
            self.manager_index = struct.unpack("<I", f.read(4))[0]
            files_list_offset = struct.unpack("<I", f.read(4))[0]
            paths_list_offset = struct.unpack("<I", f.read(4))[0]

            assert files_list_offset == f.tell()

            file_entries_count = struct.unpack("<I", f.read(4))[0]
            for i in range(file_entries_count):
                raf = RafFile(self)
                raf.hash = struct.unpack("<I", f.read(4))[0]
                raf.data_offset = struct.unpack("<I", f.read(4))[0]
                raf.data_size = struct.unpack("<I", f.read(4))[0]
                raf.path_list_index = struct.unpack("<I", f.read(4))[0]
                self.files.append(raf)

            assert paths_list_offset == f.tell()

            path_list_size = struct.unpack("<I", f.read(4))[0]
            path_list_count = struct.unpack("<I", f.read(4))[0]
            path_list_start_offset = f.tell()

            for i in range(path_list_count):
                f.seek(path_list_start_offset + (i) * 8)
                path_offset = struct.unpack("<I", f.read(4))[0]
                path_length = struct.unpack("<I", f.read(4))[0]
                f.seek(paths_list_offset + path_offset)
                path = f.read(path_length)
                path = path.strip(b'\x00')
                path = path.decode('ascii')
                self.paths.append(path)

            for raffile in self.files:
                raffile.path = self.paths[raffile.path_list_index]
                assert riot_hash(raffile.path) == raffile.hash
                self.index[raffile.path] = raffile

    def save(self, save_path=None):
        save_path = save_path or self.path
        if(len(self.paths) == 0):
            raise Exception("Archive should contain at least one file")

        with open(save_path, "wb") as f:
            # header length is constant. It consists of:
            # 4 bytes for magic number
            # 4 bytes for version (usually 1)
            # 4 bytes for manager_undex (usually 0)
            # 4 bytes for offset of the files list
            # 4 bytes for offset of the paths list
            header_length = files_list_offset = 20

            # Files list length depends on the amount of files stored inside the archive:
            # 4 bytes for count store (total number of files)
            # Then for each file:
            #   4 bytes for file hash
            #   4 bytes for the offset from the beginning of the associated .raf.dat file.
            #   4 bytes for the size of the data stored in the associated .raf.dat file.
            #   4 bytes for the index (counting from 0) into the path list
            files_list_length = 4 + (len(self.files) * 16)
            paths_list_offest = header_length + files_list_length

            # Paths are stored in ASCII hence paths lists length depends on the number of files
            # and the literal lenght of each file. Paths lists consists of:
            # 4 bytes for the number of bytes contained in the paths lists
            # 4 bytes for the number of entries in the paths lists (total number of files)
            # Then for each file:
            #   4 bytes for the  offset from the path list (not the beginning of the file)
            #   4 bytes the length of the path string in bytes.
            # Then for each file:
            #   n bytes for the literal ASCII-encoded path string
            #   1 byte for the termination character (\x00)
            literals_length = sum([len(path) + 1 for path in self.paths])
            paths_list_length = 8 + (len(self.paths) * 8) + literals_length
            eof = header_length + files_list_length + paths_list_length

            # HEADER
            f.write(self.MAGIC_NUMBER)
            f.write(struct.pack("<I", getattr(self, 'version', 1)))
            f.write(struct.pack("<I", getattr(self, 'manager_index', 0)))
            f.write(struct.pack("<I", files_list_offset))
            f.write(struct.pack("<I", paths_list_offest))

            assert files_list_offset == f.tell()

            # FILE LIST
            f.write(struct.pack("<I", len(self.paths)))
            data_file_offset = 0

            assert len(self.files) == len(self.paths)

            for raf_file in self.files:
                f.write(struct.pack("<I", riot_hash(raf_file.path)))
                f.write(struct.pack("<I", data_file_offset))
                f.write(struct.pack("<I", raf_file.data_size))
                f.write(struct.pack("<I", self.paths.index(raf_file.path)))
                data_file_offset = data_file_offset + raf_file.data_size

            assert paths_list_offest == f.tell()

            # PATH LIST
            f.write(struct.pack("<I", paths_list_length))
            f.write(struct.pack("<I", len(self.paths)))

            # path list offset + 8 bytes for path_list_size adn
            # path_list count + 8 bytes for each path_data entry
            path_offset = paths_list_offest + 8 + len(self.paths) * 8

            paths_data = list()
            for path in self.paths:
                paths_data.append({
                    "path_offset": path_offset - paths_list_offest,
                    "path_length": len(path) + 1
                })
                path_offset = path_offset + len(path) + 1

            for path_data in paths_data:
                f.write(struct.pack("<I", path_data['path_offset']))
                f.write(struct.pack("<I", path_data['path_length']))

            for i in range(len(self.paths)):
                assert paths_list_offest + paths_data[i]['path_offset'] == f.tell()
                f.write(self.paths[i].encode('ascii') + b'\x00')

            assert eof == f.tell()

        # extract all data before opening any file descriptors for writing
        # raf_file might need to open file for reading before writing
        for raf_file in self.files:
            if(not raf_file.data):
                extracted_data = raf_file.extract()

        with open(save_path + ".dat", "wb") as f:
            for raf_file in self.files:
                f.write(raf_file.raw_data)

        # unload files to save memory
        for raf_file in self.files:
            raf_file.unload()


class RafArchive(BaseRafArchive):
    def __init__(self, path):
        super(RafArchive, self).__init__(path)
        self.open()


class RafCollection():
    def __init__(self, path):
        self.index = dict()
        self.root_path = path
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.raf'):
                absolute_file_path = os.path.join(root, filename)
                relpath = os.path.relpath(absolute_file_path, path)
                self.index[relpath] = RafArchive(absolute_file_path)
                self.index[relpath].relpath = relpath

    def search(self, text, **kwargs):
        return self.raffiles(search=text, **kwargs)

    def raffiles(self, search=None, caseinsensitive=True):
        raffiles = list()
        flags = 0
        if(caseinsensitive):
            flags = re.IGNORECASE

        sortlist = [(key, value) for key, value in self.index.items()]
        sortlist.sort(key=lambda i: (len(i[0]), i[0]))

        for relpath, rafarchive in sortlist:
            for path_in_raf, raffile in rafarchive.index.items():
                if(search is None or re.search(search, path_in_raf, flags=flags)):
                    raffiles.append(raffile)
        return raffiles


class RafInstallation(object):
    INSTALLATION_TYPICAL = {
        'windows': [
            "C:\Riot Games\League of Legends",
            "C:\League of Legends",
            "C:\Program Files\League of Legends",
            "C:\Program Files (x86)\League of Legends"
        ],
        'darwin': [
            "/Applications/League of Legends.app/",
            "~/Applications/League of Legends.app/",
        ]
    }
    FILE_ARCHIVE_POSSIBLE_PATHS = {
        'darwin': ('Contents', 'LoL', 'RADS', 'projects', 'lol_game_client', 'filearchives'),
        'windows': ('rads', 'projects', 'lol_game_client', 'filearchives')
    }

    def __init__(self, installation_path=None):
        self.platform = platform.system().lower()
        if(self.platform not in self.INSTALLATION_TYPICAL.keys()):
            raise Exception("Platform {} isn't supported, sorry. Currently only Windows and OSX is suported. {}".format(
                self.platform,
                self.platform == 'linux' and " Actually if you've managed to run LOL on Linux, even though it's not supported, you'll definitely be able to run Rafiki, which is a glorified python script, on Linux. Fell free to ping me at tom@doppnet.com!" or ""
            ))

        if(installation_path):
            if(os.path.exists(installation_path)):
                self.installation_path = installation_path
                self.installation_path_exists = True
            else:
                raise Exception("Installation path specified ({}) is incorrect".format(installation_path))
        else:
            possible_install_dirs = self.INSTALLATION_TYPICAL[self.platform]
            self.installation_path = possible_install_dirs[0]
            self.installation_path_exists = False
            for possible_dir in possible_install_dirs:
                if(os.path.exists(possible_dir)):
                    self.installation_path = possible_dir
                    self.installation_path_exists = True

    def get_raf_collection(self):
        if(not os.path.exists(self.installation_path)):
            raise Exception("Leauge of Legends installation path could not be found.")
        archives_path = os.path.join(self.installation_path, *self.FILE_ARCHIVE_POSSIBLE_PATHS[self.platform])
        return RafCollection(archives_path)
