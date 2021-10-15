#!/usr/bin/python3

#######################################
# filename: run_tests.py              #
# author: Matheus Santos de Oliveira  #
# date: 12/10/2021                    #
# contact: msoliveira.eca@gmail.com   #
# description: test executor          #
#######################################

import calc_interface as ci
import risk_calc_engine as rce 
import json
import requests

# Test 1 - Provided within problem specification

test1Input = '{ \
    "age": 35, \
    "dependents": 2, \
    "house": {"ownership_status": "owned"}, \
    "income": 0, \
    "marital_status": "married", \
    "risk_questions": [0, 1, 0], \
    "vehicle": {"year": 2018} \
     }'

test1Output = '{ \
   "auto": "regular", \
   "disability": "ineligible", \
   "home": "economic", \
   "life": "regular" \
    }'

# Test 2 - All ineligible

test2Input = '{ \
    "age": 61, \
    "dependents": 2, \
    "house": 0, \
    "income": 0, \
    "marital_status": "married", \
    "risk_questions": [1, 1, 1], \
    "vehicle": 0 \
     }'

test2Output = '{ \
   "auto": "ineligible", \
   "disability": "ineligible", \
   "home": "ineligible", \
   "life": "ineligible" \
    }'

# Test 3 - All economic 

test3Input = '{ \
    "age": 25, \
    "dependents": 0, \
    "house": {"ownership_status": "owned"}, \
    "income":200001, \
    "marital_status": "married", \
    "risk_questions": [0, 0, 0], \
    "vehicle": {"year": 2015} \
     }'

test3Output = '{ \
   "auto": "economic", \
   "disability": "economic", \
   "home": "economic", \
   "life": "economic" \
    }'

# Test 4 - All regular

test4Input = '{ \
    "age": 35, \
    "dependents": 0, \
    "house": {"ownership_status": "owned"}, \
    "income":200001, \
    "marital_status": "single", \
    "risk_questions": [1, 1, 1], \
    "vehicle": {"year": 2017} \
     }'

test4Output = '{ \
   "auto": "regular", \
   "disability": "regular", \
   "home": "regular", \
   "life": "regular" \
    }'

# Test 5 - All responsible

test5Input = '{ \
    "age": 55, \
    "dependents": 1, \
    "house": {"ownership_status": "mortgaged"}, \
    "income":50000, \
    "marital_status": "single", \
    "risk_questions": [1, 1, 1], \
    "vehicle": {"year": 2019} \
     }'

test5Output = '{ \
   "auto": "responsible", \
   "disability": "responsible", \
   "home": "responsible", \
   "life": "responsible" \
    }'

def runUnitTest(test : int, inputJson : json, outputJson : json) -> int:
    rceObj = rce.RiskCalcEngine(json.loads(inputJson))
    executionOutput = rceObj.calculateRisk()
    outputDict = json.loads(executionOutput)
    referenceDict = json.loads(outputJson)
    insurances = ["auto","disability","home","life"]
    success = True
    for ins in insurances:
        if (outputDict[ins] != referenceDict[ins]):
            success = False
            print("unittest " + str(test) + ": " + ins + \
                  " expected: " + referenceDict[ins] + \
                  " received: " + outputDict[ins])
    if (success): return 1
    return 0

def runFullTest(test : int,inputJson : json, outputJson : json) -> int:
    url = 'http://127.0.0.2:5000/risk'
    payload = inputJson
    headers = {'content-type': 'application/json'}
    r = (requests.post(url, data=payload, headers=headers))
    outputDict = json.loads(r.text)
    referenceDict = json.loads(outputJson)
    insurances = ["auto","disability","home","life"]
    success = True
    for ins in insurances:
        if (outputDict[ins] != referenceDict[ins]):
            success = False
            print("Full test " + str(test) + ": " + ins + \
                  " expected: " + referenceDict[ins] + \
                  " received: " + outputDict[ins])
    if (success): return 1
    return 0

def main():
    testInput = []
    testOutput = []
    testInput.append(test1Input)
    testInput.append(test2Input)
    testInput.append(test3Input)
    testInput.append(test4Input)
    testInput.append(test5Input)
    testOutput.append(test1Output)
    testOutput.append(test2Output)
    testOutput.append(test3Output)
    testOutput.append(test4Output)
    testOutput.append(test5Output)

    unitTestsOk = 0
    fullTestsOk = 0
    for test in range(len(testInput)): 
        fullTestsOk += runFullTest(test,test1Input,test1Output)
        unitTestsOk += runUnitTest(test,test1Input,test1Output)

    print(str(unitTestsOk) + " unit tests out of " + str(len(testInput)) + \
          " were succesfully executed." + '\n')

    print(str(fullTestsOk) + " full tests out of " + str(len(testInput)) + \
          " were succesfully executed.")


if __name__ == "__main__":
    main()
