#!/bin/bash
# -*- ENCODING: UTF-8 -*-

# Configurar las variables
therouter="10.100.11.9"; # ip del router MK
thepassword="MXDjQARed4B6B8"; # Password del router MK
thename="R_SIGAR_BLVD"; # Nombre de router MK
theuser="ssh-blvd-bkps"; # Usuario de ingreso al router MK
theclient="Sigar"
theport="46254"; # Puerto de ingreso al router MK
theroute_a="/home/strongsystems/backups_MK_sigar/R_SIGAR_BLVD/"; # Ruta donde se descarga el BK
theroute_b="/home/strongsystems/backups_MK_sigar/R_SIGAR_BLVD"; # Ruta para cambiar Permisos
db_host="localhost"; # direccion DB
db_user="strongsystems"; # Usuario DB
db_pass="k8TY6&c7D4mW"; # Password DB
db_name="strong_db"; # DB

# Función para hacer la copia de seguridad
function backup_files {
  thefile=$(sshpass -p $thepassword ssh -o ConnectTimeout=10 $theuser@$therouter -p $theport ':local filename ([/system identity get name] . "-" . [:pick [/system clock get date] 7 11] . [:pick [/system clock get date] 0 3] . [:pick [/system clock get date] 4 6] . "-" . [:pick [/system clock get time] 0 2] . [:pick [/system clock get time] 3 5]); /export terse file=$filename; /system backup save dont-encrypt=yes name=($filename); put $filename' | tail -n 1 | tr -d '\r');
  sshpass -p $thepassword scp -P $theport -o ConnectTimeout=5 $theuser@$therouter:/"$thefile.backup" $theroute_a &&
  sshpass -p $thepassword scp -P $theport -o ConnectTimeout=5 $theuser@$therouter:/"$thefile.rsc" $theroute_a
}

# Realizar la copia de seguridad
backup_files

# Verificar el estado de salida del comando "scp" para determinar si la copia de seguridad se realizó correctamente
if [ $? -eq 0 ]; then
  status="OK"
else
  status="NO"
fi

# Permisos Directorios
chmod 754 $theroute_b
chown :backups $theroute_b

# Permisos Archivos
chown :backups $theroute_a*
chmod 754 $theroute_a*

# Conectarse a la base de datos y ejecutar una consulta SQL para insertar los datos
mysql -h $db_host -u $db_user -p$db_pass $db_name << EOF
INSERT INTO backup_logs (status, date, client, system_name) VALUES ('$status', NOW(), '$theclient', '$thename');
EOF
