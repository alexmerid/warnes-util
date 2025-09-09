import csv
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

# nomarch = "/media/alexander/Unidad_E/Warnes/Ejecucion/2025-06/000.csv"
nomarch = input("Ingrese el nombre del archivo CSV (con ruta completa): ")

with open(nomarch, "r", encoding="utf-8") as archivo:
    lector = csv.reader(archivo)
    next(lector)  # Saltar la primera línea si es un encabezado
    c = 0
    id_ant = 0
    for fila in lector:
        cursor.execute(
            "update poste_luminaria set fecha_desinst=%s where id_poste  = %s and fecha_desinst is NULL and codigo is NULL limit 1", (fila[4], fila[0]))
        cursor.execute("insert into poste_luminaria (id_poste, id_luminaria,estado,fecha_inst,codigo) values(%s, %s, 1, %s, %s)",
                       (fila[0], fila[1], fila[4], fila[2]))
        if id_ant != fila[0] and fila[3] != '':
            cursor.execute(
                "update poste set id_via=%s where id=%s", (fila[3], fila[0]))
        conexion.commit()
        id_ant = fila[0]
        c += 1
    print(f"Se actualizaron {c} filas")

cursor.close()
conexion.close()
