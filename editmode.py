
from enum import Enum, auto

class EditMode(Enum):
    SELECT      = auto()
    PENCIL      = auto()
    POLYLINE    = auto()
    RECTANGLE   = auto()
    ELLIPSE     = auto()
    FILL        = auto()
