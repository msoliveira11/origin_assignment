#!/usr/bin/python3

#######################################
# filename: calc_interface.py         #
# author: Matheus Santos de Oliveira  #
# date: 12/10/2021                    #
# contact: msoliveira.eca@gmail.com   #
# description: interface to avoid     #
# the need of instantiate object      #
#######################################

import risk_calc_engine as rce

def calculateRisk(inputJson):
    calc = rce.riskCalcEngine(inputJson)
    return (calc.calculateRisk())
