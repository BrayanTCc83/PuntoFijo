from sympy import Symbol, sympify, solve, srepr
from func.normalizer import functions, fn_segmentate, fn_normalizer, regex_var, regex_symbol

class MathFunction:
    def __init__(self, function) -> None:
        self.original_function = function
        self.solveable_function = fn_segmentate(fn_normalizer(function))
        self.vars = []
        self.get_vars()

    def get_vars(self):
        for var in regex_var.finditer(self.solveable_function):
            if var.group() in functions:
                continue

            char = var[0]
            o = ord(char)
            if (o >= ord('A') and o <= ord('Z')) or (o >= ord('a') and o <= ord('z')) and char not in self.vars:
                print(f"Append symbolic var '{char}'")
                self.vars.append(char)

    def get_solvers(self):
        solvers = []
        self.symbolic = sympify(self.solveable_function)
        for v in self.vars:
            exec(f"{v} = Symbol('{v}')")
            exec(f"r = solve(self.symbolic, {v})")
            exec(f"print('Posible function solver:', r)")
            exec(f"solvers.append(({v}, r[0]))")
            exec("sentence = srepr(r[0])")
            exec("print(sentence)")
            """for it in regex_symbol.finditer(sentence):
                sentence = sentence.replace(it.group(), "Symbol('x')")
            print(sentence)
            z = sympify(sentence)
            print(z)"""

        return solvers

    def __str__(self) -> str:
        return f'<f = {self.original_function}>'