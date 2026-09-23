# Simula un servicio de notificaciones (en memoria, para pruebas)
class Notificador:
    # Al crear el notificador, prepara una lista vacía para registrar envíos
    def __init__(self):
        self.enviados = []  # Historial de notificaciones: lista de tuplas (repartidor_id, mensaje)

    # Guarda una notificación dirigida a un repartidor
    def notificar(self, repartidor_id: str, mensaje: str):
        self.enviados.append((repartidor_id, mensaje))  # Agrega la notificación al historial
        return True  # Indica que la notificación se "envió" correctamente


# Controlador GRASP: coordina el caso de uso de asignar y avisar
class ServicioAsignacion:
    """
    Controller GRASP: coordina el caso de uso
    """

    # Recibe el notificador por inyección de dependencias
    def __init__(self, notificador: Notificador):
        self.notificador = notificador  # Guarda el colaborador que enviará avisos

    # Asigna el paquete a un repartidor y le manda una notificación
    def asignar_y_notificar(self, paquete, repartidor_id: str):
        # Cambia el estado del paquete a Asignado y guarda el repartidor
        paquete.asignar(repartidor_id)

        # Avisa al repartidor que tiene un nuevo envío
        self.notificador.notificar(
            repartidor_id,                          # Destinatario
            f"Nuevo envio asignado: {paquete.id}"   # Mensaje con el id del paquete
        )

        return paquete  # Devuelve el paquete ya actualizado
