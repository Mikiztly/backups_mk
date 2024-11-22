#!/usr/bin/python3

# Importacion de librerias a utilizar
import os, sys, csv, datetime, time

# Guardo en la DB el resultado de hacer el backup
def reporte(Resultado):
  if Parametros:
    print()
    print("********************")
    print("Parametros del Servidor web:")
    print(f"Host: {Parametros[0]}")
    print(f"Usuario: {Parametros[1]}")
    print(f"Password: {Parametros[2]}")
    print(f"BaseDatos: {Parametros[3]}")
    print(f"Resultado: {Resultado}")
    print("********************")
    print()
  # espero 5 segundos para poder leer el mensaje
  time.sleep(5)
# FIN del reporte

# Creacion de backup de un router o sw Mikrotic
def backup_mk(therouter, theuser, thepassword, theport, theroute, archivo_bkp):
  import paramiko
  """Copia archivos a un servidor remoto por SSH.
  Args:
    therouter: La dirección IP o nombre de host del servidor remoto.
    theuser: El nombre de usuario para la conexión SSH.
    thepassword: La contraseña para la conexión SSH.
    theport: El puerto SSH (por defecto 22).
    archivo_bkp: el nombre del backup a crear
    theroute: La ruta en el servidor donde se copiarán los archivos.
  """
  '''
  Router de pruebas MK
  user: admin
  pass: admin
  ssh: 22
  ip: 192.168.78.53
  '''
  try:
    # Crea un cliente SSH
    ssh = paramiko.SSHClient()
    # Agrego la coneccion ssh como de confianza
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Coneccion al servidor
    ssh.connect(therouter, port=theport, username=theuser, password=thepassword,look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command("system/identity/print")
    archivo_bkp = stdout.read().decode() + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # Creo los archivos de backup
    stdin, stdout, stderr = ssh.exec_command(f"/system backup save dont-encrypt=yes name={archivo_bkp}")
    print(stdout.read().decode())
    stdin, stdout, stderr = ssh.exec_command(f"/export file={archivo_bkp}")
    print(stdout.read().decode())
    stdin, stdout, stderr = ssh.exec_command("ls -l")
    print(stdout.read().decode())
    # Crea un cliente SFTP
    sftp = ssh.open_sftp()
    # Copio los archivos de backup
    archivo_origen = archivo_bkp + ".backup"
    archivo_destino = theroute + "/" + archivo_origen
    sftp.get(archivo_origen, archivo_destino)
    print(f"Archivo '{archivo_origen}' copiado a '{theroute}' correctamente.")
    stdin, stdout, stderr = ssh.exec_command(f"rm {archivo_origen}")
    print(stdout.read().decode())
    archivo_origen = archivo_bkp + ".rsc"
    archivo_destino = theroute + "/" + archivo_origen
    sftp.get(archivo_origen, archivo_destino)
    print(f"Archivo '{archivo_origen}' copiado a '{theroute}' correctamente.")
    stdin, stdout, stderr = ssh.exec_command(f"rm {archivo_origen}")
    print(stdout.read().decode())
    # Cierra la conexión SFTP y SSH
    sftp.close()
    ssh.close()
    return ("Backup realizado correctamente")
  # Manejo de errores
  except Exception as Macana:
    # Cierra la conexión SFTP y SSH
    sftp.close()
    ssh.close()
    return (f"Error general: {Macana}")
# FIN de la creacion del backup

# Programa principal
if __name__ == "__main__":
  # Verificacion que se pasen los dos argumentos y sean archivos csv
  if len(sys.argv) != 3:
    print("Uso: python script.py <ruta_del_archivo1.csv> <ruta_del_archivo2.csv>")
    sys.exit(1)

  # Guardo los archivos csv en dos variables
  BaseDatos = sys.argv[1]
  Equipos = sys.argv[2]
  # Comprobamos que los archivos sean existan y sean accesibles
  if verificar_archivos_csv(BaseDatos, Equipos):
    print("Ambos archivos CSV existen y son accesibles:")
    print(f"Ruta del primer archivo: {BaseDatos}")
    print(f"Ruta del segundo archivo: {Equipos}")
  else:
    sys.exit(1)

  # Extraigo los parametros de la DB y los guardo en una coleccion, despues siempre utilizo esta coleccion para guardar un informe de la ejecucion del backup
  Parametros = parametros_db(BaseDatos)

  # Reccorro todos los registros del archivo Equipos para hacer el backup
  try:
    # Abro el archivo de Equipos pasado como parametro
    with open(Equipos, 'r', newline='', encoding='utf-8') as Tmp_Equipos:
      Tmp_Reg = csv.reader(Tmp_Equipos)
      # Lee la primera fila para acceder a los campos por nombre
      Encabezados = next(Tmp_Reg, None) 
      # Recorro cada fila del archivo
      for XLoop in Tmp_Reg:
        # Verifico que haya encabezados y creo un diccionario
        if Encabezados:
          datos = dict(zip(Encabezados, XLoop))
          # Guardo los campos en variables refiriendome a los encabezados
          therouter = datos.get("Router")
          thepassword = datos.get("Password")
          thename = datos.get("\ufeffNombre")
          theuser = datos.get("Usuario")
          theclient = datos.get("Cliente")
          theport = datos.get("Puerto")
          theroute = os.getcwd() + "/" + datos.get("Ruta") + "/" + thename
          # Imprimo las variables
          print()
          print("--------------------")
          print(f"Router: {therouter} (lenght: {len(therouter)})")
          print(f"Password: {thepassword} (lenght: {len(thepassword)}))")
          print(f"Nombre: {thename} (lenght: {len(thename)})")
          print(f"Usuario: {theuser} (lenght: {len(theuser)})")
          print(f"Cliente: {theclient} (lenght: {len(theclient)})")
          print(f"Puerto: {theport} (lenght: {len(theport)})")
          print(f"Ruta: {theroute}")
        else:
          print(f"El archivo '{Equipos}' no tiene encabezados.")
        # Si no existe creo el directorio para el backup
        if not os.path.exists(theroute):
          os.makedirs(theroute)
        # Creo el backup
        print()
        print("Creando backup...")
        # Obtengo la fecha y hora actual
        archivo_bkp = thename + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        # Llama a la funcion para hacer el backup y guarda en la DB si se realizo bien o no el backup
        reporte(backup_mk(therouter, theuser, thepassword, theport, theroute, archivo_bkp))
  # Manejo de errores
  except Exception as Macana:
    print(f"Error en el programa principal: {Macana}")
  except OSError as Macana:
    print(f"Error al crear directorios: {Macana}")
