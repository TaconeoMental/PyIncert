import math

from .core import V
from .util import exportador

# Declaramos un exportador. Creamos __all__ y el decorador para exportar.
exportar, __all__ = exportador()

# Faltan muchas funciones importantes, pero implementaré estas por ahra porque
# me da lata andar derivando cosas a esta hora.

# Ojo que estas funciones están hechas para funcionar solamente con objetos V,
# por lo que lo ideal es que se importe con un alias si se va a usar en
# conjunto con la librería math de la slib de Python. Por ejemplo:
#
# from pyincert import V, er
# import pyincert.math as imath
# import math
#
# a = math.sin(math.pi/2)
# b = imath.sin(V(math.pi, 1%er))
#
# Aunque también podrían usarla de la siguiente forma, aunque la encuentro muy
# engorrosa:
#
# import pyincert
# a = pyincert.math.sin(pyincert.V(3, pyincert.ER(4)))

# Notar que si tengo una función "f" de una única variable x, podemos propagar
# su error como: δf = abs(df/dx)δx

@exportar
def sin(v_rad):
    """Función seno para un objeto V"""

    # (d/dx)sin(x) = cos(x)
    return V(math.sin(v_rad.valor), abs(math.cos(v_rad.valor)) * v_rad.error)

@exportar
def cos(v_rad):
    """Función coseno para un objeto V"""

    # (d/dx)cos(x) = -sin(x)
    return V(math.cos(v_rad.valor), abs(math.sin(v_rad.valor)) * v_rad.error)

@exportar
def tan(v_rad):
    """Función tangente para objetos V"""
    # Podría perfectamente hacer sin(v_rad) / cos(v_rad), pero es mi librería y
    # chao haters B)

    # (d/dx)tan(x) = sec(x)^2 = cos(x)^-2
    return V(math.tan(v_rad.valor), pow(math.cos(v_rad.valor), -2) * v_rad.error)

@exportar
def degrees(v_rad):
    return v_rad * 180 / math.pi

@exportar
def radians(v_deg):
    return v_deg * math.pi / 180

