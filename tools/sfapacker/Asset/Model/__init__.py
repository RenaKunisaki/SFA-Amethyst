# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
from sfapacker.Asset import Asset

class Model(Asset):
    """A 3D model."""

    def __init__(self, id):
        super().__init__(id = id)
