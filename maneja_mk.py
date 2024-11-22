#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly

Por ahora hace un backup del equipo que se paso con los parametros y descarga dos archivos ( .backup y .rsc) en la ruta especificada
Los parametros se deben pasar como un diccionario donde las claves deben ser:
["Nombre", "Equipo", "Puerto", "Usuario", "Contrasegna", "Cliente", "Ruta"]
"""
# Importacion de librerias a utilizar
import os,datetime, paramiko

# Creacion del backup
def backup_mk(thename: str, therouter: str, theport: int, theuser: str, thepassword: str, theroute: str, Mensaje: str):
  """
  Crea un backup en el equipo Mikrotik y descarga los archivos.
  Args:
    thename: El nombre del equipo.
    therouter: La dirección IP o nombre de host del servidor remoto.
    theport: El puerto SSH (por defecto 22).
    theuser: El nombre de usuario para la conexión SSH.
    thepassword: La contraseña para la conexión SSH.
    theroute: La ruta en el servidor donde se copiarán los archivos.
    Mensaje: Mensaje a devolver si se realiza bien el backup
  Devuelve:
    El mesaje pasado como parametro si se realiza bien el backup, en caso contrario devuelve un mensaje de error
  """
  # Captura de errores porsiaca
  try:
    # Si no existe el directorio para el backup lo creo
    if not os.path.exists(theroute):
      os.makedirs(theroute)
    # Obtengo la fecha y hora actual para armar el nombre del archivo
    archivo_bkp = thename + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # Crea un cliente SSH
    ssh = paramiko.SSHClient()
    # Agrego la coneccion ssh como de confianza
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Coneccion al servidor
    ssh.connect(therouter, port=theport, username=theuser, password=thepassword,look_for_keys=False)
    # Creo los archivos de backup
    ssh.exec_command(f"/system backup save dont-encrypt=yes name={archivo_bkp}")
    ssh.exec_command(f"/export file={archivo_bkp}")
    # Crea un cliente SFTP
    # sftp = ssh.open_sftp()
    # Copio el primer archivo
    archivo_origen = archivo_bkp + ".backup"
    archivo_destino = theroute + "/" + archivo_origen
    # sftp.get(archivo_origen, archivo_destino)
    # Borro el primer archivo
    ssh.exec_command(f"rm {archivo_origen}")
    # Copio el segundo archivo
    archivo_origen = archivo_bkp + ".rsc"
    archivo_destino = theroute + "/" + archivo_origen
    # sftp.get(archivo_origen, archivo_destino)
    # Borro el segundo archivo
    ssh.exec_command(f"rm {archivo_origen}")
    # Cierra la conexión SFTP y SSH
    # sftp.close()
    ssh.close()
    # Devuelvo el mensaje pasado como parametro por que salio todo bien
    return (Mensaje)
  # Manejo de errores
  except Exception as Macana:
    # Cierra la conexión SFTP y SSH
    # sftp.close()
    ssh.close()
    return (f"Error general: {Macana}")
# FIN de la creacion del backup

# Programa principal para pruebas
import sys, csv
if __name__ == "__main__":
  try:
    # Abro el archivo pasado como parametro
    with open(sys.argv[1], 'r', newline='', encoding='utf-8') as Tmp_Equipos:
      Tmp_Reg = csv.reader(Tmp_Equipos)
      # Lee la primera fila para acceder a los campos por nombre
      Encabezados = next(Tmp_Reg, None) 
      # Recorro cada fila del archivo
      for XLoop in Tmp_Reg:
        # Verifico que haya encabezados y creo un diccionario
        if Encabezados:
          datos = dict(zip(Encabezados, XLoop))
          # Guardo los campos en variables refiriendome a los encabezados
          therouter = datos.get("Equipo")
          thepassword = datos.get("Contrasegna")
          thename = datos.get("Nombre")
          theuser = datos.get("Usuario")
          theclient = datos.get("Cliente")
          theport = datos.get("Puerto")
          theroute = os.getcwd() + "/" + datos.get("Ruta") + "/" + thename
          # Imprimo las variables
          print()
          print("--------------------")
          print(f"Router: {therouter}")
          print(f"Password: {thepassword}")
          print(f"Nombre: {thename}")
          print(f"Usuario: {theuser}")
          print(f"Cliente: {theclient}")
          print(f"Puerto: {theport}")
          print(f"Ruta: {theroute}")
        else:
          print(f"El archivo '{sys.argv[1]}' no tiene encabezados.")
        # Creo el backup
        print()
        print("Creando backup...")
        # Llama a la funcion para hacer el backup y muestra si se realizo o que error tuvo
        resultado = backup_mk(thename, therouter, theport, theuser, thepassword, theroute, "Backup realizado correctamente")
        print(resultado)
  # Manejo de errores
  except Exception as Macana:
    print(f"Error en el programa principal: {Macana}")
  except OSError as Macana:
    print(f"Error al crear directorios: {Macana}")
