from sympy import symbols, sympify,lambdify, sin, cos, tan, sqrt, log, exp, asin, acos, atan
import os
import platform
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import tkinter as tk
matplotlib.use('TkAgg')  # Usa TkAgg como backend, o comenta esta línea para el backend por defecto
import matplotlib.pyplot as plt


# Definir 'x' en el ámbito global
x = symbols('x')


# Solicitar al usuario la entrada de la función
def solicitar_funcion():
    print("Ingresa la función f(x) = 0, donde 'x' es la variable: ")
    expresion_str = input()

    # Usar la variable 'x' global
    expresion = sympify(expresion_str)

    # Función para evaluar la expresión en un punto dado
    def f(valor):
        return expresion.subs(x, valor).evalf()

    return f, expresion  # Retornar tanto la función como la expresión

# Método de bisección adaptado para usar la función de evaluación
def biseccion(f, a, b, tol, modo='todas'):
    if f(a) * f(b) >= 0:
        print("El método de bisección no puede aplicarse si f(a) y f(b) tienen el mismo signo.")
        return None

    c = a
    c_anterior = None
    error = float('inf')
    iteracion = 0
    historial_iteraciones = []
    
    while True:
        c_anterior = c
        c = (a + b) / 2.0
        if iteracion > 0:
            error = abs(c - c_anterior)
        historial_iteraciones.append((iteracion, c, error))
        
        if error <= tol:
            break
        
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
        
        iteracion += 1
    
    if modo == 'todas':
        for it, val, err in historial_iteraciones:
            if it == 0:
                print(f"Iteración {it}: c = {val}")
            else:
                print(f"Iteración {it}: c = {val}, error = {err}")
            
    elif modo == 'primeras_ultimas':
        primeras = historial_iteraciones[:2]
        ultimas = historial_iteraciones[-2:]
        for it, val, err in primeras + ultimas:
            if it == 0:
                print(f"Iteración {it}: c = {val}")
            else:
                print(f"Iteración {it}: c = {val}, error = {err}")

    print(f"La raíz encontrada con la tolerancia de {tol} es aproximadamente: {c}")
    return c


def limpiar_consola():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def instruccion():
    limpiar_consola()
    print("Ingresa los datos de la siguiente manera: ")
    print("Suma '+' Resta '-' Multiplicación '*' Division '/' Potencia '**' Raíz 'sqrt(x)'")
    print("Logaritmo 'log(x, base)' Exponencial 'exp(x)' Seno 'sin(x)' Coseno 'cos(x)' Tangente 'tan(x)' ")
    print("Arcoseno 'asin(x)' Arcocoseno 'acos(x)' Arcotangente 'atan(x)' ")





def graficar_funcion_con_raiz(f_simbolica, a, b, raiz):
    # 'x' ya está definida en el ámbito global, por lo que no necesita ser pasada a 'lambdify'
    f_num = lambdify(x, f_simbolica, 'numpy')

    # Crear valores para x en un rango alrededor de la raíz encontrada
    x_vals = np.linspace(a - 1, b + 1, 400)
    y_vals = f_num(x_vals)

    # Graficar la función y marcar la raíz encontrada
    plt.plot(x_vals, y_vals, label='f(x)')
    plt.plot(raiz, f_num(raiz), 'ro', label='Raíz encontrada')
    plt.axhline(0, color='black', lw=0.5)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Gráfica de f(x) con la raíz encontrada')
    plt.legend()
    plt.grid(True)
    plt.show()

def program(modo='todas'):
    limpiar_consola()

    f, expresion = solicitar_funcion()  # Actualizar para recibir 'expresion'
    a = float(input("Ingresa el límite inferior del intervalo a: "))
    b = float(input("Ingresa el límite superior del intervalo b: "))
    tol = float(input("Ingresa la tolerancia deseada: "))
    raiz = biseccion(f, a, b, tol, modo)  # Asegúrate de que 'biseccion' devuelva 'c'

    graficar_funcion_con_raiz(expresion, a, b, raiz) 


continuar = True
while continuar:
    print("¿Qué desea hacer?")
    print("1. Leer instrucciones")
    print("2. Ejecutar programa y ver todas las iteraciones")
    print("3. Ejecutar programa y ver solo las dos primeras y las dos últimas iteraciones")
    print("4. Salir")
    
    opcion = input("Ingrese su opción: ")
    if opcion == "1":
        instruccion()
    elif opcion == "2":
        program(modo='todas')
    elif opcion == "3":
        program(modo='primeras_ultimas')
    elif opcion == "4":
        continuar = False
    else:
        print("Opción inválida. Intente nuevamente.")
    input("Presiona Enter para continuar...")  # Agregar una pausa antes de limpiar la consola
    limpiar_consola()

