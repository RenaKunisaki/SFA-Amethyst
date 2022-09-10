# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
import os
import os.path
from PIL import Image
import struct
import xml.etree.ElementTree as ET
from sfapacker.Asset import Asset
from sfapacker.BinaryFile import BinaryFile
from .Header import Header
from .texture import decode_image, encode_image
from .GX import GX

class TextureFrame(Asset):
    """One frame of a texture."""

    header: Header = None
    """The raw header from the game's texture file."""

    imageData: bytes = None
    """The raw image imageData from the game's texture file."""

    frameNo: int = None
    """Which frame of the texture this is."""

    def __init__(self, id):
        super().__init__(id = id)


    @staticmethod
    def fromTexture(texture, frameNo, imageData) -> TextureFrame:
        """Instantiate TextureFrame from Texture.
        """
        self = TextureFrame(texture.id)
        self.frameNo = frameNo

        # read the header
        self.header = Header.from_buffer_copy(imageData)
        self.imageData = imageData[0x60:]

        # decode the image imageData
        self.image = decode_image(self.imageData,
            None, # palette_data
            GX.ImageFormat(self.header.format), # image_format
            None, # palette_format
            0, # num_colors (for palettes)
            self.header.width, self.header.height)

        # XXX this isn't correct, but does work most of the time...
        # I think the actual way to do this is "don't".
        #if self.header.mipmapVar1D & 1:
        #    self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

        return self


    @staticmethod
    def fromImage(path:str, id:int, eFrame:ET.Element) -> TextureFrame:
        """Instantiate TextureFrame from file on disk.

        :param path: Path to image file.
        :param id: Texture ID.
        :param eFrame: XML element containing the attributes.
        """
        self = TextureFrame(id)
        self.image   = Image.open(path)
        self.frameNo = eFrame.get('n', 0)
        texObj = GX.TexObj(mode0=0, mode1=0, image0=0, image3=0,
            userData=0, format=0, tlutName=0, loadCnt=0,
            loadFmt=0, flags=0,
        )
        self.header  = Header(
            frameVal10    = int(eFrame.get('frameVal10'),    0),
            framesPerTick = int(eFrame.get('framesPerTick'), 0),
            minLod        = int(eFrame.get('minLod'),        0),
            maxLod        = int(eFrame.get('maxLod'),        0),
            unk1E         = int(eFrame.get('unk1E'),         0),
            tevVal50      = int(eFrame.get('tevVal50'),      0),
            format        = GX.ImageFormat[eFrame.get('format')].value,
            wrapS         = GX.WrapMode   [eFrame.get('wrapS')].value,
            wrapT         = GX.WrapMode   [eFrame.get('wrapT')].value,
            minFilter     = GX.FilterMode [eFrame.get('minFilter')].value,
            magFilter     = GX.FilterMode [eFrame.get('magFilter')].value,
            width         = self.image.size[0],
            height        = self.image.size[1],
            usage         = 1, # ref count, always 1 in file
            texObj        = texObj,
            # I can't find any documentation about whether other fields
            # will be initialized to a particular value, so let's assume
            # they won't be.
            next=0, flags=0, xOffset=0, unk12=0, unk1B=0,
            unk1F=0, texRegion=0, bufSize=0,
            bNoTexRegionCallback=0, bDoNotFree=0, unk4A=0,
            unk4B=0, size=0,
        )
        return self


    def toBinary(self) -> bytes:
        """Convert to game binary format.

        :return: The binary data.
        """
        # I don't think this game even supports palettes...
        imageData, paletteData, colors = encode_image(
            self.image, self.header.format, None,
            mipmap_count=self.header.maxLod - self.header.minLod)
        self.imageData = imageData.getbuffer()
        data = self._compress(bytes(self.header) + self.imageData)
        # pad to multiple of 32 bytes (XXX necessary?)
        pad = 32 - (len(data) & 0x1F)
        if pad >= 32: pad = 0
        if pad > 0: data += b'\0' * pad
        return data


    def toXml(self) -> ET.Element:
        """Make XML element for this frame.

        Result contains the header information but not the
        actual image imageData.
        """

        # copy only necessary header elements
        H = self.header
        return ET.Element('TextureFrame', {
            'n':                    str(self.frameNo),
            #'next':                 str(H.next), # always 0
            #'flags':                str(H.flags), # always 0
            #'xOffset':              str(H.xOffset), # always 0
            #'width':                str(H.width),
            #'height':               str(H.height),
            #'usage':                str(H.usage), # always 1
            'frameVal10':           str(H.frameVal10),
            #'unk12':                str(H.unk12), # always 0
            'framesPerTick':        str(H.framesPerTick),
            'format':               GX.ImageFormat(H.format).name,
            'wrapS':                GX.WrapMode(H.wrapS).name,
            'wrapT':                GX.WrapMode(H.wrapT).name,
            'minFilter':            GX.FilterMode(H.minFilter).name,
            'magFilter':            GX.FilterMode(H.magFilter).name,
            #'unk1B':                str(H.unk1B), # always 0
            'minLod':               str(H.minLod),
            'maxLod':               str(H.maxLod),
            'unk1E':                str(H.unk1E), # unused?
            #'unk1F':                str(H.unk1F), # always 0
            #'texRegion':            str(H.texRegion), # always 0
            #'bufSize':              str(H.bufSize), # always 0
            #'bNoTexRegionCallback': str(H.bNoTexRegionCallback), # always 0
            #'bDoNotFree':           str(H.bDoNotFree), # always 0
            #'unk4A':                str(H.unk4A), # always 0
            #'unk4B':                str(H.unk4B), # always 0
            #'size':                 str(H.size), # always 0
            'tevVal50':             str(H.tevVal50),

            # all always 0
            #'texObj_mode0':    str(H.texObj.mode0),
            #'texObj_mode1':    str(H.texObj.mode1),
            #'texObj_image0':   str(H.texObj.image0),
            #'texObj_image3':   str(H.texObj.image3),
            #'texObj_userData': str(H.texObj.userData),
            #'texObj_format':   str(H.texObj.format),
            #'texObj_tlutName': str(H.texObj.tlutName),
            #'texObj_loadCnt':  str(H.texObj.loadCnt),
            #'texObj_loadFmt':  str(H.texObj.loadFmt),
            #'texObj_flags':    str(H.texObj.flags),
        })


