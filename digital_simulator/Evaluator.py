#!/usr/bin/python
# vim: set fileencoding=utf8
# Created: April 5, 2008
# By: Antonio Chavez
#
# Extended Trinary Evaluator: Evaluates trinary expression containing unary
#   and dyatic gates
#

from Expr import *
from Trits import *

import doctest

dyatic_functions = {
    "+" : {False:"i01", None:"001", True:"111"},
    "*" : {False:"iii", None:"i00", True:"i01"}
}    

def expr_dyatic(expression, variables):
    first = variables[expression[0]]
    f_value = trit_bool[first]
 
    if len(expression) == 1:
        return (f_value, "")

    f_next = expression[1]
    if f_next in dyatic_functions:
        f_apply = dyatic_functions[f_next]
        result, next_expr = expr_recurse(expression[2:], variables)

        t_func = Trits(f_apply[f_value])
        t_sec = Trits(trit_string[result])
        return (evaluate_unary(t_func, t_sec))[0], next_expr

    elif f_next == "(":
        f_apply = dyatic_functions["*"]
        result, next_expr = expr_recurse(expression[2:], variables)

        if next_expr[0] != ")":
            raise "Expected \")\", found \"%s\"" % (next_expr[0])
 
        t_func = Trits(f_apply[f_value])
        t_sec = Trits(trit_string[result])
        return (Expr.evaluate_unary(t_func, t_sec))[0], next_expr[1:]

    elif f_next.isalpha():
        f_apply = dyatic_functions["*"]
        second = variables[f_next]

        t_func = Trits.Trits(f_apply[f_values])
        t_sec = Trist.Trits(second)
        return (Expr.evaluate_unary(t_func, t_sec))[0], expression[2:]

    else:
        return (f_value, expression[1:])

def expr_unary(expression, variables):
    count = 0
    while expression[count] in unary_functions:
        count = count + 1

    func = expression[:count]
    func = func + "a"

    result, next = expr_recurse(expression[count:], variables)
    e = Expr(func)
    return (e.evaluate(Trits(trit_string[result])), next)

def expr_recurse(expression, variables):
    if expression[0] in unary_functions:
        return expr_unary(expression, variables)
    elif expression[0].isalpha():
        return expr_dyatic(expression, variables)
    elif expression == "(":
        expression = expression[1:]
        result, next = expr_recurse(expression, variables)
        if next[0] != ")":
            raise "Expected \")\", found \"%s\"" % (next[0])
        return result, next[1:]
    else:
        raise "Unexpected character found \"%s\"" % (expression[0]) 

def trinary_eval(expression, variables):
    '''Evaluates trinary expression.  Unary and Dyatic functions supported:
        Unary: /, ∇, ∆, ¬, ⌐, ↘, ↗, ∩, ∪, ♨
        Dyatic: + (max), * (min)
       expression: String containing expression to evalutate
       variables: dictionary of variables and their values 
       returns: The result of evaluating the expression.

>>> print trinary_eval("//A+B", {"A" : "1", "B" : "1"})[0]
Variable: a
Gate: /
Gate: /
True
>>> print trinary_eval("//A+B", {"A" : "1", "B" : "0"})[0]
Variable: a
Gate: /
Gate: /
True
>>> print trinary_eval("//A+B", {"A" : "i", "B" : "0"})[0]
Variable: a
Gate: /
Gate: /
None
>>> print trinary_eval("//A+B", {"A" : "0", "B" : "0"})[0]
Variable: a
Gate: /
Gate: /
None
>>> print trinary_eval("//A+B", {"A" : "0", "B" : "1"})[0]
Variable: a
Gate: /
Gate: /
True
>>> print trinary_eval("/(A+/B*C)",{"A":"0","B":"0","C":"1"})
None
    '''
    result, lo = expr_recurse(expression, variables)
    return result

if __name__ == "__main__":
    doctest.testmod()
