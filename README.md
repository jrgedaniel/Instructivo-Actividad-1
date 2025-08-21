# Instructivo-Actividad-1

# Comparación de Búsqueda Lineal vs Binaria (GUI Tkinter + Matplotlib)

Proyecto para la materia **Análisis de Algoritmos**. Implementa:
- Generación de listas ordenadas de distintos tamaños.
- Búsqueda **lineal** y **binaria** con medición de tiempos (ms) usando `time.perf_counter()`.
- **Gráfica** integrada en la GUI con tiempos promedio para 4 tamaños (100, 1 000, 10 000, 100 000).
- ≥ 5 repeticiones por tamaño/algoritmo (configurable).

## Requisitos
- Python **3.10+**
- Windows incluye `tkinter` por defecto (en la mayoría de instalaciones).
- Librerías:
  - `matplotlib`
  - `numpy` (opcional; **no es estrictamente necesario** para correr este proyecto).

## Instalación (opcional, recomendado en Windows)
```bash
python -m venv .venv
.venv\Scripts\activate


pip install -r requirements.txt
```

## Ejecución
```bash
python main.py
```

## Archivos
- `main.py` → Punto de entrada. Crea la ventana y ejecuta la app.
- `ui.py` → Lógica de la interfaz con Tkinter + Matplotlib.
- `algorithms.py` → Implementación de búsqueda lineal y binaria.
- `data_utils.py` → Generación de datos, medición de tiempos y benchmarking.
- `requirements.txt` → Dependencias del proyecto.



