#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly

Se ejecuta pasando como argumentos dos archivos csv:

1) Datos para conectarse al servidor mariadb para guardar los informes de los backups, los datos que tiene son:
  Encabezados: ["Servidor", "Usuario", "Contrasegna", "Base_Datos"]

2) El segundo csv contiene los datos de los equipos para hacer el backup, los datos que tiene son:
  Encabezados: ["Nombre", "Equipo", "Puerto", "Usuario", "Contrasegna", "Cliente", "Ruta"]

Verificar la existencia de los archivos y después abrirlos para guardar cada campo en variables
"""
# Importacion de librerias a utilizar
import sys, csv, archivos_csv, maneja_mk

# Por si acaso tambien hago captura de errores
try:
  # Verificacion que se pasen los dos argumentos
  if len(sys.argv) != 3:
    # Si hay algun error lo informo y salgo
    print("Uso: python script.py <Base_Datos.csv> <Equipos.csv>")
    sys.exit(1)

  # Verifico que el primer archivo sea el correcto para conectarse a la DB
  Resultado = archivos_csv.verificar_archivo_csv(sys.argv[1], ["Servidor", "Usuario", "Contrasegna", "Base_Datos"])
  if Resultado != True:
    # Si hay algun error lo informo y salgo
    print(Resultado)
    print("  Encabezados requeridos: ['Servidor', 'Usuario', 'Contrasegna', 'Base_Datos']")
    sys.exit(1)

  # Verifico que el segundo archivo sea el correcto para obtener los datos de los equipos
  Resultado= archivos_csv.verificar_archivo_csv(sys.argv[2],["Nombre", "Equipo", "Puerto", "Usuario", "Contrasegna", "Cliente", "Ruta"])
  if Resultado != True:
    # Si hay algun error lo informo y salgo
    print(Resultado)
    print("  Encabezados requeridos: ['Nombre', 'Equipo', 'Puerto', 'Usuario', 'Contrasegna', 'Cliente', 'Ruta']")
    sys.exit(1)

  # Abro el archivo pasado como segundo parametro
  with open(sys.argv[2], 'r', newline='', encoding='utf-8') as Tmp_Equipos:
    Tmp_Reg = csv.reader(Tmp_Equipos)
    # Lee la primera fila para acceder a los campos por nombre
    Encabezados = next(Tmp_Reg, None) 
    # Recorro cada fila del archivo
    for XLoop in Tmp_Reg:
      # Ya se hizo la verificacion del archivo por lo Obtengo los encabezados
      Datos = dict(zip(Encabezados, XLoop))
      # Llamo a la funcion para hacer el backup y obtengo si se realizo bien el backup o que error tuvo
      Resultado = maneja_mk.backup_mk(Datos.get("Nombre"), Datos.get("Equipo"), Datos.get("Puerto"), Datos.get("Usuario"), Datos.get("Contrasegna"), Datos.get("Ruta"), "Backup realizado correctamente")
      print(Resultado)

# Paso algo que no tuve en cuenta, lo informo
except Exception as Macana:
  print(f"Error no manejado:\n {Macana}")
