# interfaz/estadisticas_frame.py

import tkinter as tk
from tkinter import ttk

class FrameEstadisticas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.lista_empresas = master.lista_empresas
        self._crear_componentes()

    def _crear_componentes(self):
        tk.Label(self, text="Estadísticas", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Empresa:").pack()
        self.combo_empresa = ttk.Combobox(self, state="readonly")
        self.combo_empresa.pack()
        self.combo_empresa.bind("<<ComboboxSelected>>", self.cargar_puntos)

        tk.Label(self, text="Punto de atención:").pack()
        self.combo_punto = ttk.Combobox(self, state="readonly")
        self.combo_punto.pack()
        self.combo_punto.bind("<<ComboboxSelected>>", self.mostrar_estadisticas)

        self.texto = tk.Text(self, width=90, height=20)
        self.texto.pack(pady=10)

        self.cargar_empresas()
        btn_reporte = tk.Button(self, text="Generar Reporte HTML", command=self.generar_html)
        btn_reporte.pack(pady=5)

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

    def mostrar_estadisticas(self, event=None):
        self.texto.delete(1.0, tk.END)
        punto = self.puntos_dict.get(self.combo_punto.get())
        if not punto:
            return

        datos = punto.estadisticas()
        self.texto.insert(tk.END, f"Punto: {punto.nombre}\n")
        self.texto.insert(tk.END, f"Clientes atendidos: {datos['clientes_atendidos']}\n\n")

        self.texto.insert(tk.END, "Tiempo de Espera:\n")
        self.texto.insert(tk.END, f"  Promedio: {round(datos['espera']['promedio'], 2)} min\n")
        self.texto.insert(tk.END, f"  Máximo:   {datos['espera']['max']} min\n")
        self.texto.insert(tk.END, f"  Mínimo:   {datos['espera']['min']} min\n\n")

        self.texto.insert(tk.END, "Tiempo de Atención:\n")
        self.texto.insert(tk.END, f"  Promedio: {round(datos['atencion']['promedio'], 2)} min\n")
        self.texto.insert(tk.END, f"  Máximo:   {datos['atencion']['max']} min\n")
        self.texto.insert(tk.END, f"  Mínimo:   {datos['atencion']['min']} min\n\n")

        self.texto.insert(tk.END, "Escritorios:\n")
        for esc in punto.escritorios.recorrer_adelante():
            if esc.clientes_atendidos == 0:
                continue
            self.texto.insert(tk.END, f"  {esc.identificacion} - {esc.encargado}\n")
            self.texto.insert(tk.END, f"    Atendidos: {esc.clientes_atendidos}\n")
            self.texto.insert(tk.END, f"    Promedio: {round(esc.promedio_atencion(), 2)} min\n")
            self.texto.insert(tk.END, f"    Máximo:   {esc.max_tiempo} min\n")
            self.texto.insert(tk.END, f"    Mínimo:   {esc.min_tiempo} min\n\n")
    def generar_html(self):
        from reportes.reportes_html import ReporteHTML
        punto = self.puntos_dict.get(self.combo_punto.get())
        if punto:
            ReporteHTML.generar_reporte_punto(punto)
            self.label_reporte = tk.Label(self, text="Reporte generado en 'reportes/reporte_atencion.html'", fg="green")
            self.label_reporte.pack()
