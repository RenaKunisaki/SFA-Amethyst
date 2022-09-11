# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
from collections import OrderedDict
from ctypes import sizeof, Structure
from ..GX.GX import GX

class Model:
    """A model (character or map block) in the game."""

    RenderStreamOrder:OrderedDict[str,str] = {}
    """List of stream name => mesh name suffix, in the order they
    should be parsed.
    """
    # not using regular dict (which guarantees order since 3.7)
    # since I'm not certain which version Blender uses

    name:str = ""
    """The model's internal name."""

    renderStreams:dict[str,bytes] = {}
    """The raw data of each render stream."""

    def __init__(self, gx:GX) -> None:
        self.gx = gx


    def readFromFile(self, file, path:str) -> Model:
        """Read the model from the given file.

        :param file: File to read from.
        :param path: File's path.
        :returns: The model.
        """
        raise NotImplementedError # this is only a base class


    def _readObjects(self, dType:Structure, file, offset, count) \
    -> list[Structure]:
        """Read an array of objects.

        :param dType: The object class to read.
        :param file: The file to read from.
        :param offset: The offset to read from.
        :param count: The number of objects.
        :returns: The object instances.
        """
        result = []
        file.seek(offset)
        for _ in range(count):
            result.append(dType.from_buffer_copy(
                    file.read(sizeof(dType))))
        return result
