RAFIKI - Riot Archive File extractor & packer
-------------------------------------------

Python API for reading and writing to a **raf** format used by RIOT's game Leauge of Legends. Developed on Linux, tested on Mac and Windows (for platform's native version of the game). Yeah, I think it's weird too.

Helper/Example Scripts
----------------------

Extract all files containing **hud** string in its path. This will create a new folder **extracted** wher relevant files will be placed (under their full RAF path):

    python rafiki.py extract -s path_to_lol/rads/projects/lol_game_client/filearchives -f "hud/elements" -o extracted
    
Find all files containing string **hud**, then search for file overrides in a folder named **extracted** and if an override exists, replace the file before packing everything back into archives. A new folder **overrides** will be created where relevant **raf** archives will be placed. You need to copy these files manually to actually include overrides in the game.

    python rafiki.py pack -s path_to_lol/rads/projects/lol_game_client/filearchives -f "hud/elements" -r extracted -o overrides
    
    
Note: Running on Windows
--------------------------

All above should run ok on Windows. Bear in mind you need to change all "/" to "\". Obviously you need to install [Python for Windows](http://www.python.org/getit/windows/)

You will most likely need a 64 bit version of python (and 64 bit version of Windows) as 32 bit version tends to come up with a Memory Error on writing **raf** files. Patches welcome
