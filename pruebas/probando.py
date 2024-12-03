#!/usr/bin/python3

""" usar el archivo servidor_sql.txt para obtener los datos, guardarlos en un diccionario y conectarse a un servidor sql
Servidor=localhost
Usuario=strongsystems
Contrasegna=k8TY6&c7D4mW
Base_Datos=strong_db
 """
 
import mysql.connector
from mysql.connector import Error

def conectar_db(Host, Usuario, Contrasegna, Base_Datos):
  try:
    # Conexión a la base de datos
    Conexion = mysql.connector.connect(host=Host, user=Usuario, password=Contrasegna, database=Base_Datos)
    Puntero = Conexion.cursor()
    # Verificar si existe la tabla Equipos
    Puntero.execute("SHOW TABLES LIKE 'Equipos'")
    Existe_Tabla = Puntero.fetchone()
    # Si no existe la tabla, crearla
    if not Existe_Tabla:
      Puntero.execute("""
        CREATE TABLE Equipos (
          Nombre VARCHAR(25) NOT NULL,
          Router VARCHAR(15) NOT NULL,
          Puerto INT NOT NULL,
          Usuario VARCHAR(25) NOT NULL,
          Password VARCHAR(25) NOT NULL,
          Cliente VARCHAR(25) NOT NULL,
          Ruta VARCHAR(25) NOT NULL,
          PRIMARY KEY (Router),
          UNIQUE (Nombre)
        )
      """)
    # Cerrar el cursor y la conexión
    Puntero.close()
    return True
  # Manejo de errores
  except Error as Macana:
    return f"Error al conectar a la base de datos: {Macana.msg}"

# Ejemplo de uso (reemplazar con tus credenciales)
try:
  with open("/home/dcasavilla/backups_mk/servidor_sql.txt", "r") as archivo:
    datos = {}
    for linea in archivo:
      clave, valor = linea.strip().split("=")
      datos[clave] = valor.strip()
  host = datos["Servidor"]
  usuario = datos["Usuario"]
  password = datos["Contrasegna"]
  base_datos = datos["Base_Datos"]

  resultado = conectar_db(host, usuario, password, base_datos)
  if resultado != True:
    print(f"Error en la conexión a la base de datos.\n{resultado}")
  else:
    print("Conexión exitosa a la base de datos.")

except FileNotFoundError:
  print("El archivo 'servidor_sql.txt' no se encuentra.")
except Exception as e:
  print(f"Error inesperado: {e}")