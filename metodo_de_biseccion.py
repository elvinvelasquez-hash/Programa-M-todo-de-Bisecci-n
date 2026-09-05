""" Estudiante: Elvin fernando velasquez Medina
Metodo: Biseccion
Descripcion: El metodo de biseccion es un metodo cerrado o de intervalos que nos permite encontrar
una aproximacion a la raiz de una ecuacion no lineal f(x) = 0. se inicia de un intervalo (a,b) en el 
cual la funcion cambia de signo, es decir f(a)*f(b)< 0, lo que garantiza (por el teorema del valor intermedio)
que existe al menos una raiz dentro de dicho intervalo.
en cada iteracion se calcula el punto medio: Xn = (a+b)/2
y se evalua f(Xn), dependiendo del signo de f(a)*f(Xn):
    si f(a)*f(Xn) < 0 (la raiz esta en (a,Xn) entonces b=Xn)
    si f(a)*f(Xn) > 0 (la raiz esta en (Xn,b) entonces a=Xn)
    si f(a)*f(Xn) = 0 ( Xn es la raiz exacta)
El proceso se repite hasta que el error relativo aproximado sea menor que la tolerancia
establecida por el usuario O hasta alcanzar el número máximo de interacciones permitido"""
import time
import math  # Aquí se podrán utilizar las siguientes funciones matemáticas (sin, cos, exp, sqrt, etc.)


def normalizar_expresion(expresion):
    """este normaliza expresiones escritas por el usuario para que puedan evaluarse correctamente."""
    expr = expresion.strip()
    expr = expr.replace("^", "**")
    expr = expr.replace("ln(", "log(")
    return expr


def evaluar_funcion(expresion, x):
    """
    aqui se evalúa la función f(x) ingresada por el usuario como una cadena de texto.
    Se utiliza eval() con un diccionario restringido que solo expone el
    módulo 'math' y la variable 'x', evitando el uso de funciones
    prediseñadas para encontrar raíces.
    """
    expr = normalizar_expresion(expresion)
    entorno_permitido = {
        "x": x,
        "math": math,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "asin": math.asin, "acos": math.acos, "atan": math.atan,
        "exp": math.exp, "log": math.log, "log10": math.log10,
        "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
        "abs": abs, "pow": pow, "ln": math.log
    }
    # pylint: disable=eval-used (Aquí le estoy diciendo a pylint que usar la función eval() es segura y que puede desactivar las reglas de evaluación potencialmente inseguras)
    valor = eval(expr, {"__builtins__": {}}, entorno_permitido)
    if isinstance(valor, complex):
        raise ValueError("La función evaluada no es real en ese punto.")
    return float(valor)


def validar_intervalo(expresion, a, b):
    """Verifica si el intervalo es válido para aplicar bisección."""
    try:
        fa = evaluar_funcion(expresion, a)
        fb = evaluar_funcion(expresion, b)
    except Exception as exc:
        raise ValueError("Error: la función no se puede evaluar en ese intervalo.") from exc

    if math.isclose(fa, 0.0, abs_tol=1e-12) or math.isclose(fb, 0.0, abs_tol=1e-12):
        return True

    if fa * fb >= 0:
        raise ValueError("Error: no existe cambio de signo en el intervalo [a, b].")

    return True


def solicitar_datos():
    """
    aqui solicitamos al usuario todos los datos necesarios para ejecutar el método:
    la función, el intervalo inicial [a, b], el número máximo de
    iteraciones y el error relativo (tolerancia) deseado.
    """
    print("-" * 70)
    print("                    MÉTODO DE BISECCIÓN")
    print("Estudiante: Elvin Fernando Velasquez Medina")
    print("cuenta: 20251031851")
    print("Descripción: Este programa implementa el método de bisección para encontrar una aproximación a la raíz de una función no lineal f(x) = 0.")
    print("-" * 70)
    print("            Ingrese f(x) usando 'x' como variable.")
    print("-" * 70)

    expresion = input("f(x) = ").strip()

    while True:
        try:
            a = float(input("Valor inicial 'a' (límite inferior): "))
            b = float(input("Valor inicial 'b' (límite superior): "))
            if a >= b:
                print("Error: 'a' debe ser menor que 'b'. Intente de nuevo.\n")
                continue

            try:
                validar_intervalo(expresion, a, b)
            except ValueError as exc:
                print(f"{exc}\n")
                print("Ingrese otro intervalo [a, b] que sí cumpla con cambio de signo.\n")
                continue

            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.\n")

    while True:
        try:
            max_iter = int(input("Número máximo de iteraciones: "))
            if max_iter <= 0:
                print("Debe ser un entero positivo.\n")
                continue
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.\n")

    while True:
        try:
            error_relativo = float(input("Error relativo (tolerancia, ej. 0.0001): "))
            if error_relativo <= 0:
                print("Debe ser un número positivo.\n")
                continue
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número.\n")

    return expresion, a, b, max_iter, error_relativo


