#!/usr/bin/env python3
"""Read gamebits.xml and produce bitnames.dat."""
import os
import sys
import xml.etree.ElementTree as ET
ENTRY_LEN = 24
MAX_ID = 0

names = {}
seenName = set()
gameBits = ET.parse(sys.argv[1]).getroot()
for bit in gameBits.findall('./bit'):
    id = int(bit.get('id'), 0)
    MAX_ID = max(MAX_ID, id)
    name = bit.get('name')
    if name is not None and name != '' and name in seenName:
        print("WARNING: Duplicate GameBit name: '" + str(name) + "'")
    seenName.add(name)
    names[id] = name
if len(seenName) == 0:
    sys.stderr.write("No gamebits found. Try removing xmlns attribute from gamebits.xml\n")
    sys.exit(1)

with open(sys.argv[2], 'wb') as outFile:
    for i in range(MAX_ID+1):
        name = names.get(i, '')
        if name is None: name = ''
        #name = bytes(name[0:ENTRY_LEN], 'utf-8').ljust(ENTRY_LEN, b'\0')
        name = bytes(name, 'utf-8') + b'\0'
        outFile.write(name)
