# Excepción personalizada: se lanza cuando alguien intenta un cambio de estado no permitido
class TransicionInvalida(Exception):
    pass  # No necesita lógica extra; solo sirve como tipo de error identificable


class Paquete:
    # Tupla con los estados válidos del ciclo de vida del paquete
    ESTADOS = ("Creado", "Asignado", "En camino", "Entregado")

    # Diccionario de reglas: cada estado apunta al conjunto de estados a los que puede pasar
    # Creado -> Asignado
    # Asignado -> En camino
    # En camino -> Entregado
    # Entregado -> ninguno (set vacío = estado final)
    TRANSICIONES = {
        "Creado": {"Asignado"},
        "Asignado": {"En camino"},
        "En camino": {"Entregado"},
        "Entregado": set()
    }

    # Constructor: crea un paquete nuevo con id y estado inicial
    def __init__(self, id_paquete: str):
        self.id = id_paquete          # Identificador único del paquete
        self.estado = "Creado"        # Todo paquete empieza en "Creado"
        self.repartidor_id = None     # Aún no tiene repartidor asignado

    # Método interno (privado por convención del "_"): valida y aplica un cambio de estado
    def _cambiar(self, nuevo: str):
        # Si el estado destino no está permitido desde el estado actual, lanza error
        if nuevo not in self.TRANSICIONES[self.estado]:
            raise TransicionInvalida(f"No se puede pasar de : {self.estado} -> {nuevo}")

        # Si la transición es válida, actualiza el estado
        self.estado = nuevo

    # Caso de uso: asignar un repartidor al paquete
    def asignar(self, repartidor_id: str):
        self._cambiar("Asignado")              # Pasa de Creado a Asignado (si es válido)
        self.repartidor_id = repartidor_id     # Guarda quién entregará el paquete

    # Caso de uso: el repartidor inicia el viaje
    def iniciar_viaje(self):
        self._cambiar("En camino")  # Solo funciona si el estado actual es Asignado

    # Caso de uso: marcar el paquete como entregado
    def entregar(self):
        self._cambiar("Entregado")  # Solo funciona si el estado actual es En camino
