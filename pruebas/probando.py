#!/usr/bin/python3

# verificar que un archivo csv tenga los siguientes encabezados: servidor, usuario, contraseña, base datos
import csv
import sys

def verificar_encabezados_csv(ruta_archivo, encabezados_requeridos):
    try:
        with open(ruta_archivo, 'r', newline='', encoding='utf-8') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            encabezados = next(lector_csv)
            if encabezados == encabezados_requeridos:
                return True
            else:
                return f"Error: El archivo '{ruta_archivo}' no tiene los encabezados requeridos. Encabezados encontrados: {encabezados}"
    except FileNotFoundError:
        return f"Error: El archivo '{ruta_archivo}' no existe."
    except Exception as e:
        return f"Error al leer el archivo '{ruta_archivo}': {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python verificar_encabezados.py <ruta_del_archivo.csv>")
        sys.exit(1)

    ruta_archivo = sys.argv[1]
    encabezados_requeridos = ["servidor", "usuario", "contraseña", "base datos"]
    resultado = verificar_encabezados_csv(ruta_archivo, encabezados_requeridos)

    if isinstance(resultado, bool) and resultado:
        print("El archivo CSV tiene los encabezados requeridos.")
    else:
        print(resultado)
        sys.exit(1)
