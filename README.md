RAFIKI - Riot Archive File extractor & packer
-------------------------------------------

[![Build Status](https://travis-ci.org/tnajdek/rafiki.svg?branch=master)](https://travis-ci.org/tnajdek/rafiki)

Python API for reading and writing to a **raf** format used by RIOT's game Leauge of Legends. Tested on Mac and Windows (for platform's native version of the game).

*** This is low-level API exclusively for dealign with RAF files. If you're after multi-screen/ultrawide resolution support mod, see: [lol-eyefinity-hud-fixer](https://github.com/tnajdek/lol-eyefinity-hud-fixer).

Helper/Example Scripts
----------------------

Extract all files containing **hud** string in its path. This will create a new folder **extracted** wher relevant files will be placed (under their full RAF path):

    python bin/rafiki.py extract -s full/path/to/lol -f "hud/elements" -o extracted
    
Find all files containing string **hud**, then search for file overrides in a folder named **extracted** and if an override exists, replace the file before packing everything back into archives. A new folder **overrides** will be created where relevant **raf** archives will be placed. You need to copy these files manually to actually include overrides in the game.

    python bin/rafiki.py pack -s full/path/to/lol -f "hud/elements" -r extracted -o overrides
    
    
Note: Running on Windows
--------------------------

All above should run ok on Windows. Bear in mind you need to change all "/" to "\". Obviously you need to install [Python for Windows](http://www.python.org/getit/windows/)

You will most likely need a 64 bit version of python (and 64 bit version of Windows) as 32 bit version tends to come up with a Memory Error on writing **raf** files. Patches welcome.
