import argparse

# snippet from an 100% save SRAM.
# See: https://www.smwcentral.net/?p=memorymap&game=smw&region=sram
# relevant:
# 96 bytes overworld level flags
# 15 bytes overworld event flags (bitwise)
# 29 bytes irrelevant
# 1 byte: # events triggered.
#
# each level flag is 1 byte: bmesudlr
# b - level beaten
# m - midway passed
# e,s - unused
# u,d,l,r - can move up down left right
#
# each event flag maps to an exit clear, and this is actually
# what is counted on the save file. each 'event' is a single bit.
good_save = bytes.fromhex("""
00 83 83 04 8F 87 89 8A 81 8E 8D 83 83 C3 87 87
86 8C 04 8D 84 CE 08 00 8A 00 8E 85 89 8A 01 83
85 85 8A 8F 8E 89 8C 85 03 89 8A 85 01 8E 8C 85
05 06 04 8D 8E 8C 00 89 8B 8B 83 83 8D CC 87 88
8C 87 8B 8D 8F 83 8C 87 01 83 83 83 83 01 83 83
83 83 03 05 8A 04 89 06 86 85 8B 09 0A 00 00 00
7F FF FF FF FF FF FD FF C3 FF 6D B6 F7 F8 00 00
00 02 00 02 00 58 00 A8 00 58 00 A8 00 05 00 0A
00 05 00 0A 00 01 01 01 01 00 00 00 60 B2 24 00
""".replace(" ", "").replace("\n", "").strip())

# Found in Lunar Magic
levels = [
    'bonus room',       # 0
    'Vanilla Secret 2',
    'Vanilla Secret 3',
    'TOP SECRET AREA',
    'Donus Ghost House',
    'Donut Plains 3',
    'Donut Plains 4',
    'Castle 2, Morton',
    'Green Switch Palace',
    'Donut Plains 2',
    'Donut Secret 1',
    'Vanilla Fortress',
    'Butter Bridge 1',
    'Butter Bridge 2',
    'Ludwig Castle',
    'Cheese Bridge',
    'Cookie Mountain', # 0x10
    'Soda Lake',
    '0x12 - Star Warp',
    'Donut Secret House',
    'Yellow Switch Palace',
    'Donut Plains 1',
    '0x16 - Star Warp',
    '0x17???',
    'Sunken Ghost Ship',
    '0x19???',
    'Castle 6 Wendy',
    'Chocolate Fortress',
    'Chocolate Island 5',
    'Choclate Island 4',
    '0x1E - Star Warp',
    'Forest Fortress',
    'Castle 5 Roy', # 0x20
    'Choco Ghost House',
    'Choc Island 1',
    'Choc Island 3',
    'Choc Island 2',
    'Castle 1, Iggy', # 0x101 (0x25-0x100, unused)
    'Yoshis Island 4',
    'Yoshis Island 3',
    'Yoshis House',
    'Yoshis Island 1',
    'Yoshis Island 2',
    'Vanilla Ghost House',
    '0x108 - Star Warp',
    'Vanilla Secret 1',
    'Vanilla Dome 3',
    'Donut Secret 2',
    '0x10c - Star Warp',
    'Front Door (Bowser)',
    'Back Door (Bowser)',
    'Valley of Bowser 4',
    'Castle 7 Larry', #0x110
    'Valley Fortress',
    '0x112',
    'Valley of Bowser 3',
    'Valley Ghost House',
    'Valley of Bowser 2',
    'Valley of Bowser 1',
    'Chocolate Secret',
    'Vanilla Dome 2',
    'Vanilla Dome 4',
    'Vanilla Dome 1',
    'Red Switch Palace',
    'Castle 3 Lemmy',
    'Forest Ghost House',
    '0x11e',
    'Forest of Illusion 4',
    'Forest of Illusion 2', #0x120
    'Blue Switch Palace',
    'Forest Secret Area',
    'Forest of Illusion 3',
    '0x124 - Star Warp',
    'Funky',
    'Outrageous',
    'Mondo',
    'Groovy',
    '0x129 - Star Warp',
    'Gnarly',
    'Tubular',
    'Way Cool',
    'Awesome',
    '0x12e - Star Warp',
    '0x12f - Star Warp',
    'Star World 2',
    '0x131 - Star Warp',
    'Star World 3',
    '0x133 - Star Warp',
    'Star World 1',
    'Star World 4',
    'Star World 5',
    '0x137 - Star Warp',
    '0x138 - Star Warp',
    '', '', '', '', ''
]

