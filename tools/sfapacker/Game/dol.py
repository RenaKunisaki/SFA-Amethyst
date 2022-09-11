import struct

class DOL:
    """A DOL-format executable."""

    NUM_TEXT_SECTIONS = 7
    """Number of .text sections in a DOL file"""

    NUM_DATA_SECTIONS = 11
    """Number of .data sections in a DOL file"""

    path:str = None
    """Path to the DOL file."""

    file = None
    """The DOL file handle."""

    textSections:list[dict] = None
    """The .text sections offsets, RAM addresses, and sizes."""

    dataSections:list[dict] = None
    """The .data sections offsets, RAM addresses, and sizes."""

    bssAddr = 0
    """The RAM address of .bss section."""

    bssSize = 0
    """The size of .bss section."""

    entryPoint = 0
    """The RAM address of the program entry point."""


    def __init__(self, path:str) -> None:
        self.path         = path
        self.file         = open(path, 'rb')
        self.textSections = []
        self.dataSections = []
        self.bssAddr      = 0
        self.bssSize      = 0
        self.entryPoint   = 0
        self._readHeader()


    def _readHeader(self):
        """Read the DOL header."""
        sections = []
        nSections = self.NUM_TEXT_SECTIONS + self.NUM_DATA_SECTIONS

        for i in range(nSections):
            sections.append({
                'offset': struct.unpack('>I', self.file.read(4))[0], # grumble
            })

        for i in range(nSections):
            sections[i]['addr'] = struct.unpack('>I',
                self.file.read(4))[0] # grumble

        for i in range(nSections):
            sections[i]['size'] = struct.unpack('>I',
                self.file.read(4))[0] # grumble

        for i in range(self.NUM_TEXT_SECTIONS):
            self.textSections.append(sections[i])
        for i in range(self.NUM_DATA_SECTIONS):
            self.dataSections.append(sections[i+self.NUM_TEXT_SECTIONS])

        self.bssAddr, self.bssSize, self.entryPoint = struct.unpack('>3I',
            self.file.read(12))

    def addrToSection(self, addr:int) -> dict:
        """Determine which section a RAM address is in.

        :param addr: RAM address.
        :returns: Section or None.
        """
        for section in self.textSections + self.dataSections:
            if (addr >= section['addr']
            and addr <  section['addr']+section['size']):
                return section
        return None

    def addrToOffset(self, addr:int) -> int:
        """Determine the file offset corresponding to a RAM address.

        :param addr: RAM address.
        :returns: File offset, or None.
        """
        section = self.addrToSection(addr)
        if section is None: return None
        return (addr - section['addr']) + section['offset']

