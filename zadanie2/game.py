import numpy as np
import pandas as pd
import os
from scipy.optimize import linprog, OptimizeResult
import warnings
warnings.filterwarnings("ignore")


def maximin(matrix: np.array) -> int:
    return np.max(np.min(matrix, axis=1))

def minimax(matrix: np.array) -> int:
    return np.min(np.max(matrix, axis=0))

def dominant_row(matrix: np.array) -> list:
    dominated = []
    for i, r1 in enumerate(matrix):
        for j, r2 in enumerate(matrix):
            if i != j:
                # r1 dominuje r2, jeśli r1 >= r2 elementowo i co najmniej jeden >
                if all(x >= y for x, y in zip(r1, r2)) and any(x > y for x, y in zip(r1, r2)):
                    dominated.append(j)
    return list(set(dominated))

def dominant_column(matrix: np.array) -> list:
    dominated = []
    transposed = matrix.T
    for i, c1 in enumerate(transposed):
        for j, c2 in enumerate(transposed):
            if i != j:
                # c1 dominuje c2, jeśli c1 <= c2 elementowo i co najmniej jeden <
                if all(x <= y for x, y in zip(c1, c2)) and any(x < y for x, y in zip(c1, c2)):
                    dominated.append(j)
    return list(set(dominated))

def player_a(matrix: np.array) -> OptimizeResult:
    num_strategies = matrix.shape[0]
    num_opponent_strategies = matrix.shape[1]

    c = np.zeros(num_strategies + 1)
    c[-1] = -1

    a_ub, b_ub = np.hstack((-matrix.T, np.ones((num_opponent_strategies, 1)))), np.ones(num_opponent_strategies)
    a_eq, b_eq = np.append(np.ones(num_strategies), 0).reshape(1, -1), [1]

    bounds = [(0, None)] * num_strategies + [(None, None)]

    return linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method='simplex')

def player_b(matrix: np.array) -> OptimizeResult:
    num_strategies = matrix.shape[0]
    num_opponent_strategies = matrix.shape[1]

    c = np.zeros(num_strategies + 1)
    c[-1] = 1

    a_ub, b_ub = np.hstack((matrix.T, -np.ones((num_opponent_strategies, 1)))), np.ones(num_opponent_strategies)
    a_eq, b_eq = np.append(np.ones(num_strategies), 0).reshape(1, -1), [1]

    bounds = [(0, None)] * num_strategies + [(None, None)]

    return linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method='simplex')

def zero_sum_game(matrix: np.array) -> str:
    va, vb = maximin(matrix), minimax(matrix)

    if va == vb:
        return f'Gra ma strategię czystą. Wartość gry: {va}'
    elif va == 0 and vb == 0:
        return 'Gra jest sprawiedliwa, ale nie ma strategii czystej.'
    else:
        # sprawdzić czy istnieją i jeśli tak, to usunąć, strategie zdominowane
        columns, rows = dominant_column(matrix), dominant_row(matrix)
        matrix = np.delete(matrix, columns, axis=1)
        matrix = np.delete(matrix, rows, axis=0)

        # jeżeli w macierzy gry znajdują się wartości ujemne lub zero,
        # to trzeba całą macierz (wartości) przesunąć w górę o pewną wartość,
        # Na końcu uzyskany wynik w postaci wartości gry należy pomniejszyć (odjąć) o tę wartość
        move_up = 0
        if np.min(matrix) < 0:
            move_up = np.abs(np.min(matrix.flatten()))
            matrix += move_up

        res_a = player_a(matrix)
        res_b = player_b(matrix)

        if res_a.success and res_b.success:
            strategy_a, strategy_b = res_a.x[:-1], res_b.x[:-1]
            game_value_a = res_a.x[-1] - move_up

            return f"Strategia gracza A: {strategy_a}. Strategia gracza B: {strategy_b}. Wartość gry: {game_value_a}"
        else:
            return "Nie znaleziono rozwiązania."


def main():
    stop_program = False
    while not stop_program:
        print('Wpisz ścieżkę do pliku:')
        try:
            path = input()
            matrix = pd.read_csv(os.path.normpath(path), header=None, sep=None, engine='python').to_numpy()
            print(zero_sum_game(matrix))
        except FileNotFoundError:
            print('Nie znaleziono pliku. Upewnij się, że ścieżka jest poprawna.')
        except Exception as e:
            print(e)
        print('Skończ program: Y/N')
        p = input()
        stop_program = True if p in ['Y', 'y'] else False


main()
