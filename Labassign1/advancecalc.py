# Q4) Create a Python program that functions as an advanced calculator. It
# should take user input for mathematical expressions and evaluate
# them, supporting basic operations, parentheses, and scientific
# notation.

import math
def advancedcalc():
    print("Enter the mathematical expression: ")
    exp = input()
    print("Result: ", eval(exp))
advancedcalc()