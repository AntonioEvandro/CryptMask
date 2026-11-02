"""
functions/Cover.py — Lógica de vídeo(s) de "capa" usados para disfarçar o
arquivo final como um vídeo comum aos olhos de observadores.

Modos suportados:
  NONE     — sem capa, usa apenas o header.bin padrão.
  SINGLE   — um único vídeo fixo (ex: videos/cover.mp4).

No modo com capa, o arquivo final escreve:
    [ capa ]
    [ CRPTMSKCOVER_END  ]
    [ free box com metadados + dados reais ]
    [ mdat ]
"""

import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.Core import (
    LoadHeader, GetCoverSize,
    CHUNK_SIZE, COVER_END,
    VIDEOS, COVER
)


# Modos de capa
MODENONE = 'none'
MODESINGLE = 'single'

class CoverConfig:
    """
    Configuração de capa escolhida pelo usuário no menu.

    mode          : MODENONE | MODESINGLE
    singlePath   : caminho do vídeo único (modo SINGLE). None = usa COVERPATH padrão.
    """

    def __init__(self, mode: str = MODESINGLE,
                 singlePath: str = None):
        self.mode          = mode
        self.singlePath   = singlePath

    def SinglePath(self) -> str:
        return self.singlePath if self.singlePath else COVER

def DescribeStatus(config: CoverConfig) -> str:
    """Gera a linha de status mostrada como 'Modo atual' no menu."""
    if config.mode == MODENONE:
        return "[Sem capa]"

    if config.mode == MODESINGLE:
        path = config.SinglePath()
        if os.path.exists(path):
            sizeMb = os.path.getsize(path) / 1024 / 1024
            return f"[Capa única]\n({os.path.relpath(path, VIDEOS if os.path.isdir(VIDEOS) else os.path.dirname(path))} - {sizeMb:.1f} MB)"
        return "[Capa única]\n(arquivo não encontrado)"