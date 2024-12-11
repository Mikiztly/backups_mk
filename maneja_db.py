#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly

Se conecta a un servidor mariadb o mysql para guardar en una DB los datos del proceso de manejar equipos MK.

Tabla backup_logs:
Guarda los resultados de los backups realizados a los equipos Mikrotik, la estructura es la siguiente:

+-------------+------+------+-----+---------+-------+
| Field       | Type | Null | Key | Default | Extra |
+-------------+------+------+-----+---------+-------+
| status      | text | NO   |     | NULL    |       |
| date        | text | NO   |     | NULL    |       |
| system_name | text | NO   |     | NULL    |       |
| client      | text | NO   |     | NULL    |       |
+-------------+------+------+-----+---------+-------+

"""

# Importación de librerías a utilizar
import mysql.connector
from mysql.connector import Error

class DatabaseManager:
  def __init__(self, Servidor):
    self.Server = Servidor
    self.connection = None
    self.cursor = None

  def conectar(self):
    """
    Conecta a la base de datos mediante un diccionario con los siguientes campos:
    Args:
      host: Servidor de la base de datos.
      user: Usuario de la base de datos.
      password: Contraseña de la base de datos.
      database: Nombre de la base de datos.
    Devuelve:
      True si se conecta correctamente a la base de datos.
      Si hay algún error devuelve un mensaje de error con la descripción del mismo
    """
    try:
      self.connection = mysql.connector.connect(**self.Server)
      self.cursor = self.connection.cursor()
      return True
    except Error as Macana:
      return f"Error al conectar a la base de datos: {Macana}"

  def cerrar(self):
    """ 
    Si hay un cursor y/o una conexión abierta los cierra
    Devuelve:
      True si se cierra correctamente.
      Si hay algún error devuelve un mensaje de error con la descripción del mismo.
    """
    try:
      if self.cursor:
        self.cursor.close()
      if self.connection:
        self.connection.close()
      return True
    except Error as Macana:
      return f"Error al cerrar la conexión: {Macana}"

  def verifica_tablas(self):
    """ 
    Crea la tabla según los parámetros especificados.
    Devuelve:
      True si se crea correctamente
      Si hay algún error devuelve un mensaje de error con la descripción del mismo
    """
    try:
      self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS backup_logs (
          `status` TEXT NULL,
          `date` TEXT NULL,
          `system_name` TEXT NULL,
          `client` TEXT NULL 
          )
      """)
      self.connection.commit()
      return True
    except Error as Macana:
      return f"Error al crear la tabla: {Macana}"

  def Backup_Logs(self, Entrada):
    """
    Utiliza una lista para escribir datos en la tabla Backup_Logs.
    Args:
      (Status, Fecha, Equipo, Cliente)
    Devuelve:
      True si se crea correctamente
      Si hay algún error devuelve un mensaje de error con la descripción del mismo
    """
    try:
      sql = "INSERT INTO backup_logs (status, date, system_name, client) VALUES (%s, %s, %s, %s)"
      self.cursor.execute(sql, Entrada)
      self.connection.commit()
      return True
    except Error as Macana:
      return f"Error al insertar datos: {Macana}"

if __name__ == "__main__":
  import datetime
  
  Servidor_sql = {
    "host": "localhost",
    "user": "strongsystems",
    "password": "nada",
    "database": "Prueba"
  }
  
  datos_equipo = ("Prueba", datetime.datetime.now(), "Mikiztly", "Mikiztly")
  
  BaseDatos = DatabaseManager(Servidor_sql)
  Resultado = BaseDatos.conectar()
  print(Resultado)
  Resultado = BaseDatos.verifica_tablas()
  print(Resultado)
  Resultado = BaseDatos.Backup_Logs(datos_equipo)
  print(Resultado)
  Resultado = BaseDatos.cerrar()
  # Imprimo el resultado para verificar que salio todo bien
  print(Resultado)
