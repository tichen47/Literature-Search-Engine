from MeTA import query
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


@app.route("/search")
def search():
    input = request.args['input']
    results = query.search(input)
    return render_template("results.html", input=input, results=results)