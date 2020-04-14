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

@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def logs():
    data_logs = [] 
    with open("logs.txt", "rt") as f: # read logs file 
        data = f.readlines()
    for line in data:
        if "root" in line and "404" not in line:
            data_logs.append(line[10:])

    return Response("".join(data_logs), mimetype="text/plain") 




@app.route('/api/v1/on-covid-19/', methods=['POST'])
@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def covid():
    request_data = request.get_json() 
    data = estimator(request_data)

    response = Response(json.dumps(data), 200, mimetype='application/json')
    response.headers['Location'] = ("/api/v1/on-covid-19/json")
    return response 

@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def covid_19_xml():
    request_data = request.get_json()
    data = estimator(request_data)

    res = Response(dicttoxml(data, attr_type=False), status=200, content_type="application/xml")
    res.headers['Location'] = ("/api/v1/on-covid-19/xml")
    return res 


@app.after_request
def log_request_info(response):
    response_time = int((time.time() - g.start) * 1000)
    status_code = response.status.split()[0]
    logging.info(
    f"{request.method}\t\t{request.path}\t\t{status_code}\t\t{str(response_time).zfill(2)}ms\n"
    )

    return response 
# run server
if __name__ == '__main__':
    app.run(debug=True)
    
