import json
import time
from flask import Flask
from flask import request
from flask import render_template
from flask import current_app
from flask import send_from_directory, jsonify
from datetime import datetime
import random

app = Flask(__name__,static_folder='./static')

auths = open("auth/legal_auth_tokens.txt", "r")
legalauthcodes = auths.read().splitlines()
keys = open("auth/legal_keys.txt", "r")
legalkeys = keys.read().splitlines()

noauth = app.response_class(response = json.dumps({"message": "Did not get valid auth code in request"}), status = 400, mimetype='application/json')
nokey = app.response_class(response = json.dumps({"message": "Did not get valid key code in request"}), status = 400, mimetype='application/json')
inactive = app.response_class(response = json.dumps({"message": "This endpoint is inactive due to maintenance."}), status = 503, mimetype='application/json')
apifailure = app.response_class(response = json.dumps({"message": "Your API call failed due to a server fault"}), status = 500, mimetype='application/json')


#########################################USERS STUFF#############################################

@app.route('/post-test', methods = ['POST'])
def post_test():
    try:
        thiskey = request.headers.get("X-Api-Key")
    except:
        return nokey
    
    body = json.loads(request.data.decode('utf-8'))
    try:
        auth = body["auth"]
        return genericJSONLoader(0.0, 0.0, "data/integration.json", auth, thiskey)
    except:
        return noauth

@app.route('/get-test', methods = ['GET'])
def get_test():
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure = 0.0
    removal_odds = 0.0
    return genericJSONLoader(failure, removal_odds, "data/integration.json", auth, key)

@app.route("/info-one", methods = ['GET'])
def info_one():
    hour = datetime.now().time().hour
    if not((hour >= 0 and hour <= 6) or (hour >= 12 and hour <= 18)):
        # inactive
        return inactive
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.1

    datadict = open("data/studentInfoGet.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[0:15]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)

@app.route("/info-two", methods = ['GET'])
def info_two():
    hour = datetime.now().time().hour
    if not((hour >= 0 and hour <= 6) or (hour >= 12 and hour <= 18)):
        # inactive
        return inactive
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.1

    datadict = open("data/studentInfoGet.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[15:43]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)

@app.route("/info-three", methods = ['GET'])
def info_three():
    hour = datetime.now().time().hour
    if not((hour >= 0 and hour <= 6) or (hour >= 12 and hour <= 18)):
        # inactive
        return inactive
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.1

    datadict = open("data/studentInfoGet.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[43:]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)



@app.route("/info-four", methods = ['GET'])
def info_four():
    hour = datetime.now().time().hour
    if ((hour >= 0 and hour <= 6) or (hour >= 12 and hour <= 18)):
        # inactive
        return inactive
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.1

    datadict = open("data/studentInfoGet.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[0:15]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)

@app.route("/info-five", methods = ['GET'])
def info_five():
    hour = datetime.now().time().hour
    if ((hour >= 0 and hour <= 6) or (hour >= 12 and hour <= 18)):
        # inactive
        return inactive
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.1

    datadict = open("data/studentInfoGet.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[15:43]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)

@app.route("/info-six", methods = ['GET'])
def info_six():
    hour = datetime.now().time().hour
    if ((hour >= 0 and hour <= 6) or (hour >= 12 and hour <= 18)):
        # inactive
        return inactive
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.1

    datadict = open("data/studentInfoGet.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[43:]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)


@app.route("/get-active", methods = ['GET'])
def get_active():
    hour = datetime.now().time().hour
    output = list()
    if ((hour >= 0 and hour <= 6) or (hour >= 12 and hour <= 18)):
        output = ["/info-one", "/info-two", "/info-three"]
    else:
        output = ["/info-four", "/info-five", "/info-six"]    
    return make200(output)


#############################################GENERIC STUFF###########################################

def dataToRequest(failure_odds, dictionary_to_return, auth, key):
    print(auth)

    # Ensure that auth and key data are legal
    if not(auth in legalauthcodes):
        return noauth
    else:
        index = legalauthcodes.index(auth)
        if (legalkeys[index] != key):
            return nokey

    # Mock a server fault some percent of the time
    toabort = random.random()
    if (toabort < failure_odds):
        return apifailure

    # If you have passed the auth, key, and fault test, then you will receive your data
    return make200(dictionary_to_return)
    

    
    

def genericJSONLoader(failure, removal_odds, file, auth, key):
    # fails failure percent of the time
    # removes an element removal_odds percent of the time
    
    if not(auth in legalauthcodes):
        return noauth
    else:
        index = legalauthcodes.index(auth)
        print(index)
        if (legalkeys[index] != key):
            return nokey
    
    toremove = random.random()
    toabort = random.random()
    rent = open(file, "r")
    jsoner = json.loads(rent.read())
    
    if (toremove < removal_odds):
        numtoremove = 1 + int(random.random() * 2)
        for _ in range(numtoremove):
            jsoner.pop(int(random.random() * len(jsoner)))
    if (toabort < failure):
        return apifailure
    
    return make200(jsoner)

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
    
