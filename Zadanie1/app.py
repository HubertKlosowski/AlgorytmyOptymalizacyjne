import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, abort

from criterions import *

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv', 'xlsx'}

@app.route('/')
def base_template():
    return render_template('base.html')

@app.route('/choose', methods=['GET', 'POST'])
def choose_template():
    if request.method == 'POST':
        route, choose = request.form['choose'].split()

        if choose == 'enter_manually':
            try:
                rows, columns = int(request.form['rows']), int(request.form['columns'])
            except ValueError:
                # return redirect(url_for('base_template'))
                return render_template(
                    'choose.html',
                    c_error='Liczba wierszy i kolumn musi być liczbą całkowitą większą od 0.'
                )

            if rows <= 0 or columns <= 0:
                return render_template(
                    'choose.html',
                    c_error='Liczba wierszy i kolumn musi być liczbą całkowitą większą od 0.'
                )

        if route == 'wald' and choose == 'enter_manually':
            return redirect(url_for('wald_template_manually', choose=choose, rows=rows, columns=columns))
        elif route == 'wald' and choose == 'send_file':
            return redirect(url_for('wald_template_file', choose=choose))
        elif route == 'optimistic' and choose == 'enter_manually':
            return redirect(url_for('optimistic_template_manually', choose=choose, rows=rows, columns=columns))
        elif route == 'optimistic' and choose == 'send_file':
            return redirect(url_for('optimistic_template_file', choose=choose))
        elif route == 'hurwicz' and choose == 'enter_manually':
            return redirect(url_for('hurwicz_template_manually', choose=choose, rows=rows, columns=columns))
        elif route == 'hurwicz' and choose == 'send_file':
            return redirect(url_for('hurwicz_template_file', choose=choose))

        elif route == 'savage':
            return redirect(url_for('savage_template', choose=choose))
        elif route == 'bayes_laplace':
            return redirect(url_for('bayes_laplace_template', choose=choose))
        else:
            return abort(404)
    else:
        source = request.args.get('source', 'unknown')
        return render_template('choose.html', source=source)

@app.route('/wald_file', methods=['GET', 'POST'])
def wald_template_file():
    if request.method == 'POST':
        data = request.files['file']
        ext = data.filename.split('.')[-1]
        if ext not in ALLOWED_EXTENSIONS:
            return render_template(
                'wald_file.html',
                c_error='Rozszerzenie pliku nie jest obsługiwane. Możliwe rozszerzenia: csv, txt, tsv, xlsx.'
            )

        if not ext == 'xlsx':
            matrix = pd.read_csv(data.stream, header=None).to_numpy()
        else:
            matrix = pd.read_excel(data.stream, header=None).to_numpy()

        try:
            wald_value = wald(matrix)
        except TypeError:
            return render_template(
                'wald_file.html',
                c_error='Wartości macierzy użyteczności muszą być liczbami.'
            )
        return render_template(
            'wald_file.html',
            decision=wald_value,
            matrix=matrix
        )
    else:
        return render_template('wald_file.html')

@app.route('/wald_manually', methods=['GET', 'POST'])
def wald_template_manually():
    rows, columns = int(request.args.get('rows')), int(request.args.get('columns'))
    if request.method == 'POST':
        matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                value = float(request.form.get(f'matrix_{i}_{j}', 0))
                row.append(value)
            matrix.append(row)
        matrix = np.array(matrix)

        try:
            wald_value = wald(matrix)
        except TypeError:
            return render_template(
                'wald_manually.html',
                c_error='Wartości macierzy użyteczności muszą być liczbami.'
            )
        return render_template(
            'wald_manually.html',
            rows=rows,
            columns=columns,
            decision=wald_value,
            matrix=matrix
        )
    else:
        return render_template(
            'wald_manually.html',
            rows=rows,
            columns=columns
        )

@app.route('/optimistic_file', methods=['GET', 'POST'])
def optimistic_template_file():
    if request.method == 'POST':
        data = request.files['file']
        ext = data.filename.split('.')[-1]
        if ext not in ALLOWED_EXTENSIONS:
            return render_template(
                'optimistic_file.html',
                c_error='Rozszerzenie pliku nie jest obsługiwane. Możliwe rozszerzenia: csv, txt, tsv, xlsx.'
            )

        if not ext == 'xlsx':
            matrix = pd.read_csv(data.stream, header=None).to_numpy()
        else:
            matrix = pd.read_excel(data.stream, header=None).to_numpy()

        try:
            optimistic_value = optimistic(matrix)
        except TypeError:
            return render_template(
                'optimistic_file.html',
                c_error='Wartości macierzy użyteczności muszą być liczbami.'
            )
        return render_template(
            'optimistic_file.html',
            decision=optimistic_value,
            matrix=matrix
        )
    else:
        return render_template('optimistic_file.html')

