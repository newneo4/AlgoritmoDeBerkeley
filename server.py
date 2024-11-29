# Programa Python para sincronizar relojes de estaciones meteorológicas (Servidor)

from dateutil import parser
import threading
import datetime
import socket
import time

# Diccionario para almacenar los datos de las estaciones
datos_estaciones = {}

# Función para recibir la hora desde las estaciones meteorológicas
def recibir_hora_estacion(conector, direccion):
    while True:
        try:
            # Recibir la hora del cliente
            hora_recibida = conector.recv(1024).decode()
            hora_estacion = parser.parse(hora_recibida)

            # Calcular la diferencia de tiempo con el servidor
            diferencia = datetime.datetime.now() - hora_estacion

            # Almacenar los datos de la estación
            datos_estaciones[direccion] = {
                "hora_estacion": hora_estacion,
                "diferencia": diferencia,
                "conector": conector
            }
            print(f"[Actualización] Datos recibidos de la estación {direccion}.\n")
        except:
            print(f"[Error] La estación {direccion} dejó de responder.\n")
            break

        time.sleep(5)

# Función para aceptar conexiones de estaciones
def aceptar_conexiones(servidor):
    while True:
        conector, direccion = servidor.accept()
        direccion_estacion = f"{direccion[0]}:{direccion[1]}"
        print(f"[Conexión] Estación {direccion_estacion} conectada correctamente.\n")
        
        # Crear un hilo para recibir datos de la estación
        hilo = threading.Thread(target=recibir_hora_estacion, args=(conector, direccion_estacion))
        hilo.start()

# Calcular la diferencia promedio de tiempo
def calcular_diferencia_promedio():
    diferencias = [datos["diferencia"] for datos in datos_estaciones.values()]
    suma_diferencias = sum(diferencias, datetime.timedelta(0))
    return suma_diferencias / len(diferencias) if diferencias else datetime.timedelta(0)

# Función para sincronizar los relojes de las estaciones
def sincronizar_relojes():
    while True:
        print(f"[Sincronización] Iniciando nuevo ciclo de sincronización...\n")
        if datos_estaciones:
            diferencia_promedio = calcular_diferencia_promedio()
            hora_sincronizada = datetime.datetime.now() + diferencia_promedio

            for direccion, datos in datos_estaciones.items():
                try:
                    datos["conector"].send(str(hora_sincronizada).encode())
                    print(f"[Sincronización] Hora sincronizada enviada a la estación {direccion}.\n")
                except:
                    print(f"[Error] No se pudo sincronizar con la estación {direccion}.\n")
        else:
            print("[Sincronización] No hay estaciones conectadas.\n")
        
        time.sleep(10)

# Función para iniciar el servidor
def iniciar_servidor(puerto=8080):
    servidor = socket.socket()
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('', puerto))
    servidor.listen(10)
    print("[Servidor] Estación central iniciada correctamente.\n")

    # Iniciar el hilo para aceptar conexiones
    hilo_conexiones = threading.Thread(target=aceptar_conexiones, args=(servidor,))
    hilo_conexiones.start()

    # Iniciar el hilo para sincronizar relojes
    hilo_sincronizacion = threading.Thread(target=sincronizar_relojes)
    hilo_sincronizacion.start()

# Código principal
if __name__ == '__main__':
    iniciar_servidor()
