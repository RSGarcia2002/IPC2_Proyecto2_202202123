# visualizador_grafico.py

from graphviz import Digraph
import os

class VisualizadorGrafico:

    @staticmethod
    def graficar_cola(punto, nombre_archivo="cola_espera"):
        dot = Digraph(comment='Cola de Espera')
        dot.attr(rankdir='LR')

        clientes = punto.cola_espera.recorrer()

        for i, cliente in enumerate(clientes):
            etiqueta = f"{cliente.nombre}\nDPI: {cliente.dpi}"
            dot.node(str(i), etiqueta)

        for i in range(len(clientes) - 1):
            dot.edge(str(i), str(i + 1))

        ruta = f"reportes/{nombre_archivo}"
        dot.render(ruta, format='png', cleanup=True)
        print(f"Cola graficada en {ruta}.png")

    @staticmethod
    def graficar_escritorios(punto, nombre_archivo="escritorios"):
        dot = Digraph(comment='Escritorios')
        dot.attr(rankdir='LR')

        escritorios = punto.escritorios.recorrer_adelante()

        for i, esc in enumerate(escritorios):
            estado = "Activo" if esc.activo else "Inactivo"
            etiqueta = f"{esc.identificacion}\n{esc.encargado}\n{estado}"
            color = "green" if esc.activo else "red"
            dot.node(str(i), etiqueta, style="filled", fillcolor=color)

        for i in range(len(escritorios) - 1):
            dot.edge(str(i), str(i + 1))

        ruta = f"reportes/{nombre_archivo}"
        dot.render(ruta, format='png', cleanup=True)
        print(f"Escritorios graficados en {ruta}.png")
