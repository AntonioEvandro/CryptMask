import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.Core import (
    MakeFreeBoxHeader, MakeMdatBox,BuildMeta,
    CHUNK_SIZE, SPLIT_SIZE, TYPE_SINGLE, TYPE_SPLIT, ShowProgress
)
from functions.Cover import WriteCoverBlock, totalCoverSize
from utils.Utils import GB as gb


def WriteMp4(inputPath: str, outputPath: str, originalName: str, tipo: int,
    idx: int, totalParts: int, dataStart: int, dataLen: int, 
    coverPaths: list = None) -> None:

    meta = BuildMeta(originalName, tipo, idx, totalParts, dataLen)
    fboxHdr = MakeFreeBoxHeader(len(meta) + dataLen)
    mdat = MakeMdatBox()

    os.makedirs(os.path.dirname(os.path.abspath(outputPath)), exist_ok=True)

    with open(outputPath, 'wb') as outF:
        WriteCoverBlock(outF, coverPaths or [])

        # Metadados e dados
        outF.write(fboxHdr)
        outF.write(meta)

        with open(inputPath, 'rb') as inF:
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
    totalSize = os.path.getsize(outputPath)
    print(f"[enc] Salvo: {outputPath}  ({totalSize / gb / gb:.2f} MB)")


def EncodeSingle(inputPath: str, outputPath: str, coverPaths: list = None) -> None:
    if not os.path.exists(inputPath):
        raise FileNotFoundError(f"Arquivo não encontrado: {inputPath}")

    dataLen = os.path.getsize(inputPath)
    originalName = os.path.basename(inputPath)

    print(f"[enc] Lendo: {inputPath}  ({dataLen / gb / gb:.2f} MB)")
    WriteMp4(inputPath, outputPath, originalName, TYPE_SINGLE, 0, 1, 0, dataLen, coverPaths)


def EncodeSplit(
        inputPath: str, outputDir: str, coverPaths: list = None, 
        splitSize: int = SPLIT_SIZE) -> list:
    if not os.path.exists(inputPath):
        raise FileNotFoundError(f"Arquivo não encontrado: {inputPath}")

    fileSize = os.path.getsize(inputPath)
    originalName = os.path.basename(inputPath)
    stem = os.path.splitext(originalName)[0]

    coverPaths = coverPaths or []
    coverSize = totalCoverSize(coverPaths)
    effectiveSplitSize = splitSize - coverSize

    if effectiveSplitSize <= 0:
        raise ValueError(
            f"Capa(s) muito grande(s) ({coverSize / gb / gb:.1f} MB). "
            f"Limite de split é {splitSize / gb / gb / gb:.1f} GB)."
        )

    totalParts = (fileSize + effectiveSplitSize - 1) // effectiveSplitSize

    print(f"[ENC] Arquivo: {inputPath} ({fileSize / gb / gb / gb:.2f} GB)")
    if coverPaths:
        print(f"[enc] Capa(s): {len(coverPaths)} vídeo(s)  ({coverSize / gb / gb:.1f} MB)")
    print(f"[enc] Dividindo em {totalParts} parte(s) de até "
          f"{effectiveSplitSize / gb / gb / gb:.1f} GB cada")

    os.makedirs(outputDir, exist_ok=True)
    outputs = []

    for idx in range(1, totalParts + 1):
        dataStart = (idx - 1) * effectiveSplitSize
        dataLen   = min(effectiveSplitSize, fileSize - dataStart)
        outPath   = os.path.join(outputDir, f"{stem}.split{idx}.mp4")

        partCoverPaths = coverPaths.copy() if coverPaths else []
        
        WriteMp4(inputPath, outPath, originalName,
                   TYPE_SPLIT, idx, totalParts,
                   dataStart, dataLen, partCoverPaths)
        outputs.append(outPath)

    print(f"[enc] Concluído: {totalParts} arquivo(s) gerado(s) em '{outputDir}'")
    return outputs