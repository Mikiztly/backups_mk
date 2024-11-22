# Conectar a mariadb, verificar si existe la tabla Equipos y si no existe crearla con los campos Nombre, Router, Puerto, Usuario, Password, Cliente, Ruta
import mysql.connector
from mysql.connector import Error

def conectar_db(host, usuario, password, base_datos):
  try:
    # Conexión a la base de datos
    conexion = mysql.connector.connect(host=host, user=usuario, password=password, database=base_datos)
    cursor = conexion.cursor()
    # Verificar si existe la tabla Equipos
    cursor.execute("SHOW TABLES LIKE 'Equipos'")
    existe_tabla = cursor.fetchone()
    # Si no existe la tabla, crearla
    if not existe_tabla:
      cursor.execute("""
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
    cursor.close()
    conexion.close()
    return True
  # Manejo de errores
  except Error as Macana:
    return f"Error al conectar a la base de datos: {Macana.msg}"

# Ejemplo de uso (reemplazar con tus credenciales)
host = "localhost"
usuario = "backup"
password = "Backup-2024"
base_datos = "backup"

resultado = conectar_db(host, usuario, password, base_datos)
if resultado != True:
  print(f"Error en la conexión a la base de datos.\n{resultado}")
