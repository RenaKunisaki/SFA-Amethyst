import typing
from ctypes import BigEndianStructure
import xml.etree.ElementTree as ET

class MyStruct(BigEndianStructure):
    """Extends Structure with XML methods."""

    def _dictToXml(self, name:str, obj:dict, enums:dict) -> ET.Element:
        result = ET.Element(name)
        for name, val in obj.items():
            self._objToXml(result, name, val, enums)
        return result


    def _objToXml(self, elem:ET.Element, name:str, obj:typing.Any,
    enums:dict) -> ET.Element:
        if name in enums:
            obj = enums[name](obj).name
        if hasattr(obj, 'toXml'):
            elem.append(obj.toXml())
        elif type(obj) is dict:
            elem.append(self._dictToXml(name, obj, enums))
        elif type(obj) in (list, tuple):
            # XXX improve this?
            elem.set(name, str(obj))
        else:
            elem.set(name, str(obj))
        return elem


    def toXml(self) -> ET.Element:
        """Build XML element for this struct."""
        fields = {}
        for field in self._fields_: # list to dict
            name, typ = field
            fields[name] = getattr(self, name)

        return self._dictToXml(
            type(self).__name__, fields,
            getattr(self, '_enums_', {}))
