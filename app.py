from flask import Flask, render_template
from flask import request
import requests
import json
from flask import redirect, url_for
import jinja2

app = Flask(__name__)

@app.route('/details', methods=['GET', 'POST'])
def sendDetails():
    if request.method == 'POST':
        handles = [handle.strip() for handle in request.form["handles"].split(',')]
        data = {"handles" : handles}
        data['problems'] = dict()

        keys = list(request.form.keys())
        # print(keys)
        # print(request.form)
        # return render_template('details.html')
        for i in range(0, len(keys)-1, 2):
            rating = request.form[keys[i]]
            count = request.form[keys[i+1]]
            if len(rating) > 0:
                data["problems"][rating] = int(count)

        url = "https://cf-gym-helper.herokuapp.com/"
        response = requests.request("GET", url, data=json.dumps(data))
        
        fetchedProblems = response.json()["data"]

        problemData = []
        for key in fetchedProblems.keys():
            for val in fetchedProblems[key]:
                problemData.append((key, val))
        
        problemData = tuple(problemData)
        print(problemData)

        if response.status_code == 200:
            return render_template('problems.html', data=problemData)
        else:
            print("redirecting to error page")

    return render_template('details.html')

@app.route('/problems', methods=['GET', 'POST'])
def fetchedProblems():
    return render_template('problems.html')