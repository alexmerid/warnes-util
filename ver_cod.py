# Programa para verificar la correlatividad de los códigos de luminarias.
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

cursor.execute(
    "SELECT * FROM poste_luminaria WHERE  codigo LIKE 'A%' AND fecha_inst <= '2026-02-25' ORDER BY poste_luminaria.codigo")
c_ant = 0
codigo_anterior = ""
fila = cursor.fetchone()
while fila:
    c = int(fila['codigo'][2:7])
    if c_ant != c - 1:
        print(f"{codigo_anterior} - {fila['codigo']}")
    c_ant = c
    codigo_anterior = fila['codigo']
    fila = cursor.fetchone()

cursor.close()
conexion.close()
