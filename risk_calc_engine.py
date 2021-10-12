#######################################
# filename: risk_calc_engine.py       #
# author: Matheus Santos de Oliveira  #
# date: 12/10/2021                    #
# contact: msoliveira.eca@gmail.com   #
# description: main file of the       #
# insurance risk engine calculation   #
#######################################

import json
from datetime import date

class riskCalcEngine:
    """
    Class responsible for manipulating the user 
    input payload data and calculating his/her insurance needs.
    
    This class was implemented based on the description and the
    business rules written in file 'problem_specifications.txt'
    available in this repository.

    Attibutes
    _________
    pD : dict
        A dictionary that will receive the json data decoded
    cD : dict
        A dictionary meant to store calculation data

    Methods
    _______
    calcBaseScore()
        Calculates base value for score calculations.
    calcHomeScore()
        Calculates home score value.
    calcAutoScore()
        Calculates auto score value.
    calcDisabilityScore()
        Calculates disability score value.
    calcLifeScore()
        Calculates life score value.
    evaluateResult(value)
        Transforms a score integer value into a plan string.
    buildOutput()
        Gathers calculation data and returns a json object 
        formatted as specified by the documentation.
    calculateRisk()
        Main method that calculates the scores by calling
        other methods and returns the insurance plans as
        a json object.

    """

    def __init__(self, payload: json):
        """
        Constructor method meant to decode json payload
        and to create an internal dict to store calculation data.

        Parameters
        __________
        payload : json
            The json payload received by the front-end.

         """

        self.pD = json.loads(payload)
        # pD stands for payloadData
        self.cD = {}
        # cD stands for calculationData, this dict will
        # be used to keep track of data used within calculations
        self.cD["mortgageDisability"] = 0
        # check line #93

    def calcBaseScore(self):
        """
        Calculates base value for score calculations.
        """

        self.cD["baseScore"] = self.pD["risk_questions"][0] + \
                               self.pD["risk_questions"][1] + \
                               self.pD["risk_questions"][2] 

    def calcHomeScore(self):
        """
        Calculates home score value.
        """

        if "house" in self.pD:
            if (isinstance(self.pD["house"],int) == False): # From here we may calculate homeScore
                homeScore = self.cD["baseScore"]
                self.cD["homeEligibility"] = 1
                if (self.pD["house"]["ownership_status"] == "mortgaged"): # Rule 10.1
                    homeScore += 1
                    self.cD["mortgageDisability"] = 1 # Will be used on disability score calculation
                if (self.pD["age"]<40): # Rule 8.1
                    homeScore -= 1
                if (self.pD["age"]<30): # Rule 7.1
                    homeScore -= 1
                if (self.pD["income"]>200000): # Rule 9.1
                    homeScore -= 1
                self.cD["homeScore"] = homeScore
            else:
                self.cD["homeEligibility"] = 0 # Rule 4
        else:
            self.cD["homeEligibility"] = 0 # Rule 4

    def calcAutoScore(self):
        """
        Calculates auto score value.
        """

        if "vehicle" in self.pD:
            #if "year" in self.pD["vehicle"]: # From here we may calculate autoScore
            if (isinstance(self.pD["vehicle"],int) == False): # From here we may calculate autoScore
                autoScore = self.cD["baseScore"]
                self.cD["autoEligibility"] = 1
                if (date.today().year - self.pD["vehicle"]["year"] < 5): # Rule 13
                    autoScore += 1
                if (self.pD["age"]<40): # Rule 8.2
                    autoScore -= 1
                if (self.pD["age"]<30): # Rule 7.2
                    autoScore -= 1
                if (self.pD["income"]>200000): # Rule 9.2
                    autoScore -= 1
                self.cD["autoScore"] = autoScore
            else:
                self.cD["autoEligibility"] = 0 # Rule 3
        else:
            self.cD["autoEligibility"] = 0 # Rule 3

    def calcDisabilityScore(self):
        """
        Calculates disability score value.
        """

        if (self.pD["income"] > 0):
            if (self.pD["age"] < 60): # From here we may calculate disabilityScore
                disabilityScore = self.cD["baseScore"]
                self.cD["disabilityEligibility"] = 1
                if (self.pD["age"]<40): # Rule 8.3
                    disabilityScore -= 1
                if (self.pD["age"]<30): # Rule 7.3
                    disabilityScore -= 1
                if (self.pD["income"]>200000): # Rule 9.3
                    disabilityScore -= 1
                disabilityScore += self.cD["mortgageDisability"] # Rule 10.2
                if (self.pD["dependents"] > 0):
                    disabilityScore += 1 # Rule 11.1
                if (self.pD["marital_status"] == "married"):
                    disabilityScore -= 1 # Rule 12.2
                self.cD["disabilityScore"] = disabilityScore
            else:
                self.cD["disabilityEligibility"] = 0 # Rule 5
        else:
            self.cD["disabilityEligibility"] = 0 # Rule 2

    def calcLifeScore(self):
        """
        Calculates life score value.
        """

        if (self.pD["age"] < 60): # From here we may calculate lifeScore
            lifeScore = self.cD["baseScore"]
            self.cD["lifeEligibility"] = 1
            if (self.pD["age"]<40): # Rule 8.4
                lifeScore -= 1
            if (self.pD["age"]<30): # Rule 7.4
                lifeScore -= 1
            if (self.pD["income"]>200000): # Rule 9.4
                lifeScore -= 1
            if (self.pD["dependents"] > 0):
                lifeScore += 1 # Rule 11.2
            if (self.pD["marital_status"] == "married"):
                lifeScore += 1 # Rule 12.1
            self.cD["lifeScore"] = lifeScore
        else:
            self.cD["lifeEligibility"] = 0 # Rule 5
       
    def evaluateResult(self, value: int) -> str:
        """
        Transforms a score integer value into a plan string.

        Output
        ______
        str : The matching string related to score value.
        """

        if (value <= 0):
            return "economic" # Rule 14
        if (value >= 3):
            return "responsible" # Rule 16
        return "regular" # Rule 15

    def buildOutput(self) -> json:
        """
        Gathers calculation data and returns a json object 
        formatted as specified by the documentation.

        Output
        ______
        json : Insurance plans data in a json format.
        """

        outputDict = {}
        if (self.cD["autoEligibility"] == 1):
            outputDict["auto"] = self.evaluateResult(self.cD["autoScore"])
        else:
            outputDict["auto"] = "ineligible"

        if (self.cD["disabilityEligibility"] == 1):
            outputDict["disability"] = self.evaluateResult(self.cD["disabilityScore"])
        else:
            outputDict["disability"] = "ineligible"

        if (self.cD["homeEligibility"] == 1):
            outputDict["home"] = self.evaluateResult(self.cD["homeScore"])
        else:
            outputDict["home"] = "ineligible"

        if (self.cD["lifeEligibility"] == 1):
            outputDict["life"] = self.evaluateResult(self.cD["lifeScore"])
        else:
            outputDict["life"] = "ineligible"

        return json.dumps(outputDict)

    def calculateRisk(self) -> json:
        """
        Main method that calculates the scores by calling
        other methods and returns the insurance plans as
        a json object.

        Output
        ______
        json : Insurance plans data in a json format.
        """

        self.calcBaseScore()
        self.calcHomeScore()
        self.calcAutoScore()
        self.calcDisabilityScore()
        self.calcLifeScore()
        return self.buildOutput() 
