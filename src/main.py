# pip3 freeze > requirements.txt
import func.function as func
import numpy as np
from func.normalizer import fn_normalizer, fn_segmentate

function = input("Ingresa la función a trabajar:\n")
start_x = float(input("Ingresa el inicio de rango a trabajar:\n"))
end_x = float(input("Ingresa el fin de rango a trabajar:\n"))
x0 = float(input("Ingrese el valor de x0:\n"))
tol = float(input("Ingresa la tolerancia:\n"))
f = func.MathFunction(function)
solvers = f.get_solvers()
x = np.arange(start_x, end_x + tol*10, tol*10)
f.solve(x, x0, tol)