# PyIncert
Pequeña librería para trabajar con propagación de errores.

## Motivación
Necesito pasar Métodos Experimentales, por favor, ayuda.

## Uso
En PyIncert se trabaja con los objetos __V__ que representan una tupla de un valor y su error. Los cálculos matemáticos se harán con estos objetos mayoritariamente en reemplazo de las clases numéricas primitivas de Python (int y float). El formato para crear un objeto __V__ es simplemente ```V(Valor, Error)```. Las operaciones disponibles actualmente son: adición, sustracción, multiplicación, divisón, y potenciación. Todas estas se realizan con los operadores nativos de Python correspondientes a cada operación.
```python
from pyincert import V

voltaje = V(12, 1.3) # 12V ± 1.3
resistencia = V(4.3e3, 16) # 4.3e3Ω ± 16

# Operamos normalmente
corriente = voltaje / resistencia
print(corriente) # (Valor: 0.0028, Error: 0.0003)

# Otro ejemplo
potencia = V(10e3, 24) * V(2.8e-3, 3e-4) ** 2
print(potencia) # (Valor: 0.0784, Error: 0.0168)
```
En caso de operar con un valor sin error asociado, se puede omitir el uso del objeto __V__ y trabajar directamente con el literal, es decir:
```python
V(3, 0) * V(12, 0.1) == V(3) * V(12, 0.1) == 3 * V(12, 0.1) == V(12, 0.1) * 3
```
PyIncert también incluye la clase __P__ que representa un porcentaje. Con este objeto podemos trabajar con valores del tipo ```V ± E%```. Esta puede ser usada creando una instancia de la misma u operando el valor de error con una instancia ya creada usando el operador módulo (%). Para esta última opción, PyIncert ya incluye una instancia de __P__ llamada __pc__.
```python
from pyincert import V, P, pc

r1 = V(3.3e4, P(5)) # 3.3e4 ± 5%

# De forma equivalente (y preferible)
r2 = V(3.3e4, 5%pc)
print(r2) # (Valor: 33000.0, Error: 1650.0)
```
La representación de un objeto V por defecto redondea ambos valores a los primeros 4 decimales. Esto es meramente por temas estéticos, pues la aproximación no se usa al calcular. De todas formas, es posible cambiar la cantidad de decimales mostrados usando el método de clase _cantdec_ de __V__.
```python
from pyincert import V, pc
import math

a = V(math.pi, 23%pc) # π ± 23%
print(a) # (Valor: 3.1416, Error: 0.7226)

V.cantdec(10)
print(a) # (Valor: 3.1415926536, Error: 0.7225663103)
```