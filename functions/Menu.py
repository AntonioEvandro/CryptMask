import os, sys
from utils.Utils import MENU, _Back, _Quit, AFTERACTION

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.Core import SPLIT_SIZE, TYPE_SPLIT, ListCovers, VIDEOS
from functions.Cover import (
    CoverConfig, MODENONE, MODESINGLE, DescribeStatus, ResolveCoverSequence
)

# Diretorios padrões
BASE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(BASE, 'inputs')
OUTPUTS = os.path.join(BASE, 'outputs')
DECRYPTS = os.path.join(BASE, 'decrypts')

for _ in (INPUTS, OUTPUTS, DECRYPTS):
    os.makedirs(_, exist_ok=True)


# Helpers de input
def ask(prompt: str, default: str = '') -> str:
    try:
        val = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        raise _Quit()
    if val.lower() == 'q':
        raise _Quit()
    if val == '0':
        raise _Back()
    return val if val else default


# Acões pós operação
def AfterAction():
    print(AFTERACTION)
    while True:
        try:
            choice = input("\nOpção [0]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise _Quit()
        if not choice or choice == '0':
            return False
        if choice == '1':
            return True
        if choice == 'q':
            raise _Quit()
        print("  Opção inválida.")


# Resolução de caminhos

def FindInput(name: str) -> str:
    if os.path.exists(name):
        return name
    for folder in (INPUTS, OUTPUTS):
        candidate = os.path.join(folder, name)
        if os.path.exists(candidate):
            return candidate
        return name


def ResolveEncOutput(raw: str, originalName: str) -> str:
    stem = os.path.splitext(originalName)[0]
    if not raw:
        return os.path.join(OUTPUTS, stem + '.mp4')
    if raw.endswith(('/', '\\')) or os.path.isdir(raw):
        return os.path.join(raw, stem + '.mp4')
    if os.path.dirname(raw):
        return raw
    return os.path.join(OUTPUTS, raw)


def ResolveDecOutput(raw: str, originalName: str) -> str:
    if not raw:
        return os.path.join(DECRYPTS, originalName)
    if raw.endswith(('/', '\\')) or os.path.isdir(raw):
        return os.path.join(raw, originalName)
    if os.path.dirname(raw):
        return raw
    return os.path.join(DECRYPTS, raw)


# Sub menu: gerenciar vídeo(s) de capa
def SubmenuCover(config: CoverConfig = None) -> CoverConfig:
    """
    Sub-menu para gerenciar vídeo(s) de capa (modo único ou nenhum).

    Modo padrão: capa única (usa videos/cover.mp4 se existir, se não pergunta).
    """
    if config is None:
        # Define como SINGLE por padrão (usa cover.mp4 se existir)
        config = CoverConfig(mode=MODESINGLE)
        
    while True:
        print("\n  ───────── Vídeo de capa ───────────────")
        print("  (0 = voltar  |  q = sair)\n")

        status = DescribeStatus(config)
        print(f"  Modo atual: {status}\n")

        print("  1. Sem capa")
        print("  2. Capa única         (escolher 1 vídeo fixo)")
        print("\n  s. Confirmar  (aceita o modo atual mostrado acima)")

        try:
            choice = input("\n  Opção [s]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            raise _Quit()

        if choice == 'q':
            raise _Quit()
        if choice == '0':
            return config
        if not choice or choice == 's':
            return config

        if choice == '1':
            config = CoverConfig(mode=MODENONE)
            print("  Capa desativada.")
            continue

        if choice == '2':
            covers = ListCovers()
            if not covers:
                print(f"  [!] Nenhum .mp4 encontrado em {VIDEOS}")
                continue

            print("\n  ─────── Escolher capa única ────────────")
            for i, (name, path, size) in enumerate(covers, 1):
                sizeMb = size / 1024 / 1024
                print(f"  {i}. {name}  ({sizeMb:.1f} MB)")
            print(f"\n  0. Voltar")

            try:
                subChoice = input("\n  Escolha: ").strip()
            except (EOFError, KeyboardInterrupt):
                raise _Quit()

            if subChoice == '0':
                continue
            if subChoice.isdigit():
                idx = int(subChoice) - 1
                if 0 <= idx < len(covers):
                    config = CoverConfig(mode = MODESINGLE, singlePath = covers[idx][1])
                    print(f"  Capa única selecionada: {covers[idx][0]}")
                    continue
            print("  Opção inválida.")
            continue

        print("  Opção inválida.")


# Menu principal de codificação
# A fazer


_ACTIONS = {
    '1',
    '2'
}


def main():
    while True:
        print(MENU)
        try:
            choice = input("Opção: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais.")
            break

        if choice == 'q':
            print("Até mais.")
            break

        action = _ACTIONS.get(choice)
        if not action:
            print("Opção inválida.")
            continue

        try:
            action()
        except _Back:
            continue
        except _Quit:
            print("\n Até mais.")
            break
        except FileNotFoundError as e:
            print(f"\n[ERRO] {e}")
        except RuntimeError as e:
            print(f"\n[ERRO] {e}")
        except Exception as e:
            print(f"\n[Erro inesperado] {e}")