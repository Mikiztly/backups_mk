#!/usr/bin/python3.12

import os, paramiko
# 3.12.7
# Configuración del servidor
hostname = "192.168.78.53"
port = 22
username = "admin"
password = "admin"

# Ruta del archivo en el MikroTik
remote_path = "4011_IDS.backup"  # Ruta del archivo en el MikroTik

# Obtener la ruta al escritorio
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
# local_path = r"d:\basura\4011_IDS.backup"
local_path = os.path.join(desktop, "4011_IDS.backup")  # Guardar en el escritorio

# Crear un cliente SSH
client = paramiko.SSHClient()
# Aceptar automáticamente las claves del servidor si no están en known_hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    # Conectar al servidor
    client.connect(hostname, port=port, username=username, password=password,look_for_keys=False)
    print("Conexión SSH exitosa")
    # Borro backups viejos
    """ stdin, stdout, stderr = client.exec_command("rm MK_PRUEBAS-20241127-190428.rsc")
    print("Salida del comando:")
    print(stdout.read().decode()) """
    # Ejecutar un comando
    stdin, stdout, stderr = client.exec_command("ls -l")
    print("Salida del comando:")
    print(stdout.read().decode())
    # Iniciar una sesión SFTP
    #sftp = client.open_sftp()
    # Descargar el archivo
    #print(f"Descargando {remote_path} desde el MikroTik...")
    #sftp.get(remote_path, local_path)
    #print(f"Archivo descargado exitosamente en {local_path}")
    #sftp.close()
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