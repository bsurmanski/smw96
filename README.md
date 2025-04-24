# Super Mario World Missing Exit Finder
Ever play SMW and get to 95 out of 96 exits, and it's unclear what level 
you need to beat? Then this tool is for you!

# How to Use

This tool uses a savefile (SRAM dump). If using an emulator, this should be a .srm file. (unforunately savestates are unsupported at this time). Provide the save file with the -f flag.

`python smw96.py -f "Super Mario World (USA).srm"`

This should print out something like:

```
95 exits found. 1 remaining
-- missing paths --
none
-- missing events --
Forest Ghost House (secret)
```

# Commandline Options

* -f FILENAME - the filename
* -s {A,B,C} - the save entry (Mario A, Mario B, Mario C) to check
* -o OFFSET - arbitrary byte offset in the file where the save structure is (usable for savestates?)

# Restrictions and Future Work

* This only works with .sav files, not save states.

The RAM format and SRAM format is the same, so if the correct offset is found in the savestate,
this tool should work.

* This tool is poorly tested! There is likely bugs. It's read-only, so nothing harmful should happen but crashes and wrong answers are possible.