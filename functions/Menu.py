import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Diretorios padrões
BASE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(BASE, 'inputs')
OUTPUTS = os.path.join(BASE, 'outputs')
DECRYPTS = os.path.join(BASE, 'decrypts')

for _ in (INPUTS, OUTPUTS, DECRYPTS):
    os.makedirs(_, exist_ok=True)

# Exceções de navegação
class _Back(Exception):
    pass

class _Quit(Exception):
    pass
