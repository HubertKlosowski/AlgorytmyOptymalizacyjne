import pandas as pd
from flask import Flask, render_template, request, abort
from criterions import *

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'csv', 'tsv', 'xlsx'}

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/wald', methods=['GET', 'POST'])
def wald_template():
    if request.method == 'POST':
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

        return render_template('wald.html', decision=wald(matrix), matrix=matrix)
    else:
        return render_template('wald.html')

@app.route('/optimistic', methods=['GET', 'POST'])
def optimistic_template():
    if request.method == 'POST':
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

        return render_template('optimistic.html', decision=optimistic(matrix), matrix=matrix)
    else:
        return render_template('optimistic.html')

@app.route('/hurwicz')
def hurwicz_template():
    return render_template('hurwicz.html')

@app.route('/savage')
def savage_template():
    return render_template('savage.html')

@app.route('/bayes_laplace')
def bayes_laplace_template():
    return render_template('bayes_laplace.html')


if __name__ == '__main__':
    app.run()
