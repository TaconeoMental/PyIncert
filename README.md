# <img width="30px" src="https://raw.githubusercontent.com/TaconeoMental/PyIncert/main/assets/logo.png"> PyIncert
Pequeña librería para trabajar con propagación de errores.

## Instalación
PyIncert se puede instalar directamente desde PyPI usando pip:
```
python3 -m pip install pyincert
```

## Uso
En PyIncert se trabaja con los objetos __V__ que representan una tupla de un valor y su error. Los cálculos matemáticos se harán con estos objetos mayoritariamente en reemplazo de las clases numéricas primitivas de Python (int y float). El formato para crear un objeto __V__ es simplemente ```V(Valor, Error)```. Las operaciones disponibles actualmente son: adición, sustracción, multiplicación, divisón, y potenciación. Todas estas se realizan con los operadores nativos de Python correspondientes a cada operación.
```python
from pyincert import V

voltaje = V(12, 1.3) # 12V ± 1.3
resistencia = V(4.3e3, 16) # 4.3e3Ω ± 16

# Operamos normalmente
corriente = voltaje / resistencia
print(corriente) # 0.0028 ± 0.0003

# Otro ejemplo
potencia = V(10e3, 24) * V(2.8e-3, 3e-4) ** 2
print(potencia) # 0.0784 ± 0.0168
```
En caso de operar con un valor sin error asociado, se puede omitir el uso del objeto __V__ y trabajar directamente con el literal, es decir:
```python
V(3, 0) * V(12, 0.1) == V(3) * V(12, 0.1) == 3 * V(12, 0.1) == V(12, 0.1) * 3
```

Nótese que PyIncert toma en cuenta la correlación entre variables al momento de
calcular.
```python
from pyincert import V

x = V(3.14, 1) # 3.14 ± 1
y = V(3.14, 1)

print(x / x) # 1.0 ± 0.0
print(x / y) # 1.0 ± 0.4504

print(x * x) # 9.8596 ± 6.28
print(x * y) # 9.8596 ± 4.4406
```

### Errores Relativos
PyIncert también incluye la clase __ER__ que representa un error relativo. Con este objeto podemos trabajar con valores del tipo ```V ± E%```. Esta puede ser usada creando una instancia de la misma u operando el valor de error con una instancia ya creada usando el operador módulo (%). Para esta última opción, PyIncert ya incluye una instancia de __ER__ llamada __er__.
```python
from pyincert import V, ER, er

r1 = V(3.3e4, ER(5)) # 3.3e4 ± 5%

# De forma equivalente (y preferible)
r2 = V(3.3e4, 5%er)
print(r2) # 33000.0 ± 1650.0

# Algunas personas me han comentado que han hecho esto:
_ = er # Así queda más limpio visualmente el error relativo
r3 = V(3.3e4, 5%_)
```

### Funciones Matemáticas
PyIncert incluye un pequeño sub-módulo con algunas funciones matemáticas hechas
para trabajar con objetos __V__. Estas devuelven un nuevo objeto __V__ con el
valor evaluado y el error propagado por la función.
```python
from pyincert import V
from pyincert.math import sin, radians

theta = V(180, 1) # 180° ± 1
theta_rad = radians(theta)

print(sin(theta_rad)) # 0.0 ± 0.0175
```

### Representación
La representación de un objeto V es ```Valor ± Error``` y por defecto redondea ambos valores a los primeros 4 decimales. Esto es meramente por temas estéticos, pues la aproximación no se usa al calcular. De todas formas, es posible cambiar la cantidad de decimales mostrados usando el método de clase _cant_dec_ de __V__. En caso de que la consola no soporte Unicode se puede llamar al método de clase _use_unicode_ con el argumento _False_ para que la representación sea ```Valor +/- Error```.
```python
from pyincert import V, er
import math

a = V(math.pi, 23%er) # π ± 23%
print(a) # 3.1416 ± 0.7226

V.cant_dec(10) # Ahora la representación redondea los valores a los primeros 10 decimales
V.use_unicode(False) # Ahora se usará "+/-" en vez de "±"

print(a) # 3.1415926536 +/- 0.7225663103
```

## Licencia
La librería PyIncert se encuentra publicada bajo la licencia GPLv3.
Para más información, favor referirse al archivo de [Licencia](https://github.com/TaconeoMental/PyIncert/blob/main/LICENSE)

Copyleft (C) 2021 Mateo Contenla
