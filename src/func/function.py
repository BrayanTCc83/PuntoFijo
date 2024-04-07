from sympy import Symbol, sympify, solve

class MathFunction:
    def __init__(self, function) -> None:
        self.function = function
        self.vars = []
        self.get_vars()
        self.to_symbolic()

    def get_vars(self):
        for char in (self.function):
            o = ord(char)
            if (o >= ord('A') and o <= ord('Z')) or (o >= ord('a') and o <= ord('z')) and char not in self.vars:
                print(f"Append symbolic var '{char}'")
                self.vars.append(char)

    def to_symbolic(self):
        self.symbolic = sympify(self.function)
        print(self.symbolic)
        for v in self.vars:
            exec(f"{v} = Symbol('{v}')")
            exec(f"r = solve(self.symbolic, {v})")
            exec(f"print(r)")

    def __str__(self) -> str:
        return f'<Funcion = {self.function}, Independientes: {self.vars}>'