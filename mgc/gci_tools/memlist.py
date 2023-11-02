"""Defines Melee's memory regions (for PAL support)."""

BLOCK_LIST = [          #GCI block offset list
        0x02060,        #Block 0
        0x04060,        #Block 1
        0x06060,        #Block 2
        0x08060,        #Block 3
        0x0a060,        #Block 4
        0x0c060,        #Block 5
        0x0e060,        #Block 6
        0x10060,        #Block 7
        0x12060,        #Block 8
        0x14060,        #Block 9
        ]

BLOCK_SIZE = [0, 0x1f2c, 0x1f2c, 0x1f2c, 0x1f2c, 0x1f2c, 0x1f2c, 0x1f2c, 0, 0x1790]


def get_mem_list(pal: bool) -> []:
    """List of Melee memory addresses."""
    MEM_LIST = [  # Melee start address for each GCI block
        0x00000000,  # Block 0 (not in memory)
        0x8045d6b8,  # Block 1
        0x8045f5e4,  # Block 2
        0x80461510,  # Block 3
        0x8046343c,  # Block 4
        0x80465368,  # Block 5
        0x80467294,  # Block 6
        0x804691c0,  # Block 7
        0x00000000,  # Block 8 (not in memory)
        0x8045bf28,  # Block 9
    ]

    MEM_LIST_PAL = [  # PAL Melee start address for each GCI block
        0x00000000,  # Block 0 (not in memory)
        0x8045d6b8 - 0xf1f8,  # Block 1
        0x8045f5e4 - 0xf1f8,  # Block 2
        0x80461510 - 0xf1f8,  # Block 3
        0x8046343c - 0xf1f8,  # Block 4
        0x80465368 - 0xf1f8,  # Block 5
        0x80467294 - 0xf1f8,  # Block 6
        0x804691c0 - 0xf1f8,  # Block 7
        0x00000000,  # Block 8 (not in memory)
        0x8045bf28 - 0xf1f8,  # Block 9
    ]

    if not pal:
        return MEM_LIST
    else:
        return MEM_LIST_PAL

class MemList:
    """Keeps track of memory addresses."""

    def __init__(self, pal: bool):
        self.mem_list = get_mem_list(pal)
        self.block_list = BLOCK_LIST
        self.block_size = BLOCK_SIZE
        self.block_start = self.mem_list[0]
        self.block_end = self.mem_list[9] + self.block_size[9]
        self.mem_start = self.mem_list[9]
        self.mem_end = self.mem_list[7] + self.block_size[7]
