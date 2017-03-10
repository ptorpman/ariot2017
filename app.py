from flask import Flask, url_for, render_template
from random import choice
import simplejson as json
import os
import threading
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#Temperatur
#Vatten
#Ljus

@app.route('/images')
def images():
    urls = []
    names = os.listdir(os.path.join(app.static_folder, 'images'))
    for name in names:
        urls.append(url_for('static', filename='images/' + name))

    return render_template('image.html', urls=urls)

@app.route('/api_data')
def api_data():
    return json.dumps({'value': '42'});

@app.route('/turnOnLights')
def turnOnLights():
    #Call to turn on lights function
    return "LIGHTS ARE ON"

@app.route('/turnOffLights')
def turnOffLights():
    #Call to turn off lights function
    return "LIGHTS ARE OFF"

@app.route('/take_picture')
def take_picture():
    return 'Capture'

def update():
    while True:
        print ('Hello World!') #Replace with capture to take picture.
        time.sleep(10)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
#update()
