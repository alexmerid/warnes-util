# Programa para la etapa de apmlificación.

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
# El archivo Excel tiene la siguiente estructura:
# id_poste, id_luminaria, codigo, id_via, fecha_inst, id_referencia, latitud, longitud, obs
wb = openpyxl.load_workbook(nomarch)
hoja = wb.active

print("\n------------------------------------------------------------")
# Verficar si los Codigos de luminarias no existen en la base de datos
existentes = []
observaciones = []
for fila in hoja.iter_rows(min_row=2, values_only=True):
    if fila[0] is None:
        continue
    print(f"{fila[0]}, {fila[1]}, {fila[2]}, {fila[3]}, {fila[4]:%Y-%m-%d}, {fila[5]}, {fila[6]}, {fila[7]}, {fila[8]}")
    # cursor.execute(
    #     "select count(*) as conteo from poste_luminaria where codigo = %s", (fila[2],))
    # resultado = cursor.fetchone()
    # if resultado['conteo'] > 0:
    #     existentes.append(fila[2])
    # cursor.execute(
    #     "SELECT id_poste FROM observacion WHERE id_poste  = %s", (fila[0],))
    # resultado = cursor.fetchone()
    # if resultado:
    #     observaciones.append((fila[0], f"{fila[4]:%Y-%m-%d}"))
if existentes:
    print("Los siguientes códigos ya existen en la base de datos:")
    print(existentes)
    raise ValueError(
        "Se encontraron Códigos duplicados. Proceso detenido.")
if observaciones:
    print("Los siguientes postes tienen observaciones que deben finalizarse:")
    print(observaciones)
