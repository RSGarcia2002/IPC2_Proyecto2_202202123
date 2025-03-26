# interfaz/simulacion_frame.py

import tkinter as tk
from tkinter import ttk, messagebox

class FrameSimulacion(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.lista_empresas = master.lista_empresas
        self._crear_componentes()

    def _crear_componentes(self):
        tk.Label(self, text="Simulación de Atención", font=("Arial", 16)).pack(pady=10)

        # Empresa y punto
        tk.Label(self, text="Empresa:").pack()
        self.combo_empresa = ttk.Combobox(self, state="readonly")
        self.combo_empresa.pack()
        self.combo_empresa.bind("<<ComboboxSelected>>", self.cargar_puntos)

        tk.Label(self, text="Punto de atención:").pack()
        self.combo_punto = ttk.Combobox(self, state="readonly")
        self.combo_punto.pack()
        self.combo_punto.bind("<<ComboboxSelected>>", self.cargar_escritorios)

        # Lista de escritorios
        self.frame_escritorios = tk.Frame(self)
        self.frame_escritorios.pack(pady=10)

        # Botones de acción
        btn_atender = tk.Button(self, text="Atender Siguiente Cliente(s)", command=self.atender)
        btn_atender.pack(pady=5)

        btn_simular = tk.Button(self, text="Simular Atención Completa", command=self.simular)
        btn_simular.pack(pady=5)

        btn_graf_espera = tk.Button(self, text="Graficar Cola de Espera", command=self.graficar_cola)
        btn_graf_espera.pack(pady=5)

        btn_graf_escritorios = tk.Button(self, text="Graficar Escritorios", command=self.graficar_escritorios)
        btn_graf_escritorios.pack(pady=5)

        self.label_estado = tk.Label(self, text="", font=("Arial", 12), fg="green")
        self.label_estado.pack()

        self.cargar_empresas()

    def cargar_empresas(self):
        empresas = self.lista_empresas.recorrer()
        self.combo_empresa["values"] = [e.nombre for e in empresas]
        self.empresas_dict = {e.nombre: e for e in empresas}

    def cargar_puntos(self, event=None):
        nombre_empresa = self.combo_empresa.get()
        empresa = self.empresas_dict.get(nombre_empresa)
        if empresa:
            puntos = empresa.puntos.recorrer()
            self.combo_punto["values"] = [p.nombre for p in puntos]
            self.puntos_dict = {p.nombre: p for p in puntos}
            self.combo_punto.set("")

    def cargar_escritorios(self, event=None):
        for widget in self.frame_escritorios.winfo_children():
            widget.destroy()

        punto = self._get_punto_actual()
        if not punto:
            return

        self.botones_escritorios = []

        for escritorio in punto.escritorios.recorrer_adelante():
            estado = "Activo" if escritorio.activo else "Inactivo"
            texto_btn = f"{escritorio.identificacion} ({estado})"

            boton = tk.Button(self.frame_escritorios, text=texto_btn, width=40)
            boton.config(command=lambda e=escritorio, b=boton: self.toggle_escritorio(e, b))
            boton.pack(pady=2)
            self.botones_escritorios.append(boton)

    def toggle_escritorio(self, escritorio, boton):
        if escritorio.activo:
            escritorio.desactivar()
        else:
            escritorio.activar()
        estado = "Activo" if escritorio.activo else "Inactivo"
        boton.config(text=f"{escritorio.identificacion} ({estado})")

    def atender(self):
        punto = self._get_punto_actual()
        if punto:
            punto.atender()
            self.label_estado.config(text="Atención ejecutada.")
            self.cargar_escritorios()

    def simular(self):
        punto = self._get_punto_actual()
        if punto:
            while punto.cola_espera.tamano() > 0:
                punto.atender()
            self.label_estado.config(text="Simulación completa.")
            self.cargar_escritorios()

    def _get_punto_actual(self):
        nombre_punto = self.combo_punto.get()
        return self.puntos_dict.get(nombre_punto)

    def graficar_cola(self):
        from visualizador_grafico import VisualizadorGrafico
        punto = self._get_punto_actual()
        if punto:
            VisualizadorGrafico.graficar_cola(punto)
            self.label_estado.config(text="Cola de espera graficada.")

    def graficar_escritorios(self):
        from visualizador_grafico import VisualizadorGrafico
        punto = self._get_punto_actual()
        if punto:
            VisualizadorGrafico.graficar_escritorios(punto)
            self.label_estado.config(text="Escritorios graficados.")
