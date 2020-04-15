from flask import Flask, request, jsonify,Response, g
from src.estimator import estimator
from dicttoxml import dicttoxml 
import json
import logging
import time
import os

if "logs.txt" in os.listdir():
    os.remove("logs.txt") 

# Init
app = Flask(__name__)

logging.basicConfig(filename='logs.txt', level=logging.INFO) 

@app.before_request
def get_time():
    g.start_time = time.time() 

@app.route('/api/v1/on-covid-19/logs', methods=['GET', 'POST'])
def logs():
    logs = []  
    with open("logs.txt", "rt") as f:   # read logs file 
        data = f.readlines()
    for line in data:
        if "root" in line and "404" not in line:
            logs.append(line[10:])

    return Response("".join(logs), mimetype="text/plain")




@app.route('/api/v1/on-covid-19/', methods=['POST', 'GET'])
@app.route('/api/v1/on-covid-19/json', methods=['POST', 'GET'])
def covid():
    if request.method == "GET":
        res = Response("", content_type="application/json")
        return res, 200

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)
        return jsonify(output), 200

@app.route('/api/v1/on-covid-19/xml', methods=['POST', 'GET'])
def covid_19_xml():
    if request.method == "GET":
        res = Response("", content_type="application/xml")
        return res, 200

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)
        res = \
            Response(dicttoxml(
                output, attr_type=False),
                content_type="application/xml")
        return res, 200

@app.after_request
def log_request_info(response):
    response_time = int((time.time() - g.start_time) * 1000)
    status_code = response.status.split()[0]
    logging.info(
    f"{request.method}\t\t{request.path}\t\t{status_code}\t\t{str(response_time).zfill(2)}ms\n"
    )

    return response 
# run server
if __name__ == '__main__':
    app.run(debug=True)
    
