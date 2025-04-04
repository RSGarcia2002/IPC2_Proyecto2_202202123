import tkinter as tk
from tkinter import ttk, messagebox

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

        btn_actualizar = tk.Button(self, text="Actualizar Estadísticas", command=self.mostrar_estadisticas)
        btn_actualizar.pack(pady=5)

        # 🎯 SCROLLABLE FRAME PARA ESTADÍSTICAS
        frame_scroll = tk.Frame(self)
        frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(frame_scroll, height=300)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.texto = tk.Text(self.scrollable_frame, width=90, height=20)
        self.texto.pack()

        btn_reporte = tk.Button(self, text="Generar Reporte HTML", command=self.generar_html)
        btn_reporte.pack(pady=5)

        self.label_reporte = tk.Label(self, text="", fg="green")
        self.label_reporte.pack()

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

    def mostrar_estadisticas(self, event=None):
        self.texto.delete(1.0, tk.END)
        punto = self.puntos_dict.get(self.combo_punto.get())
        if not punto:
            return

        datos = punto.estadisticas()

        self.texto.insert(tk.END, f"Punto: {punto.nombre}\n")
        self.texto.insert(tk.END, f"Clientes atendidos: {datos['clientes_atendidos']}\n\n")

        self.texto.insert(tk.END, "Tiempo de Espera:\n")
        self.texto.insert(tk.END, f"  ▪ Promedio: {datos['espera']['promedio']} min\n")
        self.texto.insert(tk.END, f"  ▪ Máximo:   {datos['espera']['max']} min\n")
        self.texto.insert(tk.END, f"  ▪ Mínimo:   {datos['espera']['min']} min\n\n")

        self.texto.insert(tk.END, "Tiempo de Atención:\n")
        self.texto.insert(tk.END, f"  ▪ Promedio: {datos['atencion']['promedio']} min\n")
        self.texto.insert(tk.END, f"  ▪ Máximo:   {datos['atencion']['max']} min\n")
        self.texto.insert(tk.END, f"  ▪ Mínimo:   {datos['atencion']['min']} min\n\n")

        self.texto.insert(tk.END, "Escritorios:\n")
        for esc in punto.escritorios.recorrer_adelante():
            if esc.clientes_atendidos == 0:
                continue
            self.texto.insert(tk.END, f"  🖥️ {esc.identificacion} - {esc.encargado}\n")
            self.texto.insert(tk.END, f"     Atendidos: {esc.clientes_atendidos}\n")
            self.texto.insert(tk.END, f"     ▪ Promedio: {round(esc.promedio_atencion(), 2)} min\n")
            self.texto.insert(tk.END, f"     ▪ Máximo:   {esc.max_tiempo} min\n")
            self.texto.insert(tk.END, f"     ▪ Mínimo:   {esc.min_tiempo} min\n\n")

    def generar_html(self):
        from reportes.reportes_html import ReporteHTML
        punto = self.puntos_dict.get(self.combo_punto.get())
        if punto:
            ReporteHTML.generar_reporte_punto(punto)
            self.label_reporte.config(text="Reporte generado en 'reportes/reporte_atencion.html'")
