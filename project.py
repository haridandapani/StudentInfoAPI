import json
import time
from flask import Flask
from flask import request
from flask import render_template
from flask import current_app
from flask import send_from_directory, jsonify
import random

app = Flask(__name__,static_folder='./static')

apikey = "59jIWfBWdD426XjAdRAjWaF9u5WJTmgm4tzPd3Ik"

nokey = app.response_class(response = json.dumps({"message": "Did not get valid key code in request"}), status = 400, mimetype='application/json')

horoscopes = {'Tim': 'Sagittarius', 'Hari': 'Virgo', 'Eva': 'Sagittarius', 'Colton': 'Aries', 'Galen': 'Aries', 'Anika': 'Libra', 'Siddharth': 'Scorpio'}

@app.route('/introResource', methods = ['GET'])
def introResource():
    output = {'message': 'Congrats! You have successfully completed a basic GET request!'}
    return make200(output)

@app.route('/securedResource', methods = ['GET', 'POST'])
def securedResource():
    try:
        thiskey = request.headers.get("X-Api-Key")
    except:
        return nokey
    if (thiskey == None or thiskey != apikey):
        return nokey

    if request.method == 'GET':
        output = {'message': 'Congrats! You have successfully completed a GET request to a protected resource!'}
        return make200(output)
    else:
        body = json.loads(request.data.decode('utf-8'))
        try:
            name = body["name"]
            output = {'message': 'Congrats, '+name+'! You have successfully completed a POST request to a protected resource!'}
            return make200(output)
        except:
            output = {'message': 'Did not get a value for the name'}
            return make200(output, 401)
    
@app.route('/horoscopeResource', methods = ['GET'])
def horoscopeResource():

    try:
        thiskey = request.headers.get("X-Api-Key")
    except:
        return nokey
    if (thiskey == None or thiskey != apikey):
        return nokey

    name = request.args.get('name')
    

    if (name):
        try:
            horoscope = horoscopes[name]
        except:
            horoscope = 'None'
        output = {"message": horoscope}
        return make200(output)

    else:
        output = {"message": horoscopes}
        return make200(output)

@app.route('/addHoroscope', methods = ['POST'])
def addHoroscope():

    try:
        thiskey = request.headers.get("X-Api-Key")
    except:
        return nokey
    if (thiskey == None or thiskey != apikey):
        return nokey

    body = json.loads(request.data.decode('utf-8'))
    try:
        name = body["name"]
        horoscope = body["horoscope"]
        if name in horoscopes:
            horoscopes[name] = horoscopes[name] + " OR " + horoscope
        else:
            horoscopes[name] = horoscope
        output = {'message': 'Added Horoscope!'}
        return make200(output)
    except:
        output = {'message': 'Did not get a value for the name and/or horoscope'}
        return make200(output, 401) 

    

        

#############################################GENERIC STUFF###########################################

def make200(jsoner, mystatus = 200):
    response = app.response_class(
        response=json.dumps(jsoner),
        status=mystatus,
        mimetype='application/json'
        )
    return response

def main():
    app.run(threaded=True, port=5000)

if __name__ == '__main__':
    main()
    
