import pickle

from waitress import serve
from flask import Flask, render_template, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/search")
def search():
    input = request.args['input']
    command = "python3 MeTA/query.py --query=" + input
    os.system(command)
    results = pickle.load(open('query_results', 'rb'))
    return render_template("results.html", input=input, results=results)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80)
    # app.run(debug=True, host='0.0.0.0', port=80)