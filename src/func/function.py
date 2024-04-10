import matplotlib.pyplot as plt
from sympy.abc import x
from sympy import Symbol, sympify, solve, srepr, lambdify, diff
from func.normalizer import functions, fn_segmentate, fn_normalizer, regex_var, regex_symbol

class MathFunction:
    def __init__(self, function) -> None:
        self.original_function = function
        self.solveable_function = fn_segmentate(fn_normalizer(function))
        self.vars = []
        self.solvers = []
        self.get_vars()

    def get_vars(self):
        for var in regex_var.finditer(self.solveable_function):
            if var.group() in functions:
                continue

            char = var[0]
            o = ord(char)
            if (o >= ord('A') and o <= ord('Z')) or (o >= ord('a') and o <= ord('z')) and char not in self.vars:
                self.vars.append(char)

    def get_solvers(self):
        if(len(self.solvers) > 0):
            return self.solvers
        self.symbolic = sympify(self.solveable_function)
        for v in self.vars:
            exec(f"{v} = Symbol('{v}')")
            exec(f"r = solve(self.symbolic, {v})")
            exec("sentence = srepr(r[-1])")
            exec("for it in regex_symbol.finditer(sentence):\n\tsentence = sentence.replace(it.group(), \"Symbol('x')\")")
            exec("z = sympify(sentence)")
            exec(f"self.solvers.append((Symbol('x'), z))")

        return self.solvers
    
    def solve(self, x_arr, x0, tol):
        # Eligiendo el despeje apropiado mediante tabla
        print("\n--------------------------------------------------------------------------------------------------------------------------")
        print("| #Caso | Despeje                             | Derivada                             | Evaluacion en x0      | Criterio  |")
        print("--------------------------------------------------------------------------------------------------------------------------")
        i = 0
        funcion_solver = None
        for symbol, solver in self.solvers:
            i+=1
            f = chr(101 + i)
            derivada = diff(solver, symbol)
            derivada_lam = lambdify(symbol, derivada)
            evaluacion = derivada_lam(x0 + 0j).real
            criterio = abs(evaluacion) < 1
            if criterio:
                funcion_solver = solver
            print(f"| %5d | {f}(x)=%30s | {f}'(x)=%30s | {f}'(%6f)=%8f | %9s |" % (
                i, solver, derivada, x0, evaluacion, criterio if "Cumple" else "No cumple" ) )
        print("--------------------------------------------------------------------------------------------------------------------------")
            
        # Funcion elegida
        print(f"\nFuncion a trabajar: {funcion_solver}\n")

        # Iteraciones
        print("----------------------------------------------------------------------------------")
        print("|  i  | x            | %30s | Error        | Criterio  |" % (funcion_solver))
        print("----------------------------------------------------------------------------------")
        x = x0
        y = x0
        i = -1
        error = 100
        criterio = False
        function_lam = lambdify(Symbol('x'), funcion_solver)
        while not criterio:
            i += 1
            y = function_lam(x + 0j).real
            plt.plot([x, x], [x, y], 'r')
            error = abs(x - y)
            criterio = error <= tol
            print("| %3d | %12f |                   %12f | %12f | %9s |" % (i, x, y, error, criterio if "Cumple" else "No cumple"))
            plt.plot([x, y], [y, y], 'r')
            x = y
        print("----------------------------------------------------------------------------------")

        print(f"\nSolucion: {y}, Iteracion: {i}")
        # Mostrando grafica
        plt.ylabel(funcion_solver)
        self.show(x_arr, function_lam)

    def show(self, x_arr, desp):
        solvers = self.get_solvers()
        func_symbolic = sympify(fn_normalizer(self.original_function))
        func = lambdify(x, func_symbolic)

        y = []
        for x_val in x_arr:
            y.append(desp(x_val))
        plt.plot(x_arr, y, 'g')
        
        y = []
        for x_val in x_arr:
            y.append(func(x_val))
        plt.plot(x_arr, x_arr)

        plt.grid(True)
        plt.xlabel("X")
        plt.title(f"Punto fijo: {self.original_function}")
        plt.show()

    def __str__(self) -> str:
        return f'<f = {self.original_function}>'