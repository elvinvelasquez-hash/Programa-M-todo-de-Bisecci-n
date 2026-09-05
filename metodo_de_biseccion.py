import math
import pandas as pd
import streamlit as st

# Configuración del título de la página
st.set_page_config(page_title="Método de Bisección", layout="centered")

st.title("MÉTODO DE BISECCIÓN")
st.markdown("**Estudiante:** Elvin Fernando Velasquez Medina")
st.markdown("**Cuenta:** 20251031851")
st.info(
    "Esta aplicación implementa el método de bisección para encontrar una "
    "aproximación a la raíz de una función no lineal f(x) = 0."
)


def normalizar_expresion(expresion):
    expr = expresion.strip()
    expr = expr.replace("^", "**")
    expr = expr.replace("ln(", "log(")
    return expr


def evaluar_funcion(expresion, x):
    expr = normalizar_expresion(expresion)
    entorno_permitido = {
        "x": x,
        "math": math,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "exp": math.exp,
        "log": math.log,
        "log10": math.log10,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
        "pow": pow,
        "ln": math.log,
    }
    valor = eval(expr, {"__builtins__": {}}, entorno_permitido)
    if isinstance(valor, complex):
        raise ValueError("La función evaluada no es real en ese punto.")
    return float(valor)


def validar_intervalo(expresion, a, b):
    try:
        fa = evaluar_funcion(expresion, a)
        fb = evaluar_funcion(expresion, b)
    except Exception as exc:
        raise ValueError(
            "Error: la función no se puede evaluar en ese intervalo."
        ) from exc

    if math.isclose(fa, 0.0, abs_tol=1e-12) or math.isclose(
        fb, 0.0, abs_tol=1e-12
    ):
        return True

    if fa * fb >= 0:
        raise ValueError(
            "Error: no existe cambio de signo en el intervalo [a, b]."
        )

    return True


def biseccion(expresion, a, b, max_iter, error_relativo):
    validar_intervalo(expresion, a, b)
    fa = evaluar_funcion(expresion, a)
    fb = evaluar_funcion(expresion, b)

    if (
        fa * fb >= 0
        and not math.isclose(fa, 0.0, abs_tol=1e-12)
        and not math.isclose(fb, 0.0, abs_tol=1e-12)
    ):
        raise ValueError(
            "Error: no existe cambio de signo en el intervalo [a, b]."
        )

    tabla = []
    xn_anterior = None
    error_actual = None
    iteracion = 0

    if fa == 0:
        return a, 0, 0.0, [(0, a, fa, None)]
    if fb == 0:
        return b, 0, 0.0, [(0, b, fb, None)]

    while iteracion < max_iter:
        iteracion += 1
        xn = (a + b) / 2.0
        fxn = evaluar_funcion(expresion, xn)

        if xn_anterior is not None:
            error_actual = abs((xn - xn_anterior) / xn) * 100
        else:
            error_actual = None

        tabla.append((iteracion, xn, fxn, error_actual))

        if error_actual is not None and error_actual < error_relativo * 100:
            break

        if fxn == 0:
            break

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


# Formulario de entrada en la interfaz
st.subheader("Parámetros de entrada")
expresion = st.text_input("Ingrese f(x) usando 'x' como variable:", value="x**3 - x - 2")

col1, col2 = st.columns(2)
with col1:
    a = st.number_input("Valor inicial 'a' (límite inferior):", value=1.0)
with col2:
    b = st.number_input("Valor inicial 'b' (límite superior):", value=2.0)

col3, col4 = st.columns(2)
with col3:
    max_iter = st.number_input(
        "Número máximo de iteraciones:", min_value=1, value=50, step=1
    )
with col4:
    error_relativo = st.number_input(
        "Error relativo (tolerancia, ej. 0.0001):",
        value=0.0001,
        format="%.6f",
    )

if st.button("Calcular Raíz"):
    if a >= b:
        st.error("Error: 'a' debe ser menor que 'b'.")
    else:
        try:
            raiz, iteraciones, error_final, tabla = biseccion(
                expresion, a, b, int(max_iter), error_relativo
            )

            st.success("¡Cálculo realizado con éxito!")

            # Mostrar tabla de resultados
            df = pd.DataFrame(
                tabla, columns=["Iteración", "xn (raíz aprox.)", "f(xn)", "Error (%)"]
            )
            st.subheader("Tabla de Iteraciones")
            st.dataframe(df, use_container_width=True)

            # Mostrar resultados finales
            st.subheader("Resultados Finales")
            st.write(f"**Raíz aproximada encontrada:** `{raiz:.7f}`")
            st.write(f"**Número total de iteraciones:** `{iteraciones}`")
            if not math.isnan(error_final):
                st.write(f"**Error final obtenido:** `{error_final:.7f} %`")
            else:
                st.write(
                    "**Error final obtenido:** No calculable (una sola iteración)"
                )

        except ValueError as e:
            st.error(f"Error en los datos: {e}")
        except Exception as e:
            st.error(f"Ocurrió un error al evaluar la función: {e}")
