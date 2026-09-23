import pytest  # Framework de pruebas
from paquete import Paquete, TransicionInvalida  # Clases del dominio a probar
from asignacion import Notificador, ServicioAsignacion  # Clases del servicio a probar


# Verifica el flujo completo: Creado -> Asignado -> En camino -> Entregado
def test_flujo_completo():
    p = Paquete("PKG-001")           # Crea un paquete nuevo
    assert p.estado == "Creado" #"Asignado"       # Debe iniciar en Creado

    p.asignar("REP-10")              # Asigna un repartidor
    assert p.estado == "Asignado"    # Debe pasar a Asignado
    assert p.repartidor_id == "REP-10"  # Debe guardar el id del repartidor

    p.iniciar_viaje()                # Inicia el viaje
    assert p.estado == "En camino"   # Debe pasar a En camino

    p.entregar()                     # Marca como entregado
    assert p.estado == "Entregado"   # Debe quedar en Entregado


# Verifica que no se pueda saltar estados (entregar desde Creado debe fallar)
def test_no_se_puede_entregar_desde_creado():
    p = Paquete("PKG-002")  # Paquete recién creado
    
    # pytest.raises le dice a pytest que dentro del bloque se espera una excepción de tipo TransicionInvalida
    with pytest.raises(TransicionInvalida):
        # intentamos pasar de Creado -> Entregado, lo cual es inválido
        # si p.entregar() lanza TransicionInvalida, el bloque with no lanza error y se pasa el test
        p.entregar()
        #p.asignar("REP-10") 
    

# Verifica que el servicio asigne el paquete y notifique al repartidor
def test_asignar_y_notificar():
    p = Paquete("PKG-003")                 # Paquete a asignar
    noti = Notificador()                   # Notificador en memoria
    servicio = ServicioAsignacion(noti)    # Servicio con ese notificador

    servicio.asignar_y_notificar(p, "REP-22")  # Ejecuta el caso de uso

    # comprobamos que los resultados sean los esperados usando assertions

    assert p.estado == "Asignado"           # El paquete quedó asignado
    assert len(noti.enviados) == 1         # Se envió exactamente 1 notificación
    assert noti.enviados[0][0] == ("REP-22")  # El destinatario es REP-22
