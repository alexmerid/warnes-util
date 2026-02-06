import openpyxl
import pymysql

# Configuración de la conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'warnes',
    'cursorclass': pymysql.cursors.DictCursor
}

conexion = pymysql.connect(**DB_CONFIG)
cursor = conexion.cursor()

nomarch = input("Ingrese el nombre del archivo Excel (con ruta completa): ")

wb = openpyxl.load_workbook(nomarch)
hoja = wb.active

print("Filas = ", hoja.max_row)
i = 1
for fila in hoja.iter_rows(min_row=6, values_only=True):
    if fila[3] is not None:

        print(f"{i:>4}. {fila[0]:>6} {fila[3]:>8}")
        i += 1
