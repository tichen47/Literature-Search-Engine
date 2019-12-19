import pickle

from waitress import serve
from flask import Flask, render_template, request
import os
import query_affinity as qa

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
    results = results[:10]
    
    for res in results:
        conf = res[2]
        conf = 'v' + conf.replace(" ","")
        rec_list = qa.get_neighbors("m2vpp.aminer2017.w1000.l100.txt.size128.window7.negative5.txt", conf)
        
        ret = []
        for item in rec_list:
            item = item[1:]
            if item != '/s>' and item not in ret:
                ret.append(item)
                
        res.append(ret)
        # print(rec_list)
    
    return render_template("results.html", input=input, results=results)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80)
    # app.run(debug=True, host='0.0.0.0', port=80)