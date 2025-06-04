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

        flow = min(c[u][v] for u, v in zip(path, path[1:]))
        for u, v in zip(path, path[1:]):
            c[u][v] -= flow
            c[v][u] += flow

        max_flow += flow
        print('-' * 100)
        print(f'Iteracja: {itr}')
        print(f'Ścieżka: {path}, Przepływ: {flow}')
        itr += 1

    print('-' * 100)
    return max_flow


def main():
    stop_program = False
    while not stop_program:
        choose = input('Wybierz sposób wprowadzenia macierzy wypłat\n --> (P) plik, \n --> (K) konsola.\n')
        capacities = []
        if choose == 'P' or choose == 'K':
            if choose == 'P':
                try:
                    path = input('Wpisz ścieżkę do pliku: ')
                    capacities = load_data(path)
                except FileNotFoundError:
                    print('Nie znaleziono pliku. Upewnij się, że ścieżka jest poprawna.')
            elif choose == 'K':
                points = int(input('Podaj liczbę wierzchołków: '))
                if points <= 0:
                    raise ValueError('Liczba wierzchołków musi być większa od zera!')

                capacities = np.zeros(shape=(points, points))
                for i in range(points):
                    for j in range(points):
                        if i != j:
                            capacities[i][j] = float(input(f'Połączenie między {i}, a {j}: '))

            try:
                src = int(input(f'Podaj wierzchołek startowy {[el for el in range(capacities.shape[0])]}: '))
                tg = int(input(f'Podaj wierzchołek końcowy {[el for el in range(capacities.shape[0])]}: '))
                if src < 0 or tg < 0:
                    raise ValueError(f'Wierzchołki muszą być w przedziale {[el for el in range(capacities.shape[0])]}')
                print(f' --> Maksymalny przepływ w sieci = {edmonds_karp(capacities, src, tg)}')
            except ValueError as e:
                print(e)
        else:
            print('Niepoprawna opcja!')

        print('Skończ program: Y/N')
        p = input()
        stop_program = True if p in ['Y', 'y'] else False


main()
