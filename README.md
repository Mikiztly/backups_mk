# backups_mk
Programa en python para hacer backups de routers y sw Mikrotik

Modulos que se deben instalar para que funcione:
sudo apt install python3-pip
En Ubuntu 24.04 tuve que cambiar la configuracion de python:
python3 -m pip config set global.break-system-packages true

Despues de cambiar esa configuracion instalar todos los modulos:
pip install paramiko mysql-connector-python

pip install librouteros

Script de Cesar para cambiar los datos de los routers MK
https://github.com/cesarsalva91/NeMikroPy