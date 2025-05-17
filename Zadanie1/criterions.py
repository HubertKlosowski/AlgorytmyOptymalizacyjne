import numpy as np


def wald(matrix: np.array) -> int:
    the_worst = np.min(matrix, axis=1)
    return np.argmax(the_worst) + 1

def optimistic(matrix: np.array) -> int:
    return np.argmax(np.max(matrix, axis=1)) + 1

def hurwicz(matrix: np.array, gamma: float) -> int:
    if gamma < 0 or gamma > 1:
        raise ValueError('Parametr gamma musi być w przedziale [0; 1]')

    v_gamma = gamma * np.min(matrix, axis=1) + (1 - gamma) * np.max(matrix, axis=1)
    return np.argmax(v_gamma) + 1

def bayes_laplace(matrix: np.array, gammas: np.array) -> int:
    if len(gammas) != len(matrix[0]):
        raise ValueError('Każda kolumna w macierzy musi mieć przyporządkowane prawdopodobieństwo!')

    g_sum = np.sum(gammas)
    if not np.isclose(g_sum, 1.0):
        raise ValueError(f'Suma prawdopodobieństw musi wynieść 1 != {g_sum}')

    result = np.sum(gammas * matrix, axis=1)
    return np.argmax(result) + 1

def savage(matrix: np.array) -> int:
    sad_matrix = np.abs(np.subtract(matrix, np.max(matrix, axis=0)))
    return np.argmin(np.max(sad_matrix, axis=1)) + 1
