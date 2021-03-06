#!/usr/bin/python3

#######################################
# filename: calc_interface.py         #
# author: Matheus Santos de Oliveira  #
# date: 12/10/2021                    #
# contact: msoliveira.eca@gmail.com   #
# description: interface to expose    #
# the endpoint responsible by the     #
# risks calculation                   #
#######################################

import flask
import risk_calc_engine as rce

app = flask.Flask(__name__)

@app.route("/risk",methods = ["POST"])
def calculateRisk():
    """
    This method exposes the "risk" endpoint where the calculation method
    is called.
    Before starting the calculation, it calls another method responsible
    for verifying if the data received from the front-end is correct. If
    it has issues, return an error.
    If the data is fine, returns the insurances profiles.
    """
    calcDict = flask.request.json
    calc = rce.RiskCalcEngine(calcDict)
    success = checkPayloadIntegrity(calcDict)

    if (success == False):
        return flask.Response("Invalid input data", status=400)

    return (calc.calculateRisk())

@app.after_request
def add_header(response):
    """
    Sets the response header to JSON.
    """
    response.headers['Content-Type'] = 'application/JSON'
    return response 

# private methods
def checkPayloadIntegrity(payloadDict):
    """
    Checks if the input data received from the front-end
    is complete and if its' values are valid.
    """
    success = True
    # Checking age
    if "age" in payloadDict:
        if payloadDict["age"] < 0: success = False
    else:
        success = False
    # Checking dependents
    if "dependents" in payloadDict:
        if payloadDict["dependents"] < 0: success = False
    else:
        success = False
    # Checking house data
    if "house" in payloadDict:
        if (isinstance(payloadDict["house"],int) == False): 
            if "ownership_status" in payloadDict["house"]:
                if payloadDict["house"]["ownership_status"] != "owned" and \
                   payloadDict["house"]["ownership_status"] != "mortgaged":
                    success = False
            else:
                payloadDict["house"] = 0
    else:
        success = False
    # Checking income
    if "income" in payloadDict:
        if payloadDict["income"] < 0: success = False
    else:
        success = False
    # Checking vehicle data
    if "vehicle" in payloadDict:
        if (isinstance(payloadDict["vehicle"],int) == False): 
            if "year" in payloadDict["vehicle"]:
                if payloadDict["vehicle"]["year"] < 1900:
                    success = False
            else:
                payloadDict["vehicle"] = 0
    else:
        success = False
    # Checking marital_status
    if "marital_status" in payloadDict:
        if payloadDict["marital_status"] != "married" and \
           payloadDict["marital_status"] != "single":
            success = False
    else:
        success = False
    # Checking risk_questions
    if len(payloadDict["risk_questions"]) < 3:
        success = False

    return success

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.2')
