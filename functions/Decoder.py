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


def FindPayload(mp4Path: str) -> int:
    headerSize = GetHeaderSize()

    with open(mp4Path, 'rb') as f:
        # Verifica se começa com header.bin
        candidate = f.read(headerSize)

    try:
        header = LoadHeader()
        if candidate == header:
            return headerSize # Arquivo sem capa
    except Exception:
        pass

    chunkOverlap = MAKER_LEN - 1
    offset = 0
    fileSize = os.path.getsize(mp4Path)

    