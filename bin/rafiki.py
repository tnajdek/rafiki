#!/usr/bin/env python
import os
import sys
import argparse

from rafiki import RafCollection, RafInstallation
from rafiki.utils import mkdir_p, convert_lol_path

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description='Extract or Pack files from/to Riot Archive Format, optionally filtering extracted file paths')
parser.add_argument('action',
	metavar='action',
	type=str,
	choices=['extract', 'pack'],
	help='This is the desired action, either extract or pack'
)

parser.add_argument('-s',
	dest="source_path",
	required=True,
	help="Path to Leauge of Legends installation, required for both extracting and packaging. Will never be overriden or written to."
)

parser.add_argument('-o',
	dest='out_path',
	default=None,
	help='Target directory where extracted/packed files are places. **Existing files will be overwritten**'
)

parser.add_argument('-f',
	dest="filter",
	default=None,
	help="Only extract files with path containing **string**"
)

parser.add_argument("-r",
	dest="override",
	default=None,
	help="**When packaging up RAFs looks for a matching paths for overrides. If found an override will be packed in instead of the original file"
)

args = parser.parse_args()

basepath = args.out_path
if(not args.out_path):
	if(args.action == "extract"):
		basepath = "extracted"
	else:
		basepath = "packed"

if(not os.path.isabs(basepath)):
	basepath = os.path.join(SCRIPT_ROOT, basepath)

if(not os.path.isdir(args.source_path)):
	print('"%s" is not a directory, please provide full path to Leauge of Legends' % args.source_path)
	sys.exit()


try:
	ri = RafInstallation(args.source_path)
	collection = ri.get_raf_collection()
except Exception:
	print("Unable to find filearchives in \"%s\", are you sure this is valid path to Leauge of Legends?" % args.source_path)
	sys.exit()


if(args.filter):
	files = collection.search(args.filter)
else:
	files = collection.archives()

if(args.action == 'extract'):
	for raf_file in files:
		data = raf_file.extract()
		raf_file_path = convert_lol_path(raf_file.path)
		mkdir_p(basepath + os.sep + os.path.dirname(raf_file_path))
		with open(basepath + os.sep + raf_file_path, 'wb') as target_file:
			target_file.write(data)

if(args.action == 'pack'):
	archives = set()
	for raf_file in files:
		raf_file_path = convert_lol_path(raf_file.path)
		file_path = os.path.join(args.override, raf_file_path)
		try:
			with open(file_path, 'rb') as f:
				raf_file.insert(f.read())
			print("Using override for %s in %s" % (raf_file.path, raf_file.archive.path))
		except IOError:
			pass
		archives.add(raf_file.archive)

	for archive in archives:
		archive_override_path = os.path.join(basepath, archive.relpath)
		mkdir_p(os.path.dirname(archive_override_path))
		print("Writing archive \"%s\"" % archive_override_path)
		archive.save(archive_override_path)
