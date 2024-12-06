#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly

Se ejecuta pasando como argumentos dos archivos:

1) Un txt con los datos para conectarse al servidor sql para guardar los informes de los backups, los datos que tiene son:
  host:localhServidor de la base de datos.ost
  user:Usuario de la base de datos.
  password:Contraseña de la base de datos.
  database:Nombre de la base de datos.

2) El segundo tiene que ser un archivo csv que contenga los datos de los equipos para hacer el backup, los datos que tiene son:
  Encabezados: ["Nombre", "Equipo", "Puerto", "Usuario", "Contrasegna", "Cliente", "Ruta"]

Verifica la existencia de los archivos y después los abrire para guardar cada campo en variables
"""
# Importacion de librerias a utilizar
import sys, csv, archivos_csv, maneja_mk, maneja_db, datetime

# Por si acaso tambien hago captura de errores
try:
  # Verificacion que se pasen los dos argumentos
  if len(sys.argv) != 3:
    # Si hay algun error lo informo y salgo
    print("Uso: python script.py <Base_Datos.csv> <Equipos.csv>")
    sys.exit(1)

  # Verifico que el primer archivo sea el correcto para conectarse a la DB
  # Abro el archivo de solo lectura y guardo en un diccionario los datos para conectarme a la DB
  with open(sys.argv[1], 'r') as Archivo:
    Credenciales_DB = {}
    for Linea in Archivo:
      Clave, Valor = Linea.strip().split(':')
      Credenciales_DB[Clave.strip()] = Valor.strip()
  # Si devuelve un str es por que hubo algun error
  if isinstance(Credenciales_DB, str):
    print(f"Hubo un problema al leer las credenciales: \n {Credenciales_DB}")
    sys.exit(1)
  
  # Ahora intento conectarme a la DB
  BaseDatos = maneja_db.DatabaseManager(Credenciales_DB)
  Resultado = BaseDatos.conectar()
  # Si devuelve true es por que se conecto bien a la DB
  if Resultado:
    # Verifico las tablas
    BaseDatos.verifica_tablas()
  else:
    # Si hay algun error lo informo y salgo
    print(f"Error al conectar a la base de datos:\n {Resultado}")
    sys.exit(1)
  
  # Verifico que el segundo archivo sea el correcto para obtener los datos de los equipos
  Resultado= archivos_csv.verificar_archivo_csv(sys.argv[2],["Nombre", "Equipo", "Puerto", "Usuario", "Contrasegna", "Cliente", "Ruta", "Mensaje"])
  if Resultado != True:
    # Si hay algun error lo informo y salgo
    print(Resultado)
    print("  Encabezados requeridos: ['Nombre', 'Equipo', 'Puerto', 'Usuario', 'Contrasegna', 'Cliente', 'Ruta', 'Mensaje']")
    sys.exit(1)

  # Ahora se utiliza el csv con los datos de los equipos
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
      Resultado = maneja_mk.Backup_MK(Datos_MK.get("Nombre"), Datos_MK.get("Equipo"), Datos_MK.get("Puerto"), Datos_MK.get("Usuario"), Datos_MK.get("Contrasegna"), Datos_MK.get("Ruta"), Datos_MK.get("Nombre") + "-" + Fecha.strftime("%Y%m%d-%H%M%S"), Datos_MK.get("Mensaje"))
      # Guardo el resultado en la DB
      BaseDatos.Backup_Logs([Resultado, Fecha, Datos_MK.get("Nombre"), Datos_MK.get("Cliente")])
  # Ya termino de hacer los backups asi que cierro la DB
  BaseDatos.cerrar()

# Paso algo que no tuve en cuenta, lo informo
except Exception as Macana:
  print(f"Error no manejado:\n {Macana}")
