
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithms import busqueda_lineal, busqueda_binaria
from data_utils import generar_datos, medir_tiempo, benchmark

TAMANOS_PREDET = [100, 1000, 10_000, 100_000]

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Comparación: Búsqueda Lineal vs Binaria")
        self.root.geometry("900x650")

        
        self.lista = []
        self.tamano_actual = tk.IntVar(value=TAMANOS_PREDET[0])
        self.repeticiones = tk.IntVar(value=5)

       
        cont = ttk.Frame(root, padding=12)
        cont.pack(fill=tk.BOTH, expand=True)

       
        left = ttk.Frame(cont)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        ttk.Label(left, text="Tamaño de la lista:").pack(anchor=tk.W)
        self.combo_tamano = ttk.Combobox(left, values=[str(x) for x in TAMANOS_PREDET],
                                         textvariable=self.tamano_actual, state="readonly", width=12)
        self.combo_tamano.pack(anchor=tk.W, pady=(0, 6))

        self.btn_generar = ttk.Button(left, text="Generar datos", command=self.generar_datos)
        self.btn_generar.pack(anchor=tk.W, pady=(0, 10))

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        ttk.Label(left, text="Valor a buscar (entero):").pack(anchor=tk.W)
        self.entry_valor = ttk.Entry(left, width=18)
        self.entry_valor.pack(anchor=tk.W, pady=(0, 6))

        self.btn_lineal = ttk.Button(left, text="Búsqueda lineal", command=self.buscar_lineal, state=tk.DISABLED)
        self.btn_lineal.pack(anchor=tk.W, pady=(0, 4))

        self.btn_binaria = ttk.Button(left, text="Búsqueda binaria", command=self.buscar_binaria, state=tk.DISABLED)
        self.btn_binaria.pack(anchor=tk.W, pady=(0, 10))

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        ttk.Label(left, text="Repeticiones (≥5):").pack(anchor=tk.W)
        self.entry_reps = ttk.Entry(left, width=8, textvariable=self.repeticiones)
        self.entry_reps.pack(anchor=tk.W, pady=(0, 6))

        self.btn_comparar = ttk.Button(left, text="Comparar algoritmos", command=self.comparar)
        self.btn_comparar.pack(anchor=tk.W, pady=(6, 10))

       
        right = ttk.Frame(cont)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_info = ttk.Label(right, text="Lista no generada", foreground="#1f4e79")
        self.lbl_info.pack(anchor=tk.W, pady=(0, 6))

        self.lbl_result = ttk.Label(right, text="Resultados de búsqueda aparecerán aquí.")
        self.lbl_result.pack(anchor=tk.W, pady=(0, 10))

        
        self.fig = plt.Figure(figsize=(6.5, 4.2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Promedio de tiempos (ms)")
        self.ax.set_xlabel("Tamaño de la lista")
        self.ax.set_ylabel("Tiempo (ms)")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    
    def generar_datos(self):
        try:
            n = int(self.tamano_actual.get())
            if n not in (100, 1000, 10_000, 100_000):
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Seleccione un tamaño válido: 100, 1000, 10 000 o 100 000.")
            return

        self.lista = generar_datos(n)
        self.lbl_info.config(text=f"Lista generada: tamaño {n}")
      
        self.btn_lineal.config(state=tk.NORMAL)
        self.btn_binaria.config(state=tk.NORMAL)

    def _leer_valor(self) -> int | None:
        try:
            return int(self.entry_valor.get().strip())
        except Exception:
            messagebox.showerror("Error", "Ingrese un entero válido en 'Valor a buscar'.")
            return None

    def _mostrar_resultado(self, nombre: str, indice: int, tiempo_ms: float):
        n = len(self.lista)
        if indice == -1:
            texto = f"{nombre} | Tamaño={n} | Resultado: no encontrado | Tiempo: {tiempo_ms:.5f} ms"
        else:
            texto = f"{nombre} | Tamaño={n} | Índice: {indice} | Tiempo: {tiempo_ms:.5f} ms"
        self.lbl_result.config(text=texto)

    def buscar_lineal(self):
        if not self.lista:
            messagebox.showwarning("Aviso", "Primero genera la lista.")
            return
        x = self._leer_valor()
        if x is None:
            return
        tiempo_ms = medir_tiempo(busqueda_lineal, self.lista, x, repeticiones=5)
        indice = busqueda_lineal(self.lista, x)
        self._mostrar_resultado("Búsqueda lineal", indice, tiempo_ms)

    def buscar_binaria(self):
        if not self.lista:
            messagebox.showwarning("Aviso", "Primero genera la lista.")
            return
        x = self._leer_valor()
        if x is None:
            return
        
        self.lista.sort()
        tiempo_ms = medir_tiempo(busqueda_binaria, self.lista, x, repeticiones=5)
        indice = busqueda_binaria(self.lista, x)
        self._mostrar_resultado("Búsqueda binaria", indice, tiempo_ms)

    def comparar(self):
        
        try:
            reps = int(self.entry_reps.get().strip())
            if reps < 5:
                raise ValueError
        except Exception:
            messagebox.showerror("Error", "Las repeticiones deben ser un entero ≥ 5.")
            return

        algoritmos = {
            "Lineal": busqueda_lineal,
            "Binaria": busqueda_binaria,
        }
        tamanos, resultados = benchmark(algoritmos, TAMANOS_PREDET, repeticiones=reps)

       
        self.ax.clear()
        self.ax.set_title("Promedio de tiempos (ms)")
        self.ax.set_xlabel("Tamaño de la lista")
        self.ax.set_ylabel("Tiempo (ms)")
        self.ax.grid(True)

       
        self.ax.plot(tamanos, resultados["Lineal"], marker='o', label="Lineal")
        self.ax.plot(tamanos, resultados["Binaria"], marker='o', label="Binaria")
        self.ax.set_xscale('log')
        self.ax.legend()
        self.canvas.draw()
