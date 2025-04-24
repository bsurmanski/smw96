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

For use with save states, you need to know the offset to overworld level flags. For my version of SNES9x, the offset '0x12af0' worked. This likely differs based on emulator and version.

`python smw96.py -f 'Super Mario World (USA).state98' -o 0x12af0`

# Commandline Options

* -f FILENAME - the filename
* -s {A,B,C} - the save entry (Mario A, Mario B, Mario C) to check
* -o OFFSET - arbitrary byte offset (in hex) in the file where the save structure is (usable for savestates)

## Unknown Event 

You may see an output like the following:

`other events: 0x8,0x7,0x6,0x5,0x4,0x10,0xf,0xd,0xa,0x9,0x18,0x17`

each event represents a level exit. The levels here should already be represented in the `missing paths` section. I only bothered mapping exit that don't create new paths, and so wouldn't show up in the existing `missing paths` list.

# Restrictions and Future Work

* This tool is poorly tested! There is likely bugs. It's read-only, so nothing harmful should happen but crashes and wrong answers are possible.