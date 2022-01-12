import json
import time
from flask import Flask
from flask import request
from flask import render_template
from flask import current_app
from flask import send_from_directory, jsonify
import random

app = Flask(__name__,static_folder='./static')

auths = open("auth/legal_auth_tokens.txt", "r")
legalauthcodes = auths.read().splitlines()
keys = open("auth/legal_keys.txt", "r")
legalkeys = keys.read().splitlines()

noauth = app.response_class(response = json.dumps({"message": "Did not get valid auth code in request"}), status = 400, mimetype='application/json')
nokey = app.response_class(response = json.dumps({"message": "Did not get valid key code in request"}), status = 400, mimetype='application/json')

apifailure = app.response_class(response = json.dumps({"message": "Your API call failed due to a server fault"}), status = 400, mimetype='application/json')


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
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.0

    datadict = open("data/studentinfo.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[0:15]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)

@app.route("/info-two", methods = ['GET'])
def info_two():
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.0

    datadict = open("data/studentinfo.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[15:43]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)

@app.route("/info-three", methods = ['GET'])
def info_three():
    auth = request.args.get('auth')
    key = request.args.get('key')
    failure_odds = 0.0

    datadict = open("data/studentinfo.json", "r")
    jsoner = json.loads(datadict.read())
    dictionary_to_return = jsoner[43:]
    
    return dataToRequest(failure_odds, dictionary_to_return, auth, key)


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
    
