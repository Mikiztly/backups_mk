#!/usr/bin/python3
"""
Creado por Mikiztly https://github.com/Mikiztly

Por ahora hace un backup del equipo que se paso con los parametros y descarga dos archivos ( .backup y .rsc) en la ruta especificada en el argumento "Ruta"
Los parametros se deben pasar como un diccionario donde las claves deben ser:
["Nombre", "Equipo", "Puerto", "Usuario", "Contrasegna", "Cliente", "Ruta"]
"""
# Importacion de librerias a utilizar
import os, paramiko, time

# Clase para la conexion ssh al equipo MK
class SSHConnector:
  def __init__(self, Equipo: str, Puerto: int, Usuario: str, Contrasegna: str):
    """ 
    Crea una conexion ssh con el equipo Mikrotik.
    Args:
      Equipo: La dirección IP o nombre de host del equipo remoto.
      Puerto: El puerto SSH (por defecto 22).
      Usuario: El nombre de usuario para la conexión SSH.
      Contrasegna: La contraseña para la conexión SSH.
    Devuelve:
      Si se realizó correctamente el backup devuelve True.
      Si hay algún error devuelve un mensaje de error con la descripción del mismo.
     """
    self.hostname = Equipo
    self.port = Puerto
    self.username = Usuario
    self.password = Contrasegna
    self.client = None

    # Se establece la conexion ssh
  def Conecta_ssh(self):
    """ 
    Crea una conexion ssh con el equipo Mikrotik.
     """
    try:
      self.client = paramiko.SSHClient()
      self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      self.client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password, look_for_keys=False)
      return True
    # Las credenciales estan mal
    except paramiko.AuthenticationException as Macana:
      return f"Error de autenticación ssh: {Macana}"
    # Error de ssh
    except paramiko.SSHException as Macana:
      return f"Error de conexión ssh: {Macana}"
    # Error no controlado
    except Exception as Macana:
      return f"Error no controlado: {Macana}"

  # Crea una conexion sftp para manipular archivos
  def Conecta_sftp(self):
    if self.client:
      return self.client.open_sftp()
    else:
      return None

  # Si existe una conexion se cierra
  def Cierra_Conexiones(self):
    """
    Cierra la conexión ssh y sftp
    """
    try:
      if self.client:
        self.client.close()
      return True
    # Error no controlado
    except Exception as Macana:
      return f"Error no controlado: {Macana}"

# Clase para crear un backup del equipo MK
class BackupCreator:
  def __init__(self, ssh_client, Archivo_bkp: str):
    """ 
    Crea un backup de la configuracion de un equipo Mikrotik.
    Args:
      ssh_client: El cliente ssh para la conexión.
      Archivo_bkp: El nombre del archivo de backup a crear.
    Devuelve:
      Si se realizó correctamente el backup devuelve True.
      Si hay algún error devuelve un mensaje de error con la descripción del mismo.
    """
    self.ssh_client = ssh_client
    self.backup_name = Archivo_bkp

  def Crea_Backup(self):
    """ 
    Bace un backup del equipo Mikrotik, el resultado es la creacion de dos arvhios .backup y .rsc con el nombre establecido en la variable "Archivo_bkp"
     """
    try:
      # Crea el backup utilizando variables (stdin, stdout, stderr) para capturar si ocurren errores
      stdin, stdout, stderr = self.ssh_client.exec_command(f"/system backup save dont-encrypt=yes name={self.backup_name}")
      Macana = stderr.read().decode()
      # Si ocurrio algun error lo informo
      if Macana:
        raise Exception(f"Error al realizar el backup: {Macana}")
      # Pausa 2 segundos
      time.sleep(2)
      stdin, stdout, stderr = self.ssh_client.exec_command(f"/export file={self.backup_name}")
      Macana = stderr.read().decode()
      # Si ocurrio algun error lo informo
      if Macana:
        raise Exception(f"Error al realizar el backup: {Macana}")
      # Pausa 2 segundos
      time.sleep(2)
      # Si se hace correctamente el backup devuelvo True
      return True
    # Error no controlado
    except Exception as Macana:
      return f"Error no controlado: {Macana}"

class BackupDownloader:
  def __init__(self, Cliente_sftp, Archivo_bkp: str, Ruta: str):
    """ 
    Descarga los archivos creados al hacer el backup del equipo Mikrotik.
    Args:
      Cliente_sftp: Una conexion establecida por ssh realizada con la clase SSHConnector.
      Archivo_bkp: el nombre del archivo de backup a crear.
      Ruta: La carpeta del servidor donde se copiaran los archivos.
    Devuelve:
      Si se realizó correctamente el backup devuelve True
      Si hay algún error devuelve un mensaje de error con la descripción del mismo
     """
    self.sftp_client = Cliente_sftp
    self.remote_path = Ruta
    self.archivo = Archivo_bkp

  def download_backup(self):
    try:
      for Ext in [".backup", ".rsc"]:
        remote_file = self.remote_path + "/" + self.archivo + Ext
        local_file = self.archivo + Ext
        self.sftp_client.get(local_file, remote_file)
        # Pausa 2 segundos
        time.sleep(2)
      # Si se hace correctamente el backup devuelvo True
      return True
    # Error no controlado
    except Exception as Macana:
      return f"Error no controlado: {Macana}"
