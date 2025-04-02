from estructuras.pila import Pila

class Gestor:
    def __init__(self):
        self.empresas = []  # o tu estructura TDA
        self.escritorios_activos = {}  # clave: (empresa_id, punto_id) → valor: Pila

    def activar_escritorio(self, empresa_id, punto_id):
        # Buscar punto y escritorio inactivo
        punto = self.buscar_punto(empresa_id, punto_id)
        escritorio = punto.obtener_siguiente_inactivo()  # Este método lo deberás implementar
        if escritorio:
            escritorio.activar()
            key = (empresa_id, punto_id)
            if key not in self.escritorios_activos:
                self.escritorios_activos[key] = Pila()
            self.escritorios_activos[key].push(escritorio)
            return escritorio
        return None

    def desactivar_escritorio(self, empresa_id, punto_id):
        key = (empresa_id, punto_id)
        if key in self.escritorios_activos and not self.escritorios_activos[key].esta_vacia():
            escritorio = self.escritorios_activos[key].pop()
            escritorio.desactivar()
            return escritorio
        return None
