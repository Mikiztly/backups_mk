#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly
Por ahora verifica que exista un archivo csv y tenga los encabezados declarados en el argumento "Encabezados"
"""
# Importacion de librerias a utilizar
import os, sys, csv

# Verificacion de la existencia de los archivos
def verificar_archivo_csv(Archivo: str, Encabezados: list):
  """Verifica que el archivo CSV existe, es accesible y tiene los encabezados requeridos.
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
    with open(Archivo, 'r', newline='', encoding='utf-8') as Archivo_csv:
      Lector_csv = csv.reader(Archivo_csv)
      EncabezadosTmp = next(Lector_csv)
      if EncabezadosTmp != Encabezados:
        return f"Error: El archivo '{Archivo}' no tiene los encabezados requeridos.\n Encabezados encontrados: {EncabezadosTmp}"
    return True
  except Exception as Macana:
    return f"Error no manejado con el archivo CSV:\n {Macana}"
# FIN de la funcion para verificar los archivos

# Programa principal para pruebas
if __name__ == "__main__":
  # Comprobamos que el archivo exista y sea accesible
  Resultado = verificar_archivo_csv(sys.argv[1], ["Servidor", "Usuario", "Contrasegna", "Base_Datos"])
  if Resultado != True:
    print(Resultado)
  else:
    print(f"El archivo '{sys.argv[1]}' existe, es accesible y tiene los encabezados requeridos.")
