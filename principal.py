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
import sys, csv, archivos_csv, maneja_mk, reporte, datetime

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
  Resultado= archivos_csv.verificar_archivo_csv(sys.argv[2],["Nombre", "Equipo", "Puerto", "Usuario", "Contrasegna", "Cliente", "Ruta", "Mensaje"])
  if Resultado != True:
    # Si hay algun error lo informo y salgo
    print(Resultado)
    print("  Encabezados requeridos: ['Nombre', 'Equipo', 'Puerto', 'Usuario', 'Contrasegna', 'Cliente', 'Ruta', 'Mensaje']")
    sys.exit(1)

  # Abro el archivo pasado como primer parametro
  with open(sys.argv[1], 'r', newline='', encoding='utf-8') as Tmp_DB:
    Tmp_Reg_DB = csv.reader(Tmp_DB)
    # Lee la primera fila para acceder a los campos por nombre
    Encabezados_DB = next(Tmp_Reg_DB, None)
    # Recorro cada fila del archivo
    for XLoop in Tmp_Reg_DB:
      # Ya se hizo la verificacion del archivo por lo Obtengo los encabezados
      Datos_DB = dict(zip(Encabezados_DB, XLoop))
      # Abro el archivo pasado como segundo parametro
      with open(sys.argv[2], 'r', newline='', encoding='utf-8') as Tmp_MK:
        Tmp_Reg_MK = csv.reader(Tmp_MK)
        # Lee la primera fila para acceder a los campos por nombre
        Encabezados_MK = next(Tmp_Reg_MK, None)
        # Recorro cada fila del archivo
        for YLoop in Tmp_Reg_MK:
          # Obtengo la fecha y hora actual para armar el nombre del archivo
          Fecha = datetime.datetime.now()
          # Ya se hizo la verificacion del archivo por lo Obtengo los encabezados
          Datos_MK = dict(zip(Encabezados_MK, YLoop))
          # Llamo a la funcion para hacer el backup y obtengo si se realizo bien el backup o que error tuvo
          Resultado = maneja_mk.backup_mk(Datos_MK.get("Nombre"), Datos_MK.get("Equipo"), Datos_MK.get("Puerto"), Datos_MK.get("Usuario"), Datos_MK.get("Contrasegna"), Datos_MK.get("Ruta"), Datos_MK.get("Nombre") + "-" + Fecha.strftime("%Y%m%d-%H%M%S"), Datos_MK.get("Mensaje"))
          # si me devuelve el mensaje pasado como argumento guardo el OK en la DB
          if Resultado == Datos_MK.get("Mensaje"):
            reporte.resultado_backup(Datos_DB.get("Servidor"), Datos_DB.get("Usuario"), Datos_DB.get("Contrasegna"), Datos_DB.get("Base_Datos"), Resultado, Fecha, Datos_MK.get("Nombre"), Datos_MK.get("Cliente"))
          else:
            reporte.resultado_backup(Datos_DB.get("Servidor"), Datos_DB.get("Usuario"), Datos_DB.get("Contrasegna"), Datos_DB.get("Base_Datos"), Resultado, Fecha, Datos_MK.get("Nombre"), Datos_MK.get("Cliente"))

# Paso algo que no tuve en cuenta, lo informo
except Exception as Macana:
  print(f"Error no manejado:\n {Macana}")
