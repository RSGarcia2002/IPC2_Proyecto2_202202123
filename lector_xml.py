import xml.etree.ElementTree as ET
from modelos.empresa import Empresa
from modelos.punto_atencion import PuntoAtencion
from modelos.escritorio import Escritorio
from modelos.transaccion import Transaccion
from modelos.cliente import Cliente

class LectorXML:

    @staticmethod
    def cargar_configuracion(ruta, lista_empresas):
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            for e in root.findall("empresa"):
                id_empresa = e.get("id")
                nombre = e.find("nombre").text.strip()
                abreviatura = e.find("abreviatura").text.strip()

                empresa = Empresa(id_empresa, nombre, abreviatura)

                # Puntos de atención
                for p in e.find("listaPuntosAtencion").findall("puntoAtencion"):
                    id_punto = p.get("id")
                    nombre_punto = p.find("nombre").text.strip()
                    direccion = p.find("direccion").text.strip()

                    punto = PuntoAtencion(id_punto, nombre_punto, direccion)

                    # Escritorios
                    for es in p.find("listaEscritorios").findall("escritorio"):
                        id_escritorio = es.get("id")
                        identificacion = es.find("identificacion").text.strip()
                        encargado = es.find("encargado").text.strip()

                        escritorio = Escritorio(id_escritorio, identificacion, encargado)
                        punto.agregar_escritorio(escritorio)

                    empresa.agregar_punto(punto)

                # Transacciones
                for t in e.find("listaTransacciones").findall("transaccion"):
                    id_trans = t.get("id")
                    nombre_trans = t.find("nombre").text.strip()
                    tiempo = int(t.find("tiempoAtencion").text.strip())

                    transaccion = Transaccion(id_trans, nombre_trans, tiempo)
                    empresa.agregar_transaccion(transaccion)

                lista_empresas.agregar(empresa)

            print("Archivo de configuración cargado correctamente.")
        except Exception as e:
            print(f"Error al cargar archivo XML: {e}")

    @staticmethod
    def cargar_inicial(ruta, lista_empresas):
        import xml.etree.ElementTree as ET
        from modelos.cliente import Cliente

        try:
            tree = ET.parse(ruta)
            root = tree.getroot()

            for conf in root.findall("configInicial"):
                id_empresa = conf.get("idEmpresa")
                id_punto = conf.get("idPunto")

                empresa = lista_empresas.buscar(lambda e: e.id == id_empresa)
                if not empresa:
                    continue

                punto = empresa.obtener_punto(id_punto)
                if not punto:
                    continue

                # Activar escritorios
                for e_activo in conf.find("escritoriosActivos").findall("escritorio"):
                    id_escritorio = e_activo.get("idEscritorio")
                    escritorio = punto.escritorios.buscar(lambda e: e.id == id_escritorio)
                    if escritorio:
                        escritorio.activar()

                # Cargar clientes
                for c in conf.find("listadoClientes").findall("cliente"):
                    dpi = c.get("dpi")
                    nombre = c.find("nombre").text.strip()
                    cliente = Cliente(dpi, nombre)

                    for t in c.find("listadoTransacciones").findall("transaccion"):
                        id_trans = t.get("idTransaccion")
                        cantidad = int(t.get("cantidad"))

                        transaccion = empresa.obtener_transaccion(id_trans)
                        if transaccion:
                            cliente.agregar_transaccion(transaccion, cantidad)

                    if c.get("prioridad") == "si":
                        punto.agregar_cliente_prioridad(cliente)
                    else:
                        punto.agregar_cliente(cliente)
            
            print("Archivo de inicio cargado correctamente.")

            print("\n🧾 Estado de la cola de espera:")
            temp = punto.cola_espera.frente
            i = 1
            while temp:
                cliente = temp.dato
                print(f"{i}. {cliente.nombre} (DPI: {cliente.dpi})")
                temp = temp.siguiente
                i += 1
        except Exception as e:
            print(f"Error al cargar archivo de inicio: {e}")
