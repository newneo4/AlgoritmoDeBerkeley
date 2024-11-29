# Programa Python para sincronizar relojes de estaciones meteorológicas (Cliente)

from dateutil import parser
import threading
import datetime
import socket
import time

# Función para enviar la hora de la estación al servidor
def enviar_hora(cliente):
    while True:
        try:
            hora_actual = datetime.datetime.now()
            cliente.send(str(hora_actual).encode())
            print("[Cliente] Hora enviada correctamente.\n")
        except:
            print("[Error] No se pudo enviar la hora al servidor.\n")
            break
        time.sleep(5)

# Función para recibir la hora sincronizada del servidor
def recibir_hora(cliente):
    while True:
        try:
            hora_sincronizada = parser.parse(cliente.recv(1024).decode())
            print(f"[Cliente] Hora sincronizada recibida: {hora_sincronizada}.\n")
        except:
            print("[Error] No se pudo recibir la hora sincronizada del servidor.\n")
            break

# Función para iniciar la estación meteorológica (cliente)
def iniciar_cliente(puerto=8080):
    cliente = socket.socket()
    cliente.connect(('127.0.0.1', puerto))
    print("[Cliente] Conexión establecida con el servidor.\n")

    # Iniciar hilos para enviar y recibir datos
    hilo_envio = threading.Thread(target=enviar_hora, args=(cliente,))
    hilo_envio.start()

    hilo_recepcion = threading.Thread(target=recibir_hora, args=(cliente,))
    hilo_recepcion.start()

# Código principal
if __name__ == '__main__':
    iniciar_cliente()
