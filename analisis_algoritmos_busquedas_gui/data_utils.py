
from __future__ import annotations
import random
import time
from typing import Callable, Dict, List, Tuple

def generar_datos(tamano: int, seed: int | None = None) -> List[int]:
    
    if tamano <= 0:
        return []
    if seed is not None:
        random.seed(seed)
    
    lista = random.sample(range(tamano * 10), tamano)
    lista.sort()
    return lista

def medir_tiempo(algoritmo: Callable[[List[int], int], int],
                 lista: List[int], x: int, repeticiones: int = 5) -> float:
    
    if repeticiones <= 0:
        repeticiones = 1
    tiempos_ms: List[float] = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        algoritmo(lista, x)
        t1 = time.perf_counter()
        tiempos_ms.append((t1 - t0) * 1000.0)
    return sum(tiempos_ms) / len(tiempos_ms)

def benchmark(algoritmos: Dict[str, Callable[[List[int], int], int]],
              tamanos: List[int], repeticiones: int = 5, seed: int | None = None
              ) -> Tuple[List[int], Dict[str, List[float]]]:
   
    resultados: Dict[str, List[float]] = {nombre: [] for nombre in algoritmos.keys()}
    for n in tamanos:
        datos = generar_datos(n, seed=seed)
        if not datos:
            for nombre in algoritmos.keys():
                resultados[nombre].append(0.0)
            continue
        objetivo = datos[-1]  
        for nombre, func in algoritmos.items():
            promedio_ms = medir_tiempo(func, datos, objetivo, repeticiones=repeticiones)
            resultados[nombre].append(promedio_ms)
    return tamanos, resultados
