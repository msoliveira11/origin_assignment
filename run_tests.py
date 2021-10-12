#!/usr/bin/python3

#######################################
# filename: run_tests.py              #
# author: Matheus Santos de Oliveira  #
# date: 12/10/2021                    #
# contact: msoliveira.eca@gmail.com   #
# description: test executor          #
#######################################

import calc_interface as ci
import json

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

def runTest(test : int, inputJson : json, outputJson : json) -> int:
    executionOutput = ci.calculateRisk(inputJson)
    outputDict = json.loads(executionOutput)
    referenceDict = json.loads(outputJson)
    insurances = ["auto","disability","home","life"]
    success = True
    for ins in insurances:
        if (outputDict[ins] != referenceDict[ins]):
            success = False
            print("Test " + str(test) + ": " + ins + \
                  " Expected: " + referenceDict[ins] + \
                  " Received: " + outputDict[ins] + '\n')
    if (success): return 1
    return 0
 
def main():
    testsOk = 0;
    tests = 0;
    testsOk += runTest(1,test1Input,test1Output)
    tests += 1
    testsOk += runTest(2,test2Input,test2Output)
    tests += 1
    testsOk += runTest(3,test3Input,test3Output)
    tests += 1
    testsOk += runTest(4,test4Input,test4Output)
    tests += 1
    testsOk += runTest(5,test5Input,test5Output)
    tests += 1

    print(str(testsOk) + " tests from " + str(tests) + \
          " were succesfully executed." + '\n')

if __name__ == "__main__":
    main()
