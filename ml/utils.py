# ml/utils.py
from typing import Sequence, Tuple, List
import random

def train_test_split(X: Sequence[Sequence[float]], y: Sequence[float],
                     test_size: float = 0.2, seed: int = 42
) -> Tuple[List[List[float]], List[List[float]], List[float], List[float]]:
    random.seed(seed)
    idx = list(range(len(X)))
    random.shuffle(idx)
    n_test = max(1, int(len(X) * test_size))
    test_idx = set(idx[:n_test])
    X_tr, X_te, y_tr, y_te = [], [], [], []
    for i in range(len(X)):
        if i in test_idx:
            X_te.append(list(map(float, X[i]))); y_te.append(float(y[i]))
        else:
            X_tr.append(list(map(float, X[i]))); y_tr.append(float(y[i]))
    return X_tr, X_te, y_tr, y_te
