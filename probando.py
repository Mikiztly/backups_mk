#!/usr/bin/python3

import paramiko

# Configuración del servidor
hostname = "192.168.78.53"
port = 22
username = "admin"
password = "admin"

# Creacion de backup de un router o sw Mikrotic
try:
    # Crea un cliente SSH
    ssh = paramiko.SSHClient()
    # Agrego la coneccion ssh como de confianza
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Coneccion al servidor
    ssh.connect(hostname, port=port, username=username, password=password)
    print("Conexión SSH exitosa")
    ssh.close()

# Manejo de errores
except paramiko.AuthenticationException:
    print("Error de autenticación. Verifica el usuario y la contraseña.")
except paramiko.SSHException as Macana:
    print(f"Error de SSH: {Macana}")
except Exception as Macana:
    print(f"Error general: {Macana}")
