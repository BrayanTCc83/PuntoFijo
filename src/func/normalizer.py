import re

regex_mult_x = re.compile("[0-9]+[a-zA-Z]+")
regex_mult_group = re.compile("[0-9]+([*][a-z])*[(][0-9a-zA-Z+*/-]+[)]")
regex_num = re.compile("[0-9]+")
regex_symbol = re.compile("Symbol[(]'[a-z]'[)]")

def fn_normalizer(function):
    global regex_mult_x, regex_num, regex_mult_group
    
    fn = function.replace('^', '**')
    for it in (regex_mult_x.finditer(function)):
        lit = it.group() 
        num = regex_num.match(lit)
        lit = lit.replace(num.group(), num.group() + "*")
        fn = fn.replace(it.group(), lit)
        
    for it in (regex_mult_group.finditer(function)):
        lit = it.group() 
        num = regex_num.match(lit)
        lit = lit.replace(num.group(), num.group() + "*")
        fn = fn.replace(it.group(), lit)
        
    return fn

functions = ["sin", "cos", "tan", "sec", "csc", "cot", "exp", "ln", "log"]
regex_var = re.compile("[a-z]+")
symbol = ord('x')
def fn_segmentate(function):
    global symbol, regex_var, functions

    fn = function
    for var in regex_var.finditer(fn):
        if var.group() in functions:
            continue

        [start, end] = var.span()
        fn = f"{fn[0:start]}{chr(symbol)}{fn[end:]}"
        symbol += 1
        if symbol > ord('z'):
            symbol = ord('p')
    
    return fn
