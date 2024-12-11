<h1 id="Script para realizar backup de Mikrotik">Script para realizar backup de Mikrotik</h1>

Programa realizado en python para hacer backups de routers y switch Mikrotik, realizado para automatizar las tareas de backup de Nubicom.

**Módulos a instalar**<br>
Se utilizan los módulos [paramiko](https://pypi.org/project/paramiko/) para conectarse por ssh a los equipos y [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) para guardar los resultados en una Base de Datos.

Ubuntu 24.04:
Primero instalar pip:
```shell
sudo apt install python3-pip
```
Cambiar la configuración de python:
```shell
python3 -m pip config set global.break-system-packages true
```

Después de cambiar esa configuración instalar todos los módulos:
```shell
pip install paramiko mysql-connector-python
```

<h2 id="Archivos a utilizar">Archivos a utilizar</h2>

Los archivos indispensables a utilizar son:
```shell
archivos_csv.py
db_server.txt
equipos.csv
maneja_db.py
maneja_mk.py
principal.py
```

<h3 id="db_server.txt">db_server.txt</h3>
En este archivo se guardan las credenciales para conectarse a un servidor MySQL, los datos que debe tener son:<br>

* host: Servidor de la base de datos.<br>
* user: Usuario de la base de datos.<br>
* password: Contraseña de la base de datos.<br>
* database: Nombre de la base de datos.<br>

Ejemplo:
```shell
host:localhost
user:usuario
password:Alg0_d1f1c1l
database:mikrotik_db
```

<h3 id="equipos.csv">equipos.csv</h3>
Este es un archivo de texto plano CSV que contiene información de los equipos para realizar el backup, los datos que debe tener son:<br>

* Nombre: Nombre del equipo.<br>
* Equipo: Dirección IP del equipo.<br>
* Puerto: Puerto del equipo<br>
* Usuario: Usuario para conectarse por ssh.<br>
* Contraseña: Contraseña para conectarse por ssh.<br>
* Cliente: Nombre del cliente propietario del equipo.<br>
* Ruta: Directorio donde se guardara el backup.<br>
* Mensaje: Mensaje a guardar en la base de datos si el backup es exitoso.<br>

Ejemplo:
```shell
Nombre,Equipo,Puerto,Usuario,Contrasegna,Cliente,Ruta,Mensaje
diego-lab,192.168.78.53,22,admin,admin,Nubicom,backups_NBC,OK
INC_ORN_ORNGNA,192.50.11.155,37893,ssh-bkps,Pa55w0rd,Sigar,backups_SIGAR,OK
```
Los valores se deben separar por comas **SIN** espacios.

<h3 id="principal.py">principal.py</h3>
Ese es el archivo que se ejecuta para realizar el backup, se deben pasar como argumento los dos archivos anteriores: servidor_db.txt y equipos.csv. Para programarlo en cron se puede crear la siguiente linea:<br><br>

```shell
00 01 * * *     python3 /home/dcasavilla/backups_mk/principal.py /home/dcasavilla/backups_mk/db_server.txt /home/dcasavilla/backups_mk/equipos.csv
```

Con esto se crean los backups a la 1:00 AM cada día y se guardan en la carpeta home del usuario, en este caso dcasavilla con la ruta especificada en el archivo equipos.csv, por ejemplo:<br>

```shell
/home/dcasavilla/backups_NBC
/home/dcasavilla/Sigar
```

Se puede ejecutar de forma manual (estando en la carpeta de los archivos) con el siguiente comando:
```shell
python3 principal.py db_server.txt equipos.csv
```

<h2 id="Carpeta html">Carpeta html</h2>
En esta carpeta hay unos archivos php que muestra en una pagina los resultados de realizar los backups en una tabla, el servidor tiene que tener una configuración LAMP para mostrar la pagina de forma correcta. Copiar los archivos en la carpeta<br><br>

```shell
/var/www/
```
