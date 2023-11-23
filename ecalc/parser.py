#! /usr/bin/env python

import ast
from math import *

x = 10
formula = "sin(x)*x**2"
formula = "cos(x)*x**2"
formula = "hex(int(e+pi+tau))"
s = "0x6a48f8"
formula = "int(s, 16)"
try:
    result = eval(compile(ast.parse(formula, mode='eval'), filename='', mode='eval'))
except:
    print("Shit happened")
    exit(1)
print("Result:", result)
