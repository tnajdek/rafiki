Riot Archive File
-----------------

Python API for reading and writing to a **raf** format used by RIOT's game Leauge of Legends. Code is still in development and might need some cleanup, patches welcome. Developed on Linux, tested on Mac and Windows (for platform's native version of the game). Yeah, I think it's weird too.

** THIS IS EARLY DEVELOPMENT VERSION. THERE WILL BE BUGS ** 

Helper/Example Scripts
----------------------

Extract all files containing **hud2012** string in its path. This will create a new folder **extracted** wher relevant files will be placed (under their full RAF path):

    python extract.py path_to_lol/rads/projects/lol_game_client/filearchives "hud2012"
    
Find all files containing string **hud2012**, then search for file overrides in a folder named **extracted** and if an override exists, replace the file before packing everything back into archives. A new folder **overrides** will be created where relevant **raf** archives will be placed. You need to copy these files manually to actually include overrides in the game.

    python pack.py path_to_lol/rads/projects/lol_game_client/filearchives "hud2012" extracted
    
    
Note: Running on Windows
--------------------------

All above should run ok on Windows. Bear in mind you need to change all "/" to "\". Obviously you need to install [Python for Windows](http://www.python.org/getit/windows/)

