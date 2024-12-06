#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly

Se conecta a un servidor mariadb o mysql para guardar en una DB los datos del proceo de manejar equipos MK.

Tabla Backup_logs:
Guarda los resultados de los backups realizados a los equipos Mikrotik, la estructura es la siguiente:

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

class DatabaseManager:
  def __init__(self, Servidor):
    self.Server = Servidor
    self.connection = None
    self.cursor = None

  def conectar(self):
    """
    Conecta a la base de datos mediante un diccionario con los siguientes campos:
    Args:
      Server: Servidor de la base de datos.
      Usuario: Usuario de la base de datos.
      Contrasegna: Contraseña de la base de datos.
      Base_Datos: Nombre de la base de datos.
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
    Si hay un cursor y/o una coneccion abierta los cierra
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
    Crea la tabla segun los parametros especificados.
    Devuelve:
      True si se crea correctamente
      Si hay algún error devuelve un mensaje de error con la descripción del mismo
    """
    try:
      self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Backup_Logs (
          Status VARCHAR(150) NOT NULL,
          Fecha DATE NOT NULL,
          Equipo VARCHAR(25) NOT NULL,
          Cliente VARCHAR(25) NOT NULL
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
      sql = "INSERT INTO Backup_Logs (Status, Fecha, Equipo, Cliente) VALUES (%s, %s, %s, %s)"
      # val = (Status, Fecha, Equipo, Cliente)
      # self.cursor.execute(sql, val)
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
    "password": "k8TY6&c7D4mW",
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