class Texture(Asset):
    """A texture asset."""

    nFrames: int = None
    """Number of frames."""

    frames: list[TextureFrame] = None
    """The individual frames."""

    DIR_NAMES = ('TEX0', 'TEX1', 'TEXPRE')

    def __init__(self, id:int, nFrames:int, whichFile:int):
        """Construct Texture.

        :param id: The texture ID.
        :param nFrames: Number of frames this texture has.
        :param whichFile: Which file this texture comes from:
            0=TEX0, 1=TEX1, 2=TEXPRE
        """
        super().__init__(
            name = 'tex%04X' % id,
            id   = id,
        )
        self.nFrames   = nFrames
        self.frames    = []
        self.whichFile = whichFile


    @staticmethod
    def fromImages(path:str, eTexture:ET.Element) -> Texture:
        """Instantiate Texture from files on disk.

        :param path: Path to directory containing image files.
        :param eTexture: XML element containing the attributes.
        """
        frames = eTexture.findall('TextureFrame')
        fid, tid = eTexture.get('id').split(':')
        self = Texture(int(tid, 16), len(frames), int(fid, 16))
        orderedFrames = {} # idx => Frame
        for eFrame in frames:
            iFrame = int(eFrame.get('n'), 0)
            pFrame = '%04X.%02X.png' % (self.id, iFrame)
            dName  = self.DIR_NAMES[self.whichFile]
            orderedFrames[iFrame] = TextureFrame.fromImage(
                os.path.join(path, dName, pFrame), iFrame, eFrame)
        for i in range(len(frames)):
            if i not in orderedFrames:
                raise FileNotFoundError(
                    "Frame 0x%X missing from texture %X:%04X" % (
                        i, self.whichFile, self.id))
            self.frames.append(orderedFrames[i])
        return self


    def toBinary(self) -> bytes:
        """Convert to game binary format.

        :return: The binary data.
        """
        assert len(self.frames) > 0
        if len(self.frames) == 1:
            return self.frames[0].toBinary()
        # otherwise there's an offset list first
        frameData = []
        offsets   = []
        offset    = len(self.frames) * 4 # length of offset list
        for frame in self.frames:
            offsets.append(struct.pack('>I', offset))
            data = frame.toBinary()
            assert len(data) > 0
            offset += len(data)
            frameData.append(data)
        return b''.join(offsets) + b''.join(frameData)


    def unpackFromFile(self, file:BinaryFile,
    offset:int=None) -> Texture:
        """Read texture from game file.

        :param file: File to read from.
        :param offset: Offset to read from. If None, use
            file's current offset.
        :return: The decoded texture.
        """
        if offset is not None: file.seek(offset)
        offset = file.tell()

        if self.nFrames > 1:
            # offset is the location of more offsets.
            offsets = file.readu32(self.nFrames)
        else: offsets = [0] # no offsets, just an archive

        # decompress the actual textures
        for iFrame, frameOffs in enumerate(offsets):
            file.seek(offset + frameOffs)
            imageData, extParams = self._decompress(file)
            self.frames.append(TextureFrame.fromTexture(
                self, iFrame, imageData))

        return self


    def unpackToDir(self, path:str) -> None:
        """Write decoded texture to file(s).

        :param path: Directory to write to.

        Writes each frame of the texture to a file in
        the specified directory with a name in the
        format '%04X.%02X.png', where the first parameter
        is the texture ID (not index) and the second is
        the frame number.
        """
        for iFrame, frame in enumerate(self.frames):
            name = '%04X.%02X.png' % (self.id, iFrame)
            dName = self.DIR_NAMES[self.whichFile]
            try: os.mkdir(os.path.join(path, dName))
            except FileExistsError: pass
            frame.image.save(os.path.join(path, dName, name))


    def toXml(self) -> ET.Element:
        """Make XML element for this texture.

        Result contains the header information but not the
        actual image imageData.
        """
        elem = ET.Element('Texture', {
            'id': '%X:%04X' % (self.whichFile, self.id),
        })
        for frame in self.frames:
            elem.append(frame.toXml())
        return elem


