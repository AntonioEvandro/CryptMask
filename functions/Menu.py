import os, sys
from utils.Utils import MENU, _Back, _Quit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Diretorios padrões
BASE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(BASE, 'inputs')
OUTPUTS = os.path.join(BASE, 'outputs')
DECRYPTS = os.path.join(BASE, 'decrypts')

for _ in (INPUTS, OUTPUTS, DECRYPTS):
    os.makedirs(_, exist_ok=True)

_ACTIONS = {
    '1',
    '2',
    '3',
    '4',
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
