import numpy as np

def get_piece(f=0):
    x = np.random.rand()
    if x < 0.1:
        return 1
    elif x < 0.3:
        return 2
    elif x < 0.6:
        return 3
    elif x < 0.9:
        return 4
    elif x < 0.9 + 0.1*f:
        return 5
    else:
        return 6
    
def get_pieces(n,f=0):
    return np.array([get_piece(f) for _ in range(n)])