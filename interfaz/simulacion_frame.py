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

        # Botones para pila de escritorios
        btn_activar = tk.Button(self, text="Activar Escritorio", command=self.activar_escritorio)
        btn_activar.pack(pady=5)

        btn_desactivar = tk.Button(self, text="Desactivar Escritorio", command=self.desactivar_escritorio)
        btn_desactivar.pack(pady=5)

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

    def _get_empresa_actual(self):
        nombre = self.combo_empresa.get()
        return self.empresas_dict.get(nombre)

    def _get_punto_actual(self):
        nombre_punto = self.combo_punto.get()
        return self.puntos_dict.get(nombre_punto)

    def activar_escritorio(self):
        punto = self._get_punto_actual()
        if not punto:
            messagebox.showerror("Error", "Selecciona un punto de atención.")
            return

        escritorio = punto.obtener_siguiente_inactivo()
        if escritorio:
            escritorio.activar()
            self.label_estado.config(text=f"Escritorio {escritorio.identificacion} activado.")
        else:
            self.label_estado.config(text="No hay escritorios inactivos disponibles.")
        
        self.cargar_escritorios()


    def desactivar_escritorio(self):
        punto = self._get_punto_actual()
        if not punto:
            messagebox.showerror("Error", "Selecciona un punto de atención.")
            return

        pila = []
        for esc in punto.escritorios.recorrer_adelante():
            if esc.activo:
                pila.append(esc)

        if pila:
            ultimo = pila[-1]  # LIFO
            ultimo.desactivar()
            self.label_estado.config(text=f"Escritorio {ultimo.identificacion} desactivado.")
        else:
            self.label_estado.config(text="No hay escritorios activos para desactivar.")
        
        self.cargar_escritorios()

    def atender(self):
        punto = self._get_punto_actual()
        if not punto:
            return

        antes = punto.cola_espera.tamano()
        punto.atender()
        despues = punto.cola_espera.tamano()
        atendidos = antes - despues

        if atendidos > 0:
            self.label_estado.config(text=f"Se atendieron {atendidos} cliente(s).")
        else:
            self.label_estado.config(text="No hay clientes disponibles para atender.")

        self.cargar_escritorios()

    def simular(self):
        punto = self._get_punto_actual()
        if punto:
            ciclos = 0
            while not punto.cola_espera.esta_vacia():
                punto.atender()
                ciclos += 1

            # Asegurarnos de vaciar escritorios que aún tengan clientes
            for _ in range(10):
                punto.atender()

            self.label_estado.config(text=f"Simulación completa en {ciclos} ciclo(s).")
            self.cargar_escritorios()


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

    def cargar_escritorios(self):
        punto = self._get_punto_actual()
        if not punto:
            return

        print("Estado de los escritorios:")
        for esc in punto.escritorios.recorrer_adelante():
            estado = "Activo" if esc.activo else "Inactivo"
            print(f"  {esc.identificacion} - {estado}")

