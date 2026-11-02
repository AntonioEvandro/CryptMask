import os, struct

# Assinaturas
MAGIC = b'CRYPTMSK'   # formato atual

# Marcador que separa o vídeo de capa dos dados
COVER_END = b'CRPTMSKCOVER_END'  # 16 bytes

# Tipos de arquivo
TYPE_SINGLE = 0
TYPE_SPLIT  = 1

# Tamanho do bloco de I/O (256 MB)
CHUNK_SIZE = 256 * 1024 * 1024

# Limite padrão por parte em split (3 GB)
SPLIT_SIZE = 3 * 1024 * 1024 * 1024

# Caminhos
BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADER  = os.path.join(BASE, 'bin', 'header.bin')
BIN_DIR      = os.path.join(BASE, 'bin')
VIDEOS   = os.path.join(BASE, 'videos')
COVER   = os.path.join(VIDEOS, 'cover.mp4')


def LoadHeader() -> bytes:
    if not os.path.exists(HEADER):
        raise FileNotFoundError(
            f"header.bin não encontrado em: {HEADER}\n"
            "Certifique-se de que o arquivo está em bin/header.bin."
        )
    with open(HEADER, 'rb') as f:
        return f.read()


def ListCovers() -> list:
    """Lista todos os .mp4 na pasta videos/ para usar como capa única."""
    if not os.path.exists(VIDEOS):
        return []
    covers = []
    for f in os.listdir(VIDEOS):
        if f.endswith('.mp4'):
            path = os.path.join(VIDEOS, f)
            size = os.path.getsize(path)
            covers.append((f, path, size))
    return sorted(covers)


def ListVideosInFolder(folder: str) -> list:
    """Lista todos os .mp4 dentro de uma pasta (não recursivo). Retorna [(nome, path, size), ...]."""
    if not folder or not os.path.isdir(folder):
        return []
    videos = []
    for f in os.listdir(folder):
        if f.lower().endswith('.mp4'):
            path = os.path.join(folder, f)
            if os.path.isfile(path):
                videos.append((f, path, os.path.getsize(path)))
    return sorted(videos)


def GetCoverSize(coverPath: str) -> int:
    """Retorna o tamanho da capa em bytes."""
    if os.path.exists(coverPath):
        return os.path.getsize(coverPath)
    return 0


def MakeFreeBoxHeader(payloadSize: int) -> bytes:
    normalTotal = 8 + payloadSize
    if normalTotal <= 0xFFFFFFFF:
        return struct.pack('>I', normalTotal) + b'free'
    else:
        extTotal = 16 + payloadSize
        return struct.pack('>I', 1) + b'free' + struct.pack('>Q', extTotal)


def MakeMdatBox() -> bytes:
    return struct.pack('>I', 8) + b'mdat'


def BuildMeta(originalName: str, tipo: int, idx: int,
               totalParts: int, dataLen: int) -> bytes:
    """
    Estrutura CRYPTMSK (simplificada, sem propriedades):
      MAGIC         (8)
      tipo          (1)
      idx           (2)
      totalPartes   (2)
      lenNome       (2)
      nome          (N)
      lenDados      (8)
    """
    nameBytes = originalName.encode('utf-8')
    return (
        MAGIC
        + struct.pack('>B', tipo)
        + struct.pack('>H', idx)
        + struct.pack('>H', totalParts)
        + struct.pack('>H', len(nameBytes))
        + nameBytes
        + struct.pack('>Q', dataLen)
    )


def readFreeBoxAndMeta(f) -> dict:
    """
    Lê o free box e metadados. Cursor fica no início dos dados.
    Compatível com CRYPTMSK (simplificada).
    """
    sizeRaw = f.read(4)
    boxType = f.read(4)

    if boxType != b'free':
        raise ValueError(
            f"Esperado box 'free', encontrado '{boxType.decode(errors='replace')}'"
        )

    sizeField = struct.unpack('>I', sizeRaw)[0]
    if sizeField == 1:
        f.read(8)  # consome largesize

    magic = f.read(8)

    if magic == MAGIC:
        tipo         = struct.unpack('>B', f.read(1))[0]
        idx          = struct.unpack('>H', f.read(2))[0]
        totalParts   = struct.unpack('>H', f.read(2))[0]
        nameLen      = struct.unpack('>H', f.read(2))[0]
        originalName = f.read(nameLen).decode('utf-8')
        dataLen      = struct.unpack('>Q', f.read(8))[0]
        return dict(version=2, tipo=tipo, idx=idx, totalParts=totalParts, originalName=originalName, dataLen=dataLen)

    else:
        raise ValueError(
            "Assinatura inválida. Este arquivo não foi criado pelo CryptMask."
        )


def ShowProgress(done: int, total: int, label: str = '') -> None:
    pct     = done / total * 100 if total > 0 else 0
    mbDone = done / 1024 / 1024
    mbTot  = total / 1024 / 1024
    print(f'\r  {label}{mbDone:.0f} / {mbTot:.0f} MB  ({pct:.1f}%)',
          end='', flush=True)