#!/usr/bin/python3.12

import paramiko
# 3.12.7
# Configuración del servidor
hostname = "192.168.78.53"
port = 22
username = "admin"
password = "admin"

# Crear un cliente SSH
client = paramiko.SSHClient()

# Aceptar automáticamente las claves del servidor si no están en known_hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Conectar al servidor
    client.connect(hostname, port=port, username=username, password=password)
    print("Conexión SSH exitosa")

    # Ejecutar un comando
    stdin, stdout, stderr = client.exec_command("ls -l")
    print("Salida del comando:")
    print(stdout.read().decode())

    # Manejo de errores
    errores = stderr.read().decode()
    if errores:
        print("Errores:")
        print(errores)

except Exception as e:
    print(f"Error al conectarse: {e}")

finally:
    # Cerrar la conexión
    client.close()
    print("Conexión cerrada")