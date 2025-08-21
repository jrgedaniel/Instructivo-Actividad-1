
from __future__ import annotations

def busqueda_lineal(lista, x):
   
    for i, valor in enumerate(lista):
        if valor == x:
            return i
    return -1

def busqueda_binaria(lista, x):
   
    inicio, fin = 0, len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio] == x:
            return medio
        if lista[medio] < x:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1
