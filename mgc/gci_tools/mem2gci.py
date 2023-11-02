"""mem2gci.py: Translates Melee memory addresses to their corresponding location in an unpacked GCI, and vice-versa."""

from typing import List, Tuple

# state.mem_list.block_list = [          #GCI block offset list
#         0x02060,        #Block 0
#         0x04060,        #Block 1
#         0x06060,        #Block 2
#         0x08060,        #Block 3
#         0x0a060,        #Block 4
#         0x0c060,        #Block 5
#         0x0e060,        #Block 6
#         0x10060,        #Block 7
#         0x12060,        #Block 8
#         0x14060,        #Block 9
#         ]
# 
# state.mem_list.mem_list = [            #Melee start address for each GCI block
#         0x00000000,     #Block 0 (not in memory)
#         0x8045d6b8,     #Block 1
#         0x8045f5e4,     #Block 2
#         0x80461510,     #Block 3
#         0x8046343c,     #Block 4
#         0x80465368,     #Block 5
#         0x80467294,     #Block 6
#         0x804691c0,     #Block 7
#         0x00000000,     #Block 8 (not in memory)
#         0x8045bf28,     #Block 9
#         ]
# 
# state.mem_list.mem_list_PAL = [                 #PAL Melee start address for each GCI block
#         0x00000000,              #Block 0 (not in memory)
#         0x8045d6b8 - 0xf1f8,     #Block 1
#         0x8045f5e4 - 0xf1f8,     #Block 2
#         0x80461510 - 0xf1f8,     #Block 3
#         0x8046343c - 0xf1f8,     #Block 4
#         0x80465368 - 0xf1f8,     #Block 5
#         0x80467294 - 0xf1f8,     #Block 6
#         0x804691c0 - 0xf1f8,     #Block 7
#         0x00000000,              #Block 8 (not in memory)
#         0x8045bf28 - 0xf1f8,     #Block 9
#         ]
# 
# state.mem_list.block_size = [0, 0x1f2c, 0x1f2c, 0x1f2c, 0x1f2c, 0x1f2c, 0x1f2c, 0x1f2c, 0, 0x1790]
# state.mem_list.block_start = state.mem_list.block_list[0]
# state.mem_list.block_end = state.mem_list.block_list[9] + state.mem_list.block_size[9]
# state.mem_list.mem_start = state.mem_list.mem_list[9] # Memory starts with block 9 for some reason
# state.mem_list.mem_end = state.mem_list.mem_list[7] + state.mem_list.block_size[7]

def mem2gci_tuple(state: 'CompilerState', mem_address: int) -> Tuple[int, int]:
    """Takes a Melee memory address and returns the corresponding unpacked GCI
       block number and offset."""
    if mem_address < state.mem_list.mem_start or mem_address >= state.mem_list.mem_end:
        raise ValueError("Melee address 0x%08x does not have a corresponding GCI location" % mem_address)
    block_number = -1
    offset = 0
    for index, block_address in enumerate(state.mem_list.mem_list):
        offset = mem_address - block_address
        if offset >= state.mem_list.block_size[index] or offset < 0: continue
        block_number = index
        break
    if block_number < 0:
        raise ValueError("Melee address 0x%08x does not have a corresponding GCI location" % mem_address)
    return block_number, offset

def mem2gci(state: 'CompilerState', mem_address: int) -> int:
    """Takes a Melee memory address and returns the corresponding unpacked GCI
    location."""
    block_number, offset = mem2gci_tuple(state, mem_address)
    return state.mem_list.block_list[block_number] + offset

def gci2mem(state: 'CompilerState', gci_address: int) -> int:
    """Takes a GCI offset address and returns the corresponding Melee memory
       location."""
    if gci_address < state.mem_list.block_start or gci_address >= state.mem_list.block_end:
        raise ValueError("GCI address 0x%05x does not have a corresponding Melee memory location" % gci_address)
    block_number = -1
    offset = 0
    for index, block_address in enumerate(state.mem_list.block_list):
        offset = gci_address - block_address
        if offset >= state.mem_list.block_size[index] or offset < 0: continue
        block_number = index
        break
    if block_number < 0:
        raise ValueError("GCI address 0x%05x does not have a corresponding Melee memory location" % gci_address)
    return state.mem_list.mem_list[block_number] + offset

def data2gci(state: 'CompilerState', data: bytes) -> List[Tuple[int, bytes]]:
    """Takes a Melee address and bytes of data, and returns them in a list of
    GCI offsets and data blocks that correspond exactly to where the data
    should go in the GCI."""
    if not data:
        raise ValueError("Data length must be greater than 0.")
    if state.pointer < state.mem_list.mem_start:
        raise ValueError("Start address 0x%08x is not present in the GCI; earliest possible start address is 0x%08x" % (state.pointer, state.mem_list.mem_start))
    if state.pointer + len(data) > state.mem_list.mem_end:
        raise ValueError("Data ends at 0x%08x which overflows the last address present in the GCI (0x%08x)" % (state.pointer + len(data), state.mem_list.mem_end))
    current_address = state.pointer
    remaining_data = len(data)
    gci_list: List[Tuple[int, bytes]] = []
    data_pointer = 0
    while remaining_data > 0:
        current_block_number, current_offset = mem2gci_tuple(state, current_address)
        current_gci_address = state.mem_list.block_list[current_block_number] + current_offset
        amount_block_can_fit = state.mem_list.block_size[current_block_number] - current_offset
        gci_list.append((current_gci_address, data[data_pointer:data_pointer+min(remaining_data, amount_block_can_fit)]))
        remaining_data -= amount_block_can_fit
        current_address += amount_block_can_fit
        data_pointer += amount_block_can_fit
    return gci_list

