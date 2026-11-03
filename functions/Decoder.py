import os, sys, glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.Core import (
    LoadHeader, readFreeBoxAndMeta, CHUNK_SIZE, TYPE_SPLIT,
    ShowProgress, COVER_END
)
from utils.Utils import GB as gb

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

def PeekMeta(mp4Path: str) -> dict | None:
    try:
        offset = FindPayload(mp4Path)
        with open(mp4Path, 'rb') as f:
            f.seek(offset)
            return readFreeBoxAndMeta(f)
    except Exception:
        return None


def ExtractData(f, outF, dataLen: int, label: str = '[dec] ') -> None:
    remaining = dataLen
    done      = 0
    while remaining > 0:
        chunk = f.read(min(CHUNK_SIZE, remaining))
        if not chunk:
            break
        outF.write(chunk)
        done      += len(chunk)
        remaining -= len(chunk)
        ShowProgress(done, dataLen, label)
    print()


def FindSplitParts(firstPath: str, meta: dict) -> list:
    folder        = os.path.dirname(os.path.abspath(firstPath))
    originalName = meta['originalName']
    totalParts   = meta['totalParts']
    stem          = os.path.splitext(originalName)[0]

    pattern    = os.path.join(folder, f"{stem}.split*.mp4")
    candidates = glob.glob(pattern)

    parts = {}
    for path in candidates:
        m = PeekMeta(path)
        if (m and m.get('tipo') == TYPE_SPLIT
                and m.get('originalName') == originalName
                and m.get('totalParts') == totalParts):
            parts[m['idx']] = path

    missing = [i for i in range(1, totalParts + 1) if i not in parts]
    if missing:
        raise RuntimeError(
            f"Partes faltando: {missing}\n"
            f"Certifique-se de que todos os arquivos '{stem}.split*.mp4' "
            f"estão na mesma pasta."
        )

    return [parts[i] for i in range(1, totalParts + 1)]


def Decode(inputPath: str, outputPath: str = None) -> None:
    if not os.path.exists(inputPath):
        raise FileNotFoundError(f"Arquivo não encontrado: {inputPath}")

    offset = FindPayload(inputPath)

    with open(inputPath, 'rb') as f:
        f.seek(offset)
        meta = readFreeBoxAndMeta(f)

    originalName = meta['originalName']
    out = outputPath if outputPath else originalName
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)

    # Arquivo único
    if meta['tipo'] != TYPE_SPLIT:
        print(f"[dec] Lendo: {inputPath}")
        print(f"[dec] Arquivo original: {originalName}  "
              f"({meta['dataLen'] / gb / gb:.2f} MB)")
        with open(inputPath, 'rb') as f:
            f.seek(offset)
            readFreeBoxAndMeta(f)   # reposiciona cursor nos dados
            with open(out, 'wb') as out_f:
                ExtractData(f, out_f, meta['dataLen'])
        print(f"[dec] Salvo em: {out}")
        return
