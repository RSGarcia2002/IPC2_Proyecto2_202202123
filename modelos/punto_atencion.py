from estructuras.lista_doble import ListaDoble
from estructuras.cola import Cola
from estructuras.lista_simple import ListaSimple

class PuntoAtencion:
    def __init__(self, id_punto, nombre, direccion):
        self.id = id_punto
        self.nombre = nombre
        self.direccion = direccion

        self.escritorios = ListaDoble()
        self.cola_espera = Cola()
        self.clientes_atendidos = ListaSimple()

    def agregar_escritorio(self, escritorio):
        self.escritorios.agregar_final(escritorio)

    def agregar_cliente(self, cliente):
        self.cola_espera.encolar(cliente)

    def agregar_cliente_prioridad(self, cliente):
        self.cola_espera.encolar_prioridad(cliente)

    def atender(self):
        atendidos = []
        for escritorio in self.escritorios.recorrer_adelante():
            if not escritorio.activo:
                continue

            if escritorio.cliente_actual is None and not self.cola_espera.esta_vacia():
                cliente = self.cola_espera.desencolar()
                cliente.tiempo_espera = 0
                escritorio.asignar_cliente(cliente)

            if escritorio.cliente_actual:
                escritorio.atender()
                if escritorio.cliente_actual is None and escritorio.ultimo_cliente:
                    cliente = escritorio.ultimo_cliente
                    cliente.tiempo_total = escritorio.ultimo_tiempo
                    self.clientes_atendidos.agregar(cliente)
                    atendidos.append(cliente)
                    escritorio.ultimo_cliente = None  # evitar duplicado

        # Mostrar estado en consola
        print("\n📋 COLA ACTUAL:")
        i = 1
        temp = self.cola_espera.frente
        while temp:
            c = temp.dato
            print(f"{i}. {c.nombre} (DPI: {c.dpi})")
            temp = temp.siguiente
            i += 1

        for c in atendidos:
            print(f"✅ Atendido: {c.nombre}")

        if not atendidos:
            print("⚠️  No se atendió a ningún cliente.")

        print(f"👥 Clientes en espera: {self.cola_espera.tamano()}")
        print(f"✅ Clientes atendidos: {self.clientes_atendidos.tamano()}")
        print("Estado de los escritorios:")
        for esc in self.escritorios.recorrer_adelante():
            estado = "Activo" if esc.activo else "Inactivo"
            print(f"  {esc.identificacion} - {estado}")

    def estadisticas(self):
        tiempos_espera = [c.tiempo_espera for c in self.clientes_atendidos.recorrer()]
        tiempos_atencion = [c.tiempo_total for c in self.clientes_atendidos.recorrer()]

        def resumen(lista):
            if not lista:
                return {"promedio": 0, "max": 0, "min": 0}
            return {
                "promedio": sum(lista) / len(lista),
                "max": max(lista),
                "min": min(lista)
            }

        return {
            "clientes_atendidos": self.clientes_atendidos.tamano(),
            "espera": resumen(tiempos_espera),
            "atencion": resumen(tiempos_atencion)
        }

    def obtener_siguiente_inactivo(self):
        for escritorio in self.escritorios.recorrer_adelante():
            if not escritorio.activo:
                return escritorio
        return None

    def __str__(self):
        return f"{self.nombre} ({self.direccion})"
