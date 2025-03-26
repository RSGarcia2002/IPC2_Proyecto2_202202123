# interfaz/configuracion_frame.py

import tkinter as tk
from tkinter import filedialog, messagebox
from lector_xml import LectorXML
from estructuras.lista_simple import ListaSimple

class FrameConfiguracion(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.lista_empresas = master.lista_empresas if hasattr(master, 'lista_empresas') else ListaSimple()
        master.lista_empresas = self.lista_empresas

        self._crear_componentes()

    def _crear_componentes(self):
        tk.Label(self, text="Configuración del Sistema", font=("Arial", 16)).pack(pady=10)

        btn_config = tk.Button(self, text="Cargar archivo de configuración (.xml)", width=40, command=self.cargar_config)
        btn_config.pack(pady=10)

        btn_inicial = tk.Button(self, text="Cargar archivo de inicio (.xml)", width=40, command=self.cargar_inicial)
        btn_inicial.pack(pady=10)

        self.label_estado = tk.Label(self, text="", fg="green", font=("Arial", 12))
        self.label_estado.pack(pady=15)

    def cargar_config(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if ruta:
            LectorXML.cargar_configuracion(ruta, self.lista_empresas)
            self.label_estado.config(text="Configuración cargada correctamente.")
            messagebox.showinfo("Éxito", "Archivo de configuración cargado correctamente.")

    def cargar_inicial(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if ruta:
            LectorXML.cargar_inicial(ruta, self.lista_empresas)
            self.label_estado.config(text="Archivo de inicio cargado correctamente.")
            messagebox.showinfo("Éxito", "Archivo de inicio cargado correctamente.")
