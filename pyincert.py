import math

# Esta "librería" basicamente les permite trabajar y operar valores junto con sus
# errores correspondientes. Pongo librería entre comillas porque no está
# realmente creada para ser usada dentro de otro programa (aunque se puede, por
# qué no), sino más bien para ser importada dentro del REPL en la línea de
# comandos y ser usada para hacer los cálculos ahí mismo. Por ejemplo:
#
# >>> from valerror import V
# >>> 3 - (V(12.7, 2e-5) ** 3) / 2
# (Valor: -1021.1914999999999, Error: -2e-05)

def esNumero(obj):
    return isinstance(obj, (int, float)) and not isinstance(obj, bool)

class V:
    """
    Una clase que representa un valor junto con su error correspondiente.
    """

    def __init__(self, valor, error = 0):
        """
        Inicializa la clase y arroja un error si alguno de los parámetros
        (valor o error) no es un número.
        """

        if not esNumero(valor) or not esNumero(error):
            raise TypeError("Eso no es un número a :(")
        self.valor = valor
        self.error = error

    def __repr__(self):
        """Representación bonita :)"""
        return f"(Valor: {self.valor}, Error: {self.error})"

    def __add__(self, otro):
        """
        Devuelve un objeto V correspondiente a la suma del objeto actual y otro
        objeto V o un número.

        Ejemplos:
        >>> V(3, 0.01) + 2 + 3 + V(8)
        """

        if esNumero(otro): return V(self.valor + otro, self.error)
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

        if esNumero(otro): return V(self.valor - otro, self.error)
        return V(self.valor - otro.valor, math.sqrt(self.error ** 2 - otro.error ** 2))

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

        if esNumero(otro): return V(self.valor * otro, self.error * otro)
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

        if esNumero(otro): return V(self.valor / otro, self.error)
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

        if esNumero(exponente): return V(self.valor ** exponente, self.error)
        return V(self.valor ** exponente, exponente * self.valor ** (exponente - 1) * self.error)

    # No es necesario :)
    # def __rpow__(self, otro):
    #     return V(otro) ** self
