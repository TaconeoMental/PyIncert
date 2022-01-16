"""Funciones comunes"""

import functools
import math
import sys

# Aquí definimos la función que calcula derivadas parciales. Primero creamos
# una implementación que usa diferenciación numérica, en específico una
# aproximación con diferencias finitas centrales.
# (https://en.wikipedia.org/wiki/Numerical_differentiation
# Ese no es el caso óptimo eso sí. Después intentamos importar sympy. Si falla,
# dejamos la función implementada con diferencia fínita; si se importa
# correctamente redefinimos la función para calcula derivadas parciales
# (parcial) para que haga uso de computación simbólica. Esto es mejor porque en
# lugar de hacer una aproximación del tipo (f(x + eps) - f(x - eps))/2eps,
# directamente me devuelve la función correspondiente a la derivada.

# Los floats de python son de doble precisión, por lo que un buen candidato
# al valor del step_size (h) es el sqrt(epsilon de la máquina) * abs(x)
STEPSIZE = math.sqrt(sys.float_info.epsilon)

# Implementamos la diferencia central manualmente
def parcial(func, par_index):
    """
    Devuelve una función correspondiente a la derivada parcial de func con
    respecto a sus parametros[par_index].

    func: una función con parámetros (x, y, ...).

    par_index: un entero correspondiente al índice de la variable en los
    parámetros de la función.
    """

    params = func.__code__.co_varnames

    if par_index < 0 or par_index > len(params) - 1:
        err_s = f"'{func.__name__}' does not have a parameter of index {par_index}"
        raise TypeError(err_s)

    var_name = params[par_index]

    @lambdify(params)
    def f_derivative(**valores):
        step = STEPSIZE * abs(valores[var_name])

        valores[var_name] += step
        f_mas_eps = func(**valores)

        valores[var_name] -= 2 * step
        f_menos_eps = func(**valores)

        return (f_mas_eps - f_menos_eps)/(2 * step)

    return f_derivative

try:
    import sympy
except ImportError:
    # sympy no está instalado
    # la función parcial queda como la implementación de diferencia central
    pass

else:
    # sympy está instalado
    parcial_diff = parcial

    # Esta implmentación siempre será la preferida, ya que computa la derivada
    # simbolicamente.
    def parcial(func, par_index):
        """
        Devuelve una función correspondiente a la derivada parcial de func con
        respecto a sus parametros[par_index].

        func: una función con parámetros (x, y, ...).

        par_index: un entero correspondiente al índice de la variable en los
        parámetros de la función.
        """
        params = func.__code__.co_varnames

        if par_index < 0 or par_index > len(params) - 1:
            err_s = f"'{func.__name__}' does not have a parameter of index {par_index}"
            raise TypeError(err_s)

        symbol_params = [sympy.Symbol(p) for p in params]

        try:
            symbol_func = func(*symbol_params)
            symbol_diff = sympy.diff(symbol_func, symbol_params[par_index])
            return sympy.lambdify(symbol_params, symbol_diff)
        except TypeError:
            # Si la derivada calculada simbólicamente falla (porque usa
            # funciones externas por ejemplo), simplemente la cálculamos con
            # aproimaciones de diferencias finitas.
            return parcial_diff(func, par_index)

class CombinacionLineal:
    def __init__(self, **kwargs):
        # V: K
        self.terms = {**kwargs}

    def calc():
        return sum([k * v for k, v in self.terms.items()])

# Se explica sola.
def gradiente(func):
    arity = func.__code__.co_argcount
    m_grad = list()

    for index in range(arity):
        m_grad.append(parcial(func, index))

    return m_grad


# Esta función me costó más de lo que me gutaría admitir.
# Voy a dar un ejemplo medio simple porque hice esta función para un tema super
# específico.
#
# Tengo una función de este estilo
# outer_f = lambda x, y: x * y
#
# Y otra de este estilo:
# def func(**kwargs):
#     return outer_f(**kwargs) * 2
#
# Yo quiero usar "func" como un wrapper para "outer_f", pero "func" no tiene
# idea de cuáles ni cuántos argumentos recibe "outer_f". Para solucionar eso,
# defino "func" así:
#
# @lambdify(outer_f.__code__.co_varnames)
# def func(**kwargs):
#     return outer_f(**kwargs)
#
# Ahora puedo llamar a "func" y esta se va a asegurar de que reciba la cantidad
# exacta de argumentos, incluso como keywords: func(x=9, y=8).
# Si la cantidad o los nombres de los argumentos están mal, se leventará un
# TypeError como cualquier función lo haría normalmente.
def lambdify(param_names):
    """
    Decorador para forzar que una función con parámetros *args, **kwargs o
    ambos, tenga una aridad de len(param_names).
    """

    def dec_lambdify(func):
        def wrapper_lambdify(*args, **kwargs):
            param_string = ", ".join(param_names)
            args_string = ", ".join([f"{x}={x}" for x in param_names])
            func_name = func.__name__
            f_string = f"lambda {param_string}: {func_name}({args_string})"
            f_lambda = eval(f_string, {func_name: func})

            if len(param_names) != len(args):
                raise TypeError(f"{func_name}() takes {len(param_names)} positional arguments but {len(args)} were given")

            arg_union = {**dict(zip(param_names, args)), **kwargs}

            return f_lambda(**arg_union)
        return wrapper_lambdify
    return dec_lambdify

def exportador():
    """
    Crea un arreglo __all__ y un decorador que añade las definiciones al
    arreglo.

    Para usarlo se importa esta función y se añaden estas líneas:

    exportar, __all__ = exportador()

    Así creamos el arreglo __all__ y el decorador "exportador".
    """

    all_ = list()
    def dec(obj):
        if obj.__name__ not in all_:
            all_.append(obj.__name__)
        return obj
    return dec, all_
