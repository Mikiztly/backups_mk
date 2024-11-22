#!/usr/bin/python3

# Importacion de librerias a utilizar
import os, sys, csv

# Verificacion de la existencia de los archivos
def verificar_archivo_csv(Archivo: str, Encabezados: list):
  """Verifica el archivos CSV existe, es accesible y tiene los encabezados requeridos.
    Args:
      Archivo: La ruta al archivo CSV
      Encabezados: Una lista de encabezados requeridos.
    Devuelve:
      True si el archivo existe, es accesible y tiene los encabezados requeridos.
      En caso contrario devuelve un mensaje de error
  """
  try:
    # Verifico que el archivo exista y sea accesible
    if not os.path.exists(Archivo) or not os.access(Archivo, os.R_OK):
      return(f"Error: El archivo '{Archivo}' no existe o no es accesible.")
    # Ahora se comprueba que tenga los encabezados requeridos
    with open(Archivo, 'r', newline='', encoding='utf-8') as archivo_csv:
      lector_csv = csv.reader(archivo_csv)
      EncabezadosTmp = next(lector_csv)
      if EncabezadosTmp != Encabezados:
        return f"Error: El archivo '{Archivo}' no tiene los encabezados requeridos.\n Encabezados encontrados: {EncabezadosTmp}"
    print(EncabezadosTmp)
    return True
  except Exception as Macana:
    return f"Error no manejado con el archivo CSV:\n {Macana}"
# FIN de la funcion para verificar los archivos

# Abre el archivo con los parametros de la DB y los guarda en una coleccion
def parametros_db(Ruta_DB):
  """Abre un archivo CSV y guarda los Parametros de la primera fila en una coleccion.
    Devuelve:
      Una coleccion con los valores de los Parametros, o None si ocurre un error.
      Imprime un mensaje de error si el archivo no se puede abrir o si está vacío.
    """
  try:
    # Se abre el archivo
    with open(Ruta_DB, 'r', newline='', encoding='utf-8') as Tmp_DB:
      Tmp_Reg = csv.reader(Tmp_DB)
      Parametros = next(Tmp_Reg, None)  # Lee la primera fila
      # Si el archivo esta vacio Muestra el mensaje de error
      if Parametros is None:
        print(f"Error: El archivo CSV '{Ruta_DB}' está vacío.")
        return None
      # Como se pudo leer todo devuelve los parametros
      return Parametros
  # Manejo de errores
  except Exception as Macana:
    print(f"Error al abrir o leer el archivo CSV: {Macana}")
    return None
# FIN de la funcion para extraer los parametros de la DB

# Programa principal para pruebas
if __name__ == "__main__":
  # Comprobamos que el archivo exista y sea accesible
  Resultado = verificar_archivo_csv(sys.argv[1], ["servidor", "usuario", "contraseña", "base_datos"])
  if Resultado != True:
    print(Resultado)
  else:
    print(f"El archivo '{sys.argv[1]}' existe, es accesible y tiene los encabezados requeridos.")
