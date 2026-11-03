import os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.Core import (
    LoadHeader, readFreeBoxAndMeta, CHUNK_SIZE, TYPE_SPLIT,
    ShowProgress, COVER_END
)

MARKER_LEN = len(COVER_END) # 16
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

    chunkOverlap = MARKER_LEN - 1
    offset = 0
    fileSize = os.path.getsize(mp4Path)

    with open(mp4Path, 'rb') as f:
        prev = b''
        while offset < fileSize:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            combined = prev + chunk
            pos = combined.find(COVER_END)
            if pos>= 0:
                # offset absoluto do início do marcador
                absMarker = offset - len(prev) + pos
                return absMarker + MARKER_LEN
            prev = combined[-chunkOverlap:] if len(combined) >= chunkOverlap else combined
            offset += len(chunk)

    raise ValueError("Marcador CRYPTMSK não encontrado - arquivo inválido.")
