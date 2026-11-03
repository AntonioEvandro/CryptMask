# Exceções de navegação
class _Back(Exception):
    pass

class _Quit(Exception):
    pass

# Menu principal
MENU = """
        ╔══════════════════════════════╗
        ║          C r y p t           ║
        ║           M a s k            ║
        ╠══════════════════════════════╣
        ║  1. Codificar arquivo        ║
        ║  2. Decodificar arquivo      ║
        ║                              ║
        ║  q. Sair                     ║
        ╚══════════════════════════════╝"""

AFTERACTION = """
\n──────────────────────────────────────────────
    1. Repetir com outro arquivo
    0. Voltar ao menu principal
    q. Sair
"""

PARTSCHOICE = """
    1. Dividir em partes

    2. Arquivo único
"""
