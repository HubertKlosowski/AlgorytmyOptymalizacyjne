from flask import Flask, render_template
from criterions import *

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/wald')
def wald_template():
    return render_template('wald.html')

@app.route('/optimistic')
def optimistic_template():
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
