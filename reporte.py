#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly

Se conecta a una DB en mariadb o mysql para guardar los resultados de los backups realizados a los equipos Mikrotik, la estructura de la tabla Backup_logs es la siguiente:

+---------+--------------+------+-----+---------+-------+
| Field   | Type         | Null | Key | Default | Extra |
+---------+--------------+------+-----+---------+-------+
| Status  | varchar(150) | NO   |     | NULL    |       |
| Fecha   | date         | NO   |     | NULL    |       |
| Equipo  | varchar(25)  | NO   |     | NULL    |       |
| Cliente | varchar(25)  | NO   |     | NULL    |       |
+---------+--------------+------+-----+---------+-------+

"""

# Importacion de librerias a utilizar
from datetime import date
import mysql.connector
from mysql.connector import Error

# Con esta rutina verifico que esten creadas las tablas, si no existen las creo
def verifica_db(Server: str, Usuario: str, Contrasegna: str, Base_Datos: str):
  """
  Verifica que la base de datos esté configurada correctamente.
  Args:
    Server: Servidor de la base de datos.
    Usuario: Usuario de la base de datos.
    Contrasegna: Contraseña de la base de datos.
    Base_Datos: Nombre de la base de datos.
  Devuelve:
    True si la base de datos está configurada correctamente, si no existe la tabla Equipos la crea.
    Si hay algún error devuelve un mensaje de error con la descripción del mismo
  """
  try:
    # Conexión a la base de datos
    Conexion = mysql.connector.connect(host=Server, user=Usuario, password=Contrasegna, database=Base_Datos)
    Puntero = Conexion.cursor()
    # Verificar si existe la tabla Equipos
    Puntero.execute("SHOW TABLES LIKE 'Backup_logs'")
    Existe_Tabla = Puntero.fetchone()
    # Si no existe la tabla, crearla
    if not Existe_Tabla:
      Puntero.execute("""
        CREATE TABLE Backup_logs (
          Status VARCHAR(150) NOT NULL,
          Fecha DATE NOT NULL,
          Equipo VARCHAR(25) NOT NULL,
          Cliente VARCHAR(25) NOT NULL
        )
      """)
    # Cerrar el cursor y la conexión
    Puntero.close()
    return True
  # Manejo de errores
  except Error as Macana:
    return f"Error al conectar a la base de datos:\n {Macana.msg}"

# Guardo el resultado del backup en la DB
def resultado_backup(Server: str, Usuario: str, Contrasegna: str, Base_Datos: str, Status: str, Fecha: date, Equipo: str, Cliente: str):
  """
  Guarda en la base de datos el resultado del backup.
  Args:
    Server: Servidor de la base de datos.
    Usuario: Usuario de la base de datos.
    Contrasegna: Contraseña de la base de datos.
    Base_Datos: Nombre de la base de datos.
    Status: El resultado de hacer el backup.
    Fecha: La fecha del backup.
    Equipo: El nombre del equipo.
    Cliente: El nombre del cliente.
  Devuelve:
    True si guarda los datos correctamente.
    Si hay algún error devuelve un mensaje de error con la descripción del mismo
  """
  # Primero verifico que la tabla exista
  Resultado = verifica_db(Server, Usuario, Contrasegna, Base_Datos)
  try:
    if Resultado:
      # Si esta todo bien con la DB guardo el resultado del backup
      Conexion = mysql.connector.connect(host=Server, user=Usuario, password=Contrasegna, database=Base_Datos)
      Puntero = Conexion.cursor()
      # Inserto los datos en la tabla Backup_logs
      sql = "INSERT INTO Backup_logs (Status, Fecha, Equipo, Cliente) VALUES (%s, %s, %s, %s)"
      val = (Status, Fecha, Equipo, Cliente)
      Puntero.execute(sql, val)
      # Confirmo los cambios
      Conexion.commit()
      # Cierro la conexion
      Puntero.close()
      return True
    else:
      return Resultado
  # Manejo de errores
  except Error as Macana:
    return f"Error no manejado:\n {Macana.msg}"
# FIN del guardado del resultado del backup

# Programa principal para pruebas
if __name__ == "__main__":
  import datetime
  Resultado = resultado_backup("localhost", "strongsystems", "k8TY6&c7D4mW", "strong_db", "Prueba", datetime.datetime.now(), "Mikiztly", "Mikiztly")
  # Imprimo el resultado para verificar que salio todo bien
  print(Resultado)