# Found in Lunar Magic
events = {
    0x53: "Star Road (top left)",
    0x54: "Star World 2",
    0x56: "Star Road (top)",
    0x57: "Star World 3",
    0x59: "Star road (top right)",
    0x5a: "Star World 4",
    0x5c: "Star road (bot right)",
    0x4d: "Star World 5",
    0x50: "Star road (bot left)",
    0x51: "Star World 1",
    0x30: "Forest Ghost House",
    0x2a: "Forest of Illusion 1",
    0x32: "Forest of Illusion 4",
    0x34: "Forest Secret Area",
    0x2e: "Forest of Illusion 3",
    0x2c: "Forest of Illusion 2",
    0x63: "Chocolate Island 1",
    0x46: "Chocolate Island 2",
    0x48: "Chocolate Island 3",
    0x4a: "Chocolate Fortress",
    0x02: "Yellow Switch",
    0x28: "Green Switch",
    0x29: "Red Switch",
    0x37: "Blue Switch",
    0x41: "Valley Fortress",
    0x3b: "Valley Ghost House",
    0x12: "Donut Secret (Ghost) House",
    0x0b: "Donut Ghost House",
}

class LevelSetting:
    def __init__(self, b):
        self.raw = b
        self.beaten = b & 0x80
        self.midway = b & 0x40
        self.up = b & 0x08
        self.down = b & 0x04
        self.left = b & 0x02
        self.right = b & 0x01

    def __eq__(self, other):
        if not isinstance(other, LevelSetting):
            return NotImplemented
        return self.beaten == other.beaten and\
            self.up == other.up and\
            self.down == other.down and\
            self.left == other.left and\
            self.right == other.right

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"beaten: {self.beaten == 0x80}, udlr: {bin(self.raw & 0x0f)}"

def main(fname, offset=0):
    bad_save = ""
    with open(fname, 'rb') as file:
        bad_save = file.read()[offset:]
    print(f"{bad_save[0x8c]} exits found. {96 - bad_save[0x8c]} remaining")

    print("-- missing paths --")
    printed = False
    for i in range(0, 96):
        gsb = LevelSetting(good_save[i])
        bsb = LevelSetting(bad_save[i])
        level_index = i #- 0xdc if i > 0x24 else i
        if gsb != bsb: # uses comparator
            out = ""
            if gsb.beaten and not bsb.beaten:
                out += "unbeaten. "
            if gsb.midway and not bsb.midway:
                out += "midway. "
            if gsb.left != bsb.left or gsb.right != bsb.right or gsb.up != bsb.up or gsb.down != bsb.down:
                out += "cannot move "
                if gsb.left and not bsb.left:
                    out += "left;"
                if gsb.right and not bsb.right:
                    out += "right;"
                if gsb.up and not bsb.up:
                    out += "up;"
                if gsb.down and not bsb.down:
                    out += "down"
            print(f"{levels[level_index]}, - {out}")
            printed = True
        # TODO: enable this in a 'debug' option...
        # elif good_save[i] != bad_save[i]:
        #    print(f"{levels[level_index]}, - somethings up {good_save[i] - bad_save[i]}")
    if not printed:
        print("none")
    
    printed = False
    unknown_events = []
    print("-- missing events --")
    for i in range(0x60, 0x60 + 15):
        if good_save[i] != bad_save[i]:
            for j in range(0,8): # bit
                if (good_save[i] & 1 << j) != (bad_save[i] & 1 << j):
                    event_num = (i - 0x60) * 8 + (8-j)
                    level_name = ""
                    if event_num in events:
                        level_name = events[event_num]
                    elif event_num - 1 in events: # secret exits are event# + 1
                        level_name = events[event_num - 1] + " (secret)"
                    else:
                        unknown_events.append(event_num)
                        continue
                    print(f'{level_name}')
                    printed = True
    if unknown_events:
        print("other events: " + ",".join([hex(e) for e in unknown_events]))
        printed = True
    if not printed:
        print("none - this file is 100%!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A program to find missing exits in a SMW Save")
    parser.register("type", "hexint", lambda s: int(s, 16))
    parser.add_argument("-f", "--filename", help="Save file to check.", default="Super Mario World (USA).srm")
    parser.add_argument("-s", "--savename", help="Mario A, B or C.", choices=["A","B", "C"], default="A")
    parser.add_argument("-o", "--offset", help="Arbitrary byte offset in savefile (in hex). Can be used if you have a savestate and know where the save data is. 0x12af0 worked for a snes9x save state.", type="hexint", default="0x00")
    args = parser.parse_args()
    save_offset = {"B": 0x8f, "C": 0x11e}.get(args.savename, 0)
    main(args.filename, args.offset + save_offset)
