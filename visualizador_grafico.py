from graphviz import Digraph
import os

class VisualizadorGrafico:
    @staticmethod
    def graficar_cola(punto):
        import graphviz

        if punto.cola_espera.esta_vacia():
            print("⚠️ La cola de espera está vacía.")
            return

        dot = graphviz.Digraph(format='png')
        dot.attr(rankdir='LR')

        index = 0
        actual = punto.cola_espera.frente

        while actual:
            cliente = actual.dato  # ✅ Cambiado de .valor a .dato
            label = f"{cliente.nombre}\nDPI: {cliente.dpi}"

            # Marcar verde si ya fue atendido
            atendido = any(c.dpi == cliente.dpi for c in punto.clientes_atendidos.recorrer())

            if atendido:
                dot.node(f"C{index}", label=label, style="filled", fillcolor="palegreen")
            else:
                dot.node(f"C{index}", label=label)

            if index > 0:
                dot.edge(f"C{index-1}", f"C{index}")
            index += 1
            actual = actual.siguiente

        os.makedirs("reportes", exist_ok=True)
        dot.render("reportes/cola_espera", view=True)
        print("✅ Cola de espera graficada correctamente.")

    @staticmethod
    def graficar_escritorios(punto, nombre_archivo="escritorios"):
        dot = Digraph(comment='Escritorios')
        dot.attr(rankdir='LR')

        escritorios = punto.escritorios.recorrer_adelante()

        for i, esc in enumerate(escritorios):
            estado = "Activo" if esc.activo else "Inactivo"
            etiqueta = f"{esc.identificacion}\n{esc.encargado}\n{estado}"
            color = "palegreen" if esc.activo else "lightcoral"
            dot.node(str(i), etiqueta, style="filled", fillcolor=color)

        for i in range(len(escritorios) - 1):
            dot.edge(str(i), str(i + 1))

        os.makedirs("reportes", exist_ok=True)
        ruta = f"reportes/{nombre_archivo}"
        dot.render(ruta, format='png', cleanup=True)
        print(f"✅ Escritorios graficados en {ruta}.png")
