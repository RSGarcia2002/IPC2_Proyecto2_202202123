# interfaz/solicitud_frame.py

import tkinter as tk
from tkinter import ttk, messagebox
from modelos.cliente import Cliente

class FrameSolicitud(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.lista_empresas = master.lista_empresas
        self.transacciones_seleccionadas = []
        self._crear_componentes()

    def _crear_componentes(self):
        tk.Label(self, text="Solicitud de Atención", font=("Arial", 16)).pack(pady=10)

        # Selección de empresa
        tk.Label(self, text="Empresa:").pack()
        self.combo_empresa = ttk.Combobox(self, state="readonly")
        self.combo_empresa.pack()
        self.combo_empresa.bind("<<ComboboxSelected>>", self.cargar_puntos)

        # Selección de punto
        tk.Label(self, text="Punto de atención:").pack()
        self.combo_punto = ttk.Combobox(self, state="readonly")
        self.combo_punto.pack()
        self.combo_punto.bind("<<ComboboxSelected>>", self.cargar_transacciones)

        # Área para ingresar DPI y nombre
        tk.Label(self, text="DPI del cliente:").pack()
        self.entry_dpi = tk.Entry(self)
        self.entry_dpi.pack()

        tk.Label(self, text="Nombre del cliente:").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        # Área para mostrar transacciones
        self.frame_transacciones = tk.Frame(self)
        self.frame_transacciones.pack(pady=10)

        # Botón para generar solicitud
        btn_enviar = tk.Button(self, text="Solicitar Atención", command=self.enviar_solicitud)
        btn_enviar.pack(pady=10)

        self.label_resultado = tk.Label(self, text="", font=("Arial", 12), fg="blue")
        self.label_resultado.pack()

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

    def cargar_transacciones(self, event=None):
        # Limpiar frame
        for widget in self.frame_transacciones.winfo_children():
            widget.destroy()

        nombre_empresa = self.combo_empresa.get()
        empresa = self.empresas_dict.get(nombre_empresa)
        if not empresa:
            return

        transacciones = empresa.transacciones.recorrer()
        self.transacciones_vars = []

        for t in transacciones:
            var = tk.IntVar()
            entry = tk.Entry(self.frame_transacciones, width=5)
            tk.Checkbutton(self.frame_transacciones, text=t.nombre, variable=var).pack(anchor="w")
            entry.pack(anchor="w", padx=30)
            self.transacciones_vars.append((t, var, entry))

    def enviar_solicitud(self):
        nombre = self.entry_nombre.get().strip()
        dpi = self.entry_dpi.get().strip()
        punto_nombre = self.combo_punto.get()
        punto = self.puntos_dict.get(punto_nombre)

        if not nombre or not dpi or not punto:
            messagebox.showerror("Error", "Completa todos los campos")
            return

        cliente = Cliente(dpi, nombre)
        total = 0

        for trans, var, entry in self.transacciones_vars:
            if var.get():
                try:
                    cantidad = int(entry.get())
                    cliente.agregar_transaccion(trans, cantidad)
                    total += trans.tiempo * cantidad
                except ValueError:
                    messagebox.showerror("Error", f"Cantidad inválida para '{trans.nombre}'")
                    return

        if total == 0:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos una transacción.")
            return

        cliente.tiempo_espera = punto.cola_espera.tamano() * total
        punto.agregar_cliente(cliente)

        self.label_resultado.config(
            text=f"Solicitud registrada\nTiempo estimado: {cliente.tiempo_espera} min"
        )
