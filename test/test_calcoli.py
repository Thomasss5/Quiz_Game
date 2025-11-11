import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src_exercises.calcoli import somma, moltiplica

def test_somma():
    assert somma(2, 3) == 5
    assert somma(-1, 1) == 0
    assert somma(0, 0) == 0 

def test_moltiplica():
    assert moltiplica(2, 3) == 6
    assert moltiplica(-2, 3) == -6
    assert moltiplica(0, 99) == 0
