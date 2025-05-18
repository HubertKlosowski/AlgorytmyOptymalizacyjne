import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, abort

from criterions import *

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv', 'xlsx'}

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/choose', methods=['GET', 'POST'])
def choose_template():
    if request.method == 'POST':
        route, choose = request.form['choose'].split()

        try:
            rows, columns = int(request.form['rows']), int(request.form['columns'])
        except TypeError:
            return render_template(
                'choose.html',
                c_error='Liczba wierszy i kolumn musi być liczbą całkowitą większą od 0.'
            )

        if rows <= 0 or columns <= 0:
            return render_template(
                'choose.html',
                c_error='Liczba wierszy i kolumn musi być liczbą całkowitą większą od 0.'
            )

        if route == 'wald':
            return redirect(url_for('wald_template', choose=choose, rows=rows, columns=columns))
        elif route == 'optimistic':
            return redirect(url_for('optimistic_template', choose=choose, rows=rows, columns=columns))
        elif route == 'hurwicz':
            return redirect(url_for('hurwicz_template', choose=choose))
        elif route == 'savage':
            return redirect(url_for('savage_template', choose=choose))
        elif route == 'bayes_laplace':
            return redirect(url_for('bayes_laplace_template', choose=choose))
        else:
            return abort(404)
    else:
        source = request.args.get('source', 'unknown')
        return render_template('choose.html', source=source)

@app.route('/wald', methods=['GET', 'POST'])
def wald_template():
    choose, rows, columns = request.args.get('choose'), int(request.args.get('rows')), int(request.args.get('columns'))
    if request.method == 'POST':
        if choose == 'send_file':
            data = request.files['file']
            ext = data.filename.split('.')[-1]
            if ext not in ALLOWED_EXTENSIONS:
                return render_template(
                    'wald.html',
                    c_error='Rozszerzenie pliku nie jest obsługiwane. Możliwe rozszerzenia: csv, txt, tsv, xlsx.'
                )

            if not ext == 'xlsx':
                matrix = pd.read_csv(data.stream, header=None).to_numpy()
            else:
                matrix = pd.read_excel(data.stream, header=None).to_numpy()
        else:
            matrix = []
            for i in range(rows):
                row = []
                for j in range(columns):
                    value = float(request.form.get(f"matrix_{i}_{j}", 0))
                    row.append(value)
                matrix.append(row)
            matrix = np.array(matrix)

        try:
            wald_value = wald(matrix)
        except TypeError:
            return render_template(
                'wald.html',
                c_error='Wartości macierzy użyteczności muszą być liczbami.'
            )
        return render_template('wald.html', choose=choose, rows=rows, columns=columns, decision=wald_value, matrix=matrix)
    else:
        return render_template('wald.html', choose=choose, rows=rows, columns=columns)

@app.route('/optimistic', methods=['GET', 'POST'])
def optimistic_template():
    choose, rows, columns = request.args.get('choose'), int(request.args.get('rows')), int(request.args.get('columns'))
    if request.method == 'POST':
        if choose == 'send_file':
            data = request.files['file']
            ext = data.filename.split('.')[-1]
            if ext not in ALLOWED_EXTENSIONS:
                return render_template(
                    'optimistic.html',
                    c_error='Rozszerzenie pliku nie jest obsługiwane. Możliwe rozszerzenia: csv, txt, tsv, xlsx.'
                )

            if not ext == 'xlsx':
                matrix = pd.read_csv(data.stream, header=None).to_numpy()
            else:
                matrix = pd.read_excel(data.stream, header=None).to_numpy()
        else:
            matrix = []
            for i in range(rows):
                row = []
                for j in range(columns):
                    value = float(request.form.get(f"matrix_{i}_{j}", 0))
                    row.append(value)
                matrix.append(row)
            matrix = np.array(matrix)

        try:
            optimistic_value = optimistic(matrix)
        except TypeError:
            return render_template(
                'optimistic.html',
                c_error='Wartości macierzy użyteczności muszą być liczbami.'
            )
        return render_template('optimistic.html', choose=choose, rows=rows, columns=columns, decision=optimistic_value, matrix=matrix)
    else:
        return render_template('optimistic.html', choose=choose, rows=rows, columns=columns)