class BackupCleaner:
  """ 
  Limpia los archivos .backup y .rsc del equipo Mikrotik.
   """
  # Borrar todos los archivos .backup y .rsc del equipo mikrotik
  def __init__(self, ssh_client, sftp_client):
    self.ssh_client = ssh_client
    self.sftp_client = sftp_client

  def Busca_Backups(self):
    try:
      # Lista archivos en el directorio actual
      Archivos = self.sftp_client.listdir(path='.')
      # Guado solo los archivos .backup y .rsc para despues borrarlos
      """ for Lista in Archivos:
        if Lista.endswith(".backup") or Lista.endswith(".rsc"):
          Lista_Borrar.append(Lista) """
      Lista_Borrar = [Lista for Lista in Archivos if Lista.endswith(".backup") or Lista.endswith(".rsc")]
      # Backups = [Lista for Lista in Archivos if Lista.endswith(".backup", ".rsc")]
      return Lista_Borrar
    except Exception as Macana:
      return f"Error listando los archivos: {Macana}"

  def Limpia_Backups(self):
    try:
      # Obtengo los archivos a borrar
      Borrar = self.Busca_Backups()
      # Chequea que haya archivos para borrar
      if Borrar:
        # Se borran uno a uno los archivos
        for Archivo in Borrar:
          self.ssh_client.exec_command(f"rm {Archivo}")
          # Pausa 2 segundos
          time.sleep(2)
      return True
    except Exception as Macana:
      return f"Error limpiando archivos: {Macana}"

def Backup_MK(Nombre: str, Equipo: str, Puerto: int, Usuario: str, Contrasegna: str, Ruta: str, Archivo_bkp: str, Mensaje: str):
  """
  Crea un backup en el equipo Mikrotik, lo descarga y limpia los archivos remotos.
  Args:
    Nombre: El nombre del equipo.
    Equipo: La dirección IP o nombre de host del servidor remoto.
    Puerto: El puerto SSH (por defecto 22).
    Usuario: El nombre de usuario para la conexión SSH.
    Contrasegna: La contraseña para la conexión SSH.
    Ruta: La carpeta del servidor donde se copiaran los archivos.
    Archivo_bkp: el nombre del archivo de backup a crear
    Mensaje: Mensaje a devolver si se realiza bien el backup
  Devuelve:
    Si se realizó correctamente el backup devuelve el mensaje pasado como el argumento "Mensaje"
    Si hay algún error devuelve un mensaje de error con la descripción del mismo
  """
  try:
    Ruta_Completa = os.getcwd() + "/" + Ruta + "/" + Nombre
    if not os.path.exists(Ruta_Completa):
      os.makedirs(Ruta_Completa)
    # Se crea una conexion
    Conector = SSHConnector(Equipo, Puerto, Usuario, Contrasegna)
    Conexion_Result = Conector.Conecta_ssh()
    # Si no se realiza la conexion devuelvo el error
    if not Conexion_Result:
      return Conexion_Result
    # Abro el cliente ssh
    Cliente_ssh = Conector.client
    # Crea el backup
    Backup = BackupCreator(Cliente_ssh, Archivo_bkp)
    Backup_Result = Backup.Crea_Backup()
    # Si no se realiza el backup devuelvo el error
    if not Backup_Result == True:
      return Backup_Result
    # #Llamada a la función para obtener el cliente sftp
    Cliente_sftp = Conector.Conecta_sftp()
    # Descarga de archivos
    Descarga = BackupDownloader(Cliente_sftp, Archivo_bkp, Ruta_Completa)
    Descarga_Result = Descarga.download_backup()
    # Si no puede descargar los archivos devuelvo el error
    if not Descarga_Result:
      return Descarga_Result
    # Limpio los backups
    Limpiar = BackupCleaner(Cliente_ssh, Cliente_sftp)
    Limpiar_Result = Limpiar.Limpia_Backups()
    # Si no puede limpiar los archivos devuelvo el error
    if not Limpiar_Result:
      return Limpiar_Result
    # Cierro las conexiones
    Cierra_ssh = Conector.Cierra_Conexiones()
    if not Cierra_ssh:
      return Cierra_ssh
    # Devuelvo el mensaje pasado como parametro por que salio todo bien
    return Mensaje
  # Hubo algun error al crear los directorios
  except OSError as Macana:
    return f"Error al crear directorios: {Macana}"
  # Error no controlado
  except Exception as Macana:
    return f"Error no controlado: {Macana}"
