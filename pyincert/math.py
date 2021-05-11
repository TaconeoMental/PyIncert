import math

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
# a = pyincert.math.sin(pyincert.V(3, pyincert.ER(4))


def sin(v_rad):
    raise NotImplementedError

def cos(v_rad):
    raise NotImplementedError

def tan(v_rad):
    raise NotImplementedError

def degrees(v_rad):
    return v_rad * 180 / math.pi

def radians(v_deg):
    raise v_deg * math.pi / 180