@app.route('/optimistic_manually', methods=['GET', 'POST'])
def optimistic_template_manually():
    rows, columns = int(request.args.get('rows')), int(request.args.get('columns'))
    if request.method == 'POST':
        matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                value = float(request.form.get(f'matrix_{i}_{j}', 0))
                row.append(value)
            matrix.append(row)
        matrix = np.array(matrix)

        try:
            optimistic_value = optimistic(matrix)
        except TypeError:
            return render_template(
                'optimistic_manually.html',
                c_error='Wartości macierzy użyteczności muszą być liczbami.'
            )
        return render_template(
            'optimistic_manually.html',
            rows=rows,
            columns=columns,
            decision=optimistic_value,
            matrix=matrix
        )
    else:
        return render_template(
            'optimistic_manually.html',
            rows=rows,
            columns=columns
        )

@app.route('/hurwicz_file', methods=['GET', 'POST'])
def hurwicz_template_file():
    if request.method == 'POST':
        try:
            gamma = float(request.form['gamma'])
        except ValueError:
            return render_template(
                'hurwicz_file.html',
                c_error='Parametr gamma musi być typu numerycznego. Podaj wartość ponownie z przedziału [0; 1].'
            )

        data = request.files['file']
        ext = data.filename.split('.')[-1]
        if ext not in ALLOWED_EXTENSIONS:
            return render_template(
                'hurwicz_file.html',
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
                'hurwicz_file.html',
                c_error=e
            )
        return render_template(
            'hurwicz_file.html',
            decision=hurwicz_value,
            matrix=matrix
        )
    else:
        return render_template('hurwicz_file.html')

@app.route('/hurwicz_manually', methods=['GET', 'POST'])
def hurwicz_template_manually():
    rows, columns = int(request.args.get('rows')), int(request.args.get('columns'))
    if request.method == 'POST':
        try:
            gamma = float(request.form['gamma'])
        except ValueError:
            return render_template(
                'hurwicz_manually.html',
                c_error='Parametr gamma musi być typu numerycznego. Podaj wartość ponownie z przedziału [0; 1].'
            )

        matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                value = float(request.form.get(f'matrix_{i}_{j}', 0))
                row.append(value)
            matrix.append(row)
        matrix = np.array(matrix)

        try:
            hurwicz_value = hurwicz(matrix, gamma)
        except Exception as e:
            return render_template(
                'hurwicz_manually.html',
                c_error=e
            )
        return render_template(
            'hurwicz_manually.html',
            rows=rows,
            columns=columns,
            decision=hurwicz_value,
            matrix=matrix
        )
    else:
        return render_template(
            'hurwicz_manually.html',
            rows=rows,
            columns=columns
        )

@app.route('/savage_file', methods=['GET', 'POST'])
def savage_template_file():
    if request.method == 'POST':
        matrix_file = request.files['file']
        ext_matrix = matrix_file.filename.split('.')[-1]
        if ext_matrix not in ALLOWED_EXTENSIONS:
            return render_template(
                'savage_file.html',
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
                'savage_file.html',
                c_error=e
            )
        return render_template('savage_file.html', decision=savage_value, matrix=matrix)
    else:
        return render_template('savage_file.html')

@app.route('/savage_manually', methods=['GET', 'POST'])
def savage_template_manually():
    rows, columns = int(request.args.get('rows')), int(request.args.get('columns'))
    if request.method == 'POST':
        matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                value = float(request.form.get(f'matrix_{i}_{j}', 0))
                row.append(value)
            matrix.append(row)
        matrix = np.array(matrix)

        try:
            savage_value = savage(matrix)
        except Exception as e:
            return render_template(
                'savage_manually.html',
                c_error=e
            )
        return render_template(
            'savage_manually.html',
            rows=rows,
            columns=columns,
            decision=savage_value,
            matrix=matrix
        )
    else:
        return render_template(
            'savage_manually.html',
            rows=rows,
            columns=columns
        )

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
