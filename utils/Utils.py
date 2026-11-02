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
        ║  3. Verificar integridade    ║
        ║  4. Informações do arquivo   ║
        ║                              ║
        ║  q. Sair                     ║
        ╚══════════════════════════════╝"""

AFTERACTION = """
\n──────────────────────────────────────────────
    1. Repetir com outro arquivo
    0. Voltar ao menu principal
    q. Sair
"""