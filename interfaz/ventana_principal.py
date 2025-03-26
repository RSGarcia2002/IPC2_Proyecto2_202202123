# interfaz/ventana_principal.py

import tkinter as tk
from tkinter import ttk

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Atención al Cliente")
        self.geometry("800x500")
        self.resizable(False, False)

        self.frame_actual = None
        self._crear_menu()

        # Aquí podés cargar el primer frame por defecto si querés
        # self.mostrar_frame(FrameConfiguracion)

    def _crear_menu(self):
        barra = tk.Menu(self)

        menu_principal = tk.Menu(barra, tearoff=0)
        menu_principal.add_command(label="Configuración", command=lambda: self.cambiar_frame("configuracion"))
        menu_principal.add_command(label="Simulación", command=lambda: self.cambiar_frame("simulacion"))
        menu_principal.add_command(label="Solicitud", command=lambda: self.cambiar_frame("solicitud"))
        menu_principal.add_command(label="Estadísticas", command=lambda: self.cambiar_frame("estadisticas"))
        menu_principal.add_separator()
        menu_principal.add_command(label="Salir", command=self.quit)

        barra.add_cascade(label="Menú", menu=menu_principal)
        self.config(menu=barra)

    def cambiar_frame(self, tipo):
        if self.frame_actual:
            self.frame_actual.destroy()

        if tipo == "configuracion":
            from interfaz.configuracion_frame import FrameConfiguracion
            self.frame_actual = FrameConfiguracion(self)
        elif tipo == "simulacion":
            from interfaz.simulacion_frame import FrameSimulacion
            self.frame_actual = FrameSimulacion(self)
        elif tipo == "solicitud":
            from interfaz.solicitud_frame import FrameSolicitud
            self.frame_actual = FrameSolicitud(self)
        elif tipo == "estadisticas":
            from interfaz.estadisticas_frame import FrameEstadisticas
            self.frame_actual = FrameEstadisticas(self)

        self.frame_actual.pack(fill="both", expand=True)
