import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.Core import (
    MakeFreeBoxHeader, MakeMdatBox,BuildMeta,
    CHUNK_SIZE, SPLIT_SIZE, TYPE_SINGLE, TYPE_SPLIT, ShowProgress
)
from functions.Cover import WriteCoverBlock, totalCoverSize
from utils.Utils import GB as gb


def WriteMp4(input: str, output: str, originalName: str, tipo: int,
    idx: int, totalParts: int, dataStart: int, dataLen: int, 
    coverPaths: list = None) -> None:

    meta = BuildMeta(originalName, tipo, idx, totalParts, dataLen)
    fboxHdr = MakeFreeBoxHeader(len(meta) + dataLen)
    mdat = MakeMdatBox()

    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)

    with open(output, 'wb') as outF:
        WriteCoverBlock(outF, coverPaths or [])

        # Metadados e dados
        outF.write(fboxHdr)
        outF.write(meta)

        with open(input, 'rb') as inF:
            inF.seek(dataStart)
            remaining = dataLen
            written = 0
            label = f"[enc] parte {idx}/{totalParts}  "if tipo == TYPE_SPLIT else "[enc] "
            while remaining > 0:
                chunk = inF.read(min(CHUNK_SIZE, remaining))
                if not chunk: break
                outF.write(chunk)
                written += len(chunk)
                remaining -= len(chunk)
                ShowProgress(written, dataLen, label)
        outF.write(mdat)
    print()
    totalSize = os.path.getsize(output)
    print(f"[enc] Salvo: {output}  ({totalSize / gb / gb:.2f} MB)")