@app.route('/hurwicz', methods=['GET', 'POST'])
def hurwicz_template():
    if request.method == 'POST':
        try:
            gamma = float(request.form['gamma'])
        except ValueError:
            return render_template(
                'hurwicz.html',
                c_error='Parametr gamma musi być typu numerycznego. Podaj wartość ponownie z przedziału [0; 1].'
            )

        data = request.files['file']
        ext = data.filename.split('.')[-1]
        if ext not in ALLOWED_EXTENSIONS:
            return render_template(
                'hurwicz.html',
                c_error='Rozszerzenie pliku nie jest obsługiwane. Możliwe rozszerzenia: csv, txt, tsv, xlsx.'
            )

        if not ext == 'xlsx':
            matrix = pd.read_csv(data.stream, header=None).to_numpy()
        else:
            matrix = pd.read_excel(data.stream, header=None).to_numpy()

        try:
            hurwicz_value = hurwicz(matrix, gamma)
        except Exception as e:
            return render_template(
                'hurwicz.html',
                c_error=e
            )
        return render_template('hurwicz.html', decision=hurwicz_value, matrix=matrix)
    else:
        return render_template('hurwicz.html')

@app.route('/savage', methods=['GET', 'POST'])
def savage_template():
    if request.method == 'POST':
        matrix_file = request.files['file']
        ext_matrix = matrix_file.filename.split('.')[-1]
        if ext_matrix not in ALLOWED_EXTENSIONS:
            return render_template(
                'savage.html',
                c_error='Rozszerzenie pliku nie jest obsługiwane. Możliwe rozszerzenia: csv, txt, tsv, xlsx.'
            )

        if not ext_matrix == 'xlsx':
            matrix = pd.read_csv(matrix_file.stream, header=None).to_numpy()
        else:
            matrix = pd.read_excel(matrix_file.stream, header=None).to_numpy()

        try:
            savage_value = savage(matrix)
        except Exception as e:
            return render_template(
                'savage.html',
                c_error=e
            )
        return render_template('savage.html', decision=savage_value, matrix=matrix)
    else:
        return render_template('savage.html')

@app.route('/bayes_laplace', methods=['GET', 'POST'])
def bayes_laplace_template():
    if request.method == 'POST':
        proba_file, matrix_file = request.files['proba'], request.files['use_matrix']
        ext_proba, ext_matrix = proba_file.filename.split('.')[-1], matrix_file.filename.split('.')[-1]
        if ext_proba not in ALLOWED_EXTENSIONS or ext_matrix not in ALLOWED_EXTENSIONS:
            return render_template(
                'bayes_laplace.html',
                c_error='Rozszerzenie pliku nie jest obsługiwane. Możliwe rozszerzenia: csv, txt, tsv, xlsx.'
            )

        if not ext_proba == 'xlsx':
            proba = pd.read_csv(proba_file.stream, header=None).to_numpy().reshape(-1)
        else:
            proba = pd.read_excel(proba_file.stream, header=None).to_numpy().reshape(-1)

        if not ext_matrix == 'xlsx':
            matrix = pd.read_csv(matrix_file.stream, header=None).to_numpy()
        else:
            matrix = pd.read_excel(matrix_file.stream, header=None).to_numpy()

        try:
            bayes_laplace_value = bayes_laplace(matrix, proba)
        except Exception as e:
            return render_template(
                'bayes_laplace.html',
                c_error=e
            )
        return render_template('bayes_laplace.html', decision=bayes_laplace_value, matrix=matrix, proba=proba)
    else:
        return render_template('bayes_laplace.html')


if __name__ == '__main__':
    app.run()
