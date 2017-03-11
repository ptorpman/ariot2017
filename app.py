#!/usr/bin/env python

from flask import Flask, url_for, render_template, jsonify
from random import choice
import simplejson as json
import os
import threading
import time

app = Flask(__name__)
rfConst = "sensorvalues.json"
wfConst = "piinput.json"
fanConst = "fan"
cameraConst = "take_picture"
lampConst = "lamp"

inputFile = {"lamp": "auto", "fan": "auto", "airtemp_max":"25"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images')
def images():
    urls = []
    names = os.listdir(os.path.join(app.static_folder, 'photos'))
    for name in names:
        urls.append(url_for('static', filename='photos/' + name))

    return render_template('image.html', urls=urls)


#ENDPOINTS
@app.route('/api_data')
def api_data():
    try:
        with open(rfConst) as data_file:
            data = jsonify(json.loads(data_file.read()))
    except IOError:
        print ("Error")
        data = jsonify("{}")
    finally:
        data_file.close()
    return data



#LIGHT CONTROLS
@app.route('/turnOnLights')
def turnOnLights():
    inputFile[lampConst] = "on"
    return writeInputFile()

@app.route('/turnOffLights')
def turnOffLights():
    inputFile[lampConst] = "off"
    return writeInputFile()

@app.route('/setAutoLights')
def setAutoLights():
    inputFile[lampConst] = "auto"
    return writeInputFile()

#FAN CONTROLS
@app.route('/turnOnFan')
def turnOnFan():
    inputFile[fanConst] = "on"
    return writeInputFile()

@app.route('/turnOffFan')
def turnOffFan():
    inputFile[fanConst] = "off"
    return writeInputFile()

@app.route('/setAutoFan')
def setAutoFan():
    inputFile[fanConst] = "auto"
    return writeInputFile()

#CAMERA CONTROL
@app.route('/take_picture')
def take_picture():
    inputFile[cameraConst] = str(int(round(time.time() * 1000)))
    return writeInputFile()


@app.route("/writeOrderFile")
def writeInputFile():
    print(inputFile)
    try:
        with open(wfConst, 'w') as outfile:
            json.dump(inputFile, outfile)
    except IOError:
        print("WriteError")
        return "Error"

    return "success"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
