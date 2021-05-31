import math
import sys

# __all__ = ["V", "ER", "er"]

from .util import lambdify, jacobiana

# =========== Fin de los imports ==========

# Devuelve true si obj es un int o un float, false en caso contrario
def es_numero(obj):
    return isinstance(obj, (int, float)) and not isinstance(obj, bool)

def crear_binop(func):
    dx, dy = jacobiana(func)

    def operar(self, otro):
        if es_numero(otro):
            return operar(self,  V(otro))

        dx_eval = dx(self.valor, otro.valor)
        dy_eval = dy(self.valor, otro.valor)

        res = func(self.valor, otro.valor)

        incert = math.sqrt(pow(dx_eval * self.desv_est, 2) + pow(dy_eval * otro.desv_est, 2))

        obj = V(res, incert)
        obj.comb_lineal = self.comb_lineal
        obj.add_comb_lin((self, dx_eval))
        obj.add_comb_lin((otro, dy_eval))
        return obj
    return operar

def agregar_dunders_a_V():
    ops_ref = {
        "add": lambda x, y: x + y,
        "sub": lambda x, y: x - y,
        "mul": lambda x, y: x * y,
        "truediv": lambda x, y: x / y,
    }

    for nombre, operacion in ops_ref.items():
        setattr(V, f"__{nombre}__", crear_binop(operacion))

class ER:
    """
    Clase creada para representar un error relativo
    """
    def __init__(self, valor=0):
        if not es_numero(valor):
            raise TypeError("Eso no es un número a :(")
        self.valor = valor / 100

    def __rmod__(self, porcentaje):
        self.__init__(porcentaje)
        return self

# Instancia defecto de la clase. Esto nos permitirá usarla casi como un
# operador.
# Ejemplo:
# Podemos escribir un valor de 12.5 ± 0.1% de 3 formas:
# 1) Manualmente: V(12.5, 12.5 * (0.1 / 100))
# 2) Con una instancia de la clase: V(12.5, ER(0.1))
# 3) Con el pseudo operador de porcentaje: V(12.5, 0.1%er)
er = ER()

# Clase principal
class V:
    """
    Una clase que representa un valor junto con su error correspondiente.
    """

    # Este valor afecta únicamente la representación de la clase en __repr__.
    # Internamente sigue siendo la misma cantidad. Para modificar este valor es
    # necesario usar el método V.cantdec.
    cant_decimales = 15

    # Este es el separador que se usará en el método __repr__. Puede ser
    # cambiada por "+/-" con el método de clase V.unicode(false) por si la
    # consola no soporta unicode.
    pm = "±"

    def __init__(self, valor, desv_est = 0):
        """
        Inicializa la clase y arroja un error si alguno de los parámetros
        (valor o error) no es un número.
        """

        if not es_numero(valor) or not (es_numero(desv_est) or
                                        isinstance(desv_est, ER)):
            raise TypeError("Eso no es un número a :(")
        self.valor = float(valor)

        if isinstance(desv_est, ER):
            desv_est = self.valor * desv_est.valor
        self.desv_est = desv_est

        self.comb_lineal = {}


    @classmethod
    def cant_dec(cls, num):
        if num < 0:
            return
        cls.cant_decimales = num

    @classmethod
    def use_unicode(cls, b):
        if b:
            cls.pm = "±"
        else:
            cls.pm = "+/-"

    def add_comb_lin(self, elem):
        self.comb_lineal[elem[0]] = elem[1]

    def __repr__(self):
        """Representación bonita :)"""
        return f"{round(self.valor, self.cant_decimales)} {V.pm} {round(self.desv_est, self.cant_decimales)}"

agregar_dunders_a_V()
