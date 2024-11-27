#!/usr/bin/python3

# cambiar el formato de la fecha y hora
import datetime

fecha_hora = datetime.datetime.now()
formato_fecha_hora = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
print(formato_fecha_hora)
