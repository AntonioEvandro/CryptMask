import os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.Core import (
    LoadHeader, readFreeBoxAndMeta, CHUNK_SIZE, TYPE_SPLIT,
    ShowProgress, COVER_END
)

MAKER_LEN = len(COVER_END) # 16
HEADER_SIZE = None # Calculando lazy via loadHeader()


def GetHeaderSize() -> int:
    global HEADER_SIZE
    if HEADER_SIZE is None:
        HEADER_SIZE = len(LoadHeader())
    return HEADER_SIZE

