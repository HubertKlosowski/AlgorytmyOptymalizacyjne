import numpy as np


def wald(matrix: np.array) -> int:
    return np.argmax(np.min(matrix, axis=1)) + 1

def optimistic(matrix: np.array) -> int:
    return np.argmax(np.max(matrix, axis=1)) + 1

def hurwicz(matrix: np.array, gamma: float) -> int:
    if not isinstance(gamma, (int, float, np.number)):
        raise Exception('Parametr gamma musi być typu numerycznego. Podaj wartość ponownie z przedziału [0; 1].')

    if gamma < 0 or gamma > 1:
        raise Exception('Parametr gamma musi być w przedziale [0; 1].')

    v_gamma = gamma * np.min(matrix, axis=1) + (1 - gamma) * np.max(matrix, axis=1)
    return np.argmax(v_gamma) + 1

def bayes_laplace(matrix: np.array, proba: np.array) -> int:
    if len(proba) != len(matrix[0]):
        raise Exception('Każda kolumna w macierzy musi mieć przyporządkowane prawdopodobieństwo!')

    if not all(isinstance(el, (int, float, np.number)) for el in proba):
        raise Exception('Prawdopodobieństwa muszą być typu numerycznego!')

    g_sum = np.sum(proba)
    print(g_sum)
    if not np.isclose(g_sum, 1.0):
        raise Exception(f'Suma prawdopodobieństw musi być równe jedności. 1 != {g_sum}')

    result = np.sum(proba * matrix, axis=1)
    return np.argmax(result) + 1

def savage(matrix: np.array) -> int:
    sad_matrix = np.abs(np.subtract(matrix, np.max(matrix, axis=0)))
    return np.argmin(np.max(sad_matrix, axis=1)) + 1