def biseccion(expresion, a, b, max_iter, error_relativo):
    """
    aqui es donde el programa implementaroa el método de bisección.

    Parámetros:
        expresion       : es la cadena de texto con f(x)
        a, b            : son los extremos del intervalo inicial
        max_iter        : es el número máximo de iteraciones permitidas
        error_relativo  : es la tolerancia del error relativo aproximado

    Retorna:
        raiz            : es la aproximación final de la raíz
        iteracion       : es el número total de iteraciones realizadas
        error_final     : es el último error relativo calculado
        tabla           : es la lista con los datos de cada iteración
    """
    validar_intervalo(expresion, a, b)
    fa = evaluar_funcion(expresion, a)
    fb = evaluar_funcion(expresion, b)

    # Verificación de la condición fundamental del método: exista cambio de signo
    if fa * fb >= 0 and not math.isclose(fa, 0.0, abs_tol=1e-12) and not math.isclose(fb, 0.0, abs_tol=1e-12):
        raise ValueError(
            "Error: no existe cambio de signo en el intervalo [a, b]."
        )

    tabla = []
    xn_anterior = None
    error_actual = None
    iteracion = 0

    # Caso especial: si alguno de los extremos ya es raíz exacta
    if fa == 0:
        return a, 0, 0.0, [(0, a, fa, None)]
    if fb == 0:
        return b, 0, 0.0, [(0, b, fb, None)]

    while iteracion < max_iter:
        iteracion += 1

        xn = (a + b) / 2.0        # aqui estria el punto medio del intervalo
        fxn = evaluar_funcion(expresion, xn)  # Evaluación de f en el punto medio

        # Cálculo del error relativo aproximado (a partir de la 2da iteración)
        if xn_anterior is not None:
            error_actual = abs((xn - xn_anterior) / xn) * 100
        else:
            error_actual = None

        tabla.append((iteracion, xn, fxn, error_actual))

        # Condición de parada por error relativo
        if error_actual is not None and error_actual < error_relativo * 100:
            break

        # Condición de parada: raíz exacta encontrada
        if fxn == 0:
            break

        # Actualización del intervalo según el signo de f(a)*f(xn)
        if fa * fxn < 0:
            b = xn
            fb = fxn
        else:
            a = xn
            fa = fxn

        xn_anterior = xn

    raiz = xn
    error_final = error_actual if error_actual is not None else float("nan")
    return raiz, iteracion, error_final, tabla


def mostrar_tabla(tabla):
    """
    Imprime en pantalla la tabla de iteraciones con las columnas:
    N° iteración, aproximación de la raíz (xr), f(xr) y error relativo (%).
    """
    print("\n" + "-" * 70)
    print(f"{'Iter':>5} | {'xn (raíz aprox.)':>20} | {'f(xn)':>18} | {'Error (%)':>12}")
    print("-" * 70)
    for fila in tabla:
        iteracion, xr, fxr, error = fila
        error_txt = f"{error:.7f}" if error is not None else "     ---"
        print(f"{iteracion:>5} | {xr:>20.7f} | {fxr:>18.7f} | {error_txt:>12}")
    print("-" * 70)


def main():
    """Función principal: orquesta la entrada de datos, el cálculo y la salida."""
    expresion, a, b, max_iter, error_relativo = solicitar_datos()

    try:
        raiz, iteraciones, error_final, tabla = biseccion(
            expresion, a, b, max_iter, error_relativo
        )
    except ValueError as e:
        print(f"\nError: {e}")
        return
    except Exception as e:
        print(f"\nOcurrió un error al evaluar f(x): {e}")
        return

    mostrar_tabla(tabla)

    print("\n" + "-" * 70)
    print("                                   RESULTADOS FINALES")
    print("-" * 70)
    print(f"Raíz aproximada encontrada : {raiz:.7f}")
    print(f"Número total de iteraciones: {iteraciones}")
    if error_final == error_final:  # comprueba que no sea NaN
        print(f"Error final obtenido       : {error_final:.7f} %")
    else:
        print("Error final obtenido       : No calculable (una sola iteración)")
    print("-" * 70)


if __name__ == "__main__":
    main()
time.sleep(20)  # Pausa de 10 segundo antes de finalizar el programa
