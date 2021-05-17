"""Funciones comunes"""

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
