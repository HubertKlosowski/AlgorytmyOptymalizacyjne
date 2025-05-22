import numpy as np


def wald(matrix: np.array) -> int:
    return np.argmax(np.min(matrix, axis=1)) + 1


def dominant(matrix: np.array) -> list:
    dominanted = []
    for i, r1 in enumerate(matrix):
        for j, r2 in enumerate(matrix):
            if i != j:
                if all(x <= y for x, y in zip(r1, r2)):
                    dominanted.append(j)
    return list(set(dominanted))

def sum_zero_game(matrix: np.array) -> str:
    a, b = wald(matrix), wald(matrix.T)
    if a == b:
        return f'Wartość gry wynosi {a}. (strategia czysta)'
    elif a == 0:
        return 'Gra jest sprawiedliwa.'
    else:
        columns, rows = dominant(matrix.T), dominant(matrix)
        matrix = np.delete(matrix, columns, axis=1)
        matrix = np.delete(matrix, rows, axis=0)
        return str(matrix)

task = np.array([
    [1, 3, 5, 8],
    [-2, 4, 3, 5],
    [7, -1, 1, 0]
])

# task = np.array([
#     [2, 1, 3],
#     [1, 1, 1],
#     [3, 2, 4],
#     [1, 5, 0]
# ])

print(sum_zero_game(task))
