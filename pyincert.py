import math

# Esta "librería" basicamente les permite trabajar y operar valores junto con sus
# errores correspondientes. Pongo librería entre comillas porque no está
# realmente creada para ser usada dentro de otro programa (aunque se puede, por
# qué no), sino más bien para ser importada dentro del REPL en la línea de
# comandos y ser usada para hacer los cálculos ahí mismo. Por ejemplo:
#
# >>> from pyincert import V
# >>> 3 - (V(12.7, 2e-5) ** 3) / 2
# (Valor: -1021.1914999999999, Error: 2e-05)

# Devuelve true si obj es un int o un float, false en caso contrario
def es_numero(obj):
    return isinstance(obj, (int, float)) and not isinstance(obj, bool)

class P:
    """
    Clase creada para representar un porcentaje.
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
# Podemos escribir un valor de 12.5 +- 0.1% de 3 formas:
# 1) Manualmente: V(12.5, 12.5 * (0.1 / 100))
# 2) Con una instancia de la clase: V(12.5, P(0.1))
# 3) Con el pseudo operador de porcentaje: V(12.5, 0.1%pc)
pc = P()

# Clase principal
class V:
    """
    Una clase que representa un valor junto con su error correspondiente.
    """

    # Este valor afecta únicamente la representación de la clase en __repr__.
    # Internamente sigue siendo la misma cantidad. Para modificar este valor es
    # necesario usar el método V.cantdec.
    cant_decimales = 4

    def __init__(self, valor, error = 0):
        """
        Inicializa la clase y arroja un error si alguno de los parámetros
        (valor o error) no es un número.
        """

        if not es_numero(valor) or not (es_numero(error) or isinstance(error, P)):
            raise TypeError("Eso no es un número a :(")
        self.valor = valor
        self.error = self.valor * error.valor if isinstance(error, P) else error

    @classmethod
    def cantdec(cls, num):
        if num < 0:
            return
        cls.cant_decimales = num

    def __repr__(self):
        """Representación bonita :)"""
        return f"(Valor: {round(self.valor, self.cant_decimales)}, Error: {round(self.error, self.cant_decimales)})"

    def __add__(self, otro):
        """
        Devuelve un objeto V correspondiente a la suma del objeto actual y otro
        objeto V o un número.

        Ejemplos:
        >>> V(3, 0.01) + 2 + 3 + V(8)
        """

        if es_numero(otro): return V(self.valor + otro, self.error)
        return V(self.valor + otro.valor, math.sqrt(self.error ** 2 + otro.error ** 2))

    def __radd__(self, otro):
        """
        Devuelve un objeto V correspondiente a la suma entre un número y el
        objeto actual.

        Ejemplo:
        >>> 4 + V(3, 1e-2)
        """

        return self + otro

    def __sub__(self, otro):
        """
        Devuelve un objeto V correspondiente a la resta entre el objeto actual
        y el argumento.

        Ejemplo:
        >>> V(3, 1e-5) - 8
        """

        if es_numero(otro): return V(self.valor - otro, self.error)
        return V(self.valor - otro.valor, math.sqrt(self.error ** 2 + otro.error ** 2))

    def __rsub__(self, otro):
        """
        Devuelve un objeto V correspondiente a la operación de un número menos
        el objeto actual.

        Ejemplo:
        >>> 12.8 - V(4, 9)
        """

        return V(otro) - self

    def __mul__(self, otro):
        """
        Devuelve un objeto V correspondiente a la multiplicación del objeto
        actual con otro objeto V o un número.

        Ejemplo:
        >>> V(2, 1e-4) * 3 * V(4)
        """

        if es_numero(otro): return V(self.valor * otro, self.error * otro)
        m = self.valor * otro.valor
        return V(m, m * math.sqrt((self.error / self.valor) ** 2 + (otro.error / otro.valor) ** 2))

    def __rmul__(self, otro):
        """
        Devuelve un objeto V correspondiente a la multiplicación entre un
        número y el objeto actual.

        Ejemplo:
        >>> 2.5 * V(7.99993, 3e-89)
        """

        return self * otro

    def __truediv__(self, otro):
        """
        Devuelve un objeto V correspondiente a la división del objeto actual
        con otro objeto V o un número.

        Ejemplo:
        >>> V(421, 68) / 3 / V(6, 2)
        """

        if es_numero(otro): return V(self.valor / otro, self.error / otro)
        d = self.valor / otro.valor
        return V(d, d * math.sqrt((self.error / self.valor) ** 2 + (otro.error / otro.valor) ** 2))

    def __rtruediv__(self, otro):
        """
        Devuelve un objeto V correspondiente a la división de un número con el
        objeto actual.

        Ejemplo:
        >>> 6 / V(8, 9.7776)
        """

        return V(otro) / self

    def __pow__(self, exponente):
        """
        Devuelve un objeto V correspondiente al objeto actual elevado a otro
        objeto V o un número.

        Ejemplo:
        >>> V(7, 9.886) ** 2 ** V(7)
        """

        return V(self.valor ** exponente, exponente * (self.valor ** (exponente - 1)) * self.error)

