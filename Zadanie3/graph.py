import numpy as np
import pandas as pd


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, el):
        self.queue.append(el)

    def dequeue(self) -> int:
        if self.is_empty():
            raise OverflowError('Pusta kolejka.')
        return self.queue.pop(0)

    def peek(self) -> int:
        if self.is_empty():
            raise OverflowError('Pusta kolejka.')
        return self.queue[0]

    def size(self) -> int:
        return len(self.queue)

    def is_empty(self) -> bool:
        return True if self.size() == 0 else False


def load_data(path: str) -> np.array:
    matrix = pd.read_csv(path, header=None, sep=None, engine='python')
    for col in matrix.columns:
        try:
            matrix[col] = matrix[col].apply(lambda x: np.nan if x == 'x' or x == '-' else float(x))
        except ValueError:
            return f'Błąd konwersji na liczbę zmienno-przecinkową w kolumnie {col}.'

    return matrix.to_numpy()


def bfs(graph: np.array, source: int, target: int) -> list | None:
    my_set = {source: None}
    my_queue = Queue()
    my_queue.enqueue(source)

    while not my_queue.is_empty():
        x = my_queue.dequeue()
        for v, capacity in enumerate(graph[x]):
            if capacity > 0 and v not in my_set:
                my_set[v] = x
                if v == target:
                    path = []
                    while v is not None:
                        path.insert(0, v)
                        v = my_set[v]
                    return path
                my_queue.enqueue(v)
    return None


def edmonds_karp(c: np.array, source: int, target: int):
    max_flow = 0
    itr = 0

    while True:
        path = bfs(c, source, target)
        if not path:
            break

        print('-' * 100)
        print(f'Iteracja: {itr}')
        print(f'path: {path}')

        flow = min(c[u][v] for u, v in zip(path, path[1:]))
        for u, v in zip(path, path[1:]):
            c[u][v] -= flow
            c[v][u] += flow

        max_flow += flow

        print(f'Flow: {flow}')
        itr += 1

    print('-' * 100)
    return max_flow


def main():
    stop_program = False
    while not stop_program:
        print('Wpisz ścieżkę do pliku:')
        try:
            path = input()
            capacities = load_data(path)
            print(f'Podaj wierzchołek startowy {[el for el in range(capacities.shape[0])]}:')
            src = int(input())
            print(f'Podaj wierzchołek końcowy {[el for el in range(capacities.shape[0])]}:')
            tg = int(input())
            if src < 0 or tg < 0:
                raise ValueError(f'Wierzchołki muszą być w przedziale {[el for el in range(capacities.shape[0])]}')
            print(f'Max Flow = {edmonds_karp(capacities, src, tg)}')
        except FileNotFoundError:
            print('Nie znaleziono pliku. Upewnij się, że ścieżka jest poprawna.')
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)

        print('Skończ program: Y/N')
        p = input()
        stop_program = True if p in ['Y', 'y'] else False


main()
