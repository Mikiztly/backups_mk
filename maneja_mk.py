#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly

Por ahora hace un backup del equipo que se paso con los parametros y descarga dos archivos ( .backup y .rsc) en la ruta especificada
Los parametros se deben pasar como un diccionario donde las claves deben ser:
["Nombre", "Equipo", "Puerto", "Usuario", "Contrasegna", "Cliente", "Ruta"]
"""
# Importacion de librerias a utilizar
import os,datetime, paramiko, time

# Creacion del backup
def backup_mk(Nombre: str, Equipo: str, Puerto: int, Usuario: str, Contrasegna: str, Ruta: str, Mensaje: str):
  """
  Crea un backup en el equipo Mikrotik y descarga los archivos.
  Args:
    Nombre: El nombre del equipo.
    Equipo: La dirección IP o nombre de host del servidor remoto.
    Puerto: El puerto SSH (por defecto 22).
    Usuario: El nombre de usuario para la conexión SSH.
    Contrasegna: La contraseña para la conexión SSH.
    Ruta: La ruta en el servidor donde se copiarán los archivos.
    Mensaje: Mensaje a devolver si se realiza bien el backup
  Devuelve:
    El mesaje pasado como parametro si se realiza bien el backup, en caso contrario devuelve un mensaje de error
  """
  # Captura de errores porsiaca
  try:
    # Creo la ruta completa donde se guardan los backups
    Ruta_Completa = os.getcwd() + "/" + Ruta + "/" + Nombre
    # Si no existe el directorio para el backup lo creo
    if not os.path.exists(Ruta_Completa):
      os.makedirs(Ruta_Completa)
    # Obtengo la fecha y hora actual para armar el nombre del archivo
    Archivo_bkp = Nombre + "-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # Crea un cliente SSH
    ssh = paramiko.SSHClient()
    # Agrego la coneccion ssh como de confianza
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Coneccion al servidor
    ssh.connect(Equipo, port=Puerto, username=Usuario, password=Contrasegna, look_for_keys=False)
    # Creo los archivos de backup
    ssh.exec_command(f"/system backup save dont-encrypt=yes name={Archivo_bkp}")
    ssh.exec_command(f"/export file={Archivo_bkp}")
    # Crea un cliente SFTP
    sftp = ssh.open_sftp()
    # Copio el primer archivo
    Archivo_Origen = Archivo_bkp + ".backup"
    Archivo_Destino = Ruta_Completa + "/" + Archivo_Origen
    sftp.get(Archivo_Origen, Archivo_Destino)
    # Borro el primer archivo
    ssh.exec_command(f"rm {Archivo_Origen}")
    # Pausa 5 segundos
    time.sleep(5)
    # Copio el segundo archivo
    Archivo_Origen = Archivo_bkp + ".rsc"
    Archivo_Destino = Ruta_Completa + "/" + Archivo_Origen
    sftp.get(Archivo_Origen, Archivo_Destino)
    # Borro el segundo archivo
    ssh.exec_command(f"rm {Archivo_Origen}")
    # Cierra la conexión SFTP y SSH
    sftp.close()
    ssh.close()
    # Devuelvo el mensaje pasado como parametro por que salio todo bien
    return (Mensaje)
  # Manejo de errores
  except Exception as Macana:
    # Cierra la conexión SFTP y SSH
    sftp.close()
    ssh.close()
    return (f"Error general: {Macana}")
  except paramiko.AuthenticationException as Macana:
    # Cierra la conexión SFTP y SSH
    sftp.close()
    ssh.close()
    return (f"Error de credenciales: {Macana}")
  except paramiko.Message as Macana:
    # Cierra la conexión SFTP y SSH
    sftp.close()
    ssh.close()
    return (f"Error ssh o sftp: {Macana}")
  except OSError as Macana:
    print(f"Error al crear directorios: {Macana}")
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
          Equipo = datos.get("Equipo")
          Contrasegna = datos.get("Contrasegna")
          Nombre = datos.get("Nombre")
          Usuario = datos.get("Usuario")
          Cliente = datos.get("Cliente")
          Puerto = datos.get("Puerto")
          Ruta = datos.get("Ruta")
          # Imprimo las variables
          print()
          print("--------------------")
          print(f"Router: {Equipo}")
          print(f"Password: {Contrasegna}")
          print(f"Nombre: {Nombre}")
          print(f"Usuario: {Usuario}")
          print(f"Cliente: {Cliente}")
          print(f"Puerto: {Puerto}")
          print(f"Ruta: {Ruta}")
        else:
          print(f"El archivo '{sys.argv[1]}' no tiene encabezados.")
        # Creo el backup
        print()
        print("Creando backup...")
        # Llama a la funcion para hacer el backup y muestra si se realizo o que error tuvo
        resultado = backup_mk(Nombre, Equipo, Puerto, Usuario, Contrasegna, Ruta, "Backup realizado correctamente")
        print(resultado)
  # Manejo de errores
  except Exception as Macana:
    print(f"Error en el programa principal: {Macana}")
