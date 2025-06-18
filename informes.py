import csv
import pymysql
import os

# Configuración de la conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'warnes',
    'cursorclass': pymysql.cursors.DictCursor
}


# Función para generar un archivo .csv que contiene un reporte de las cantidades por tipo
# de luminarias para cada Referencia
def sumario():

    sql = """
        SELECT p.id_referencia, r.distrito, r.descripcion, l.tipo, l.potencia, 
            count(pl.id_luminaria) as cantidad
        FROM poste p inner join poste_luminaria pl on p.id=pl.id_poste
        INNER JOIN luminaria l ON pl.id_luminaria = l.id
        INNER JOIN referencia r ON p.id_referencia = r.id
        GROUP BY p.id_referencia, pl.id_luminaria;
"""
    conexion = pymysql.connect(**DB_CONFIG)
    cursor = conexion.cursor()
    cursor.execute(sql)
    tabla = cursor.fetchall()
    cursor.close()
    conexion.close()
    id_ant = 0
    total = 0
    with open("tmp/Sumario.csv", "w") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([".", "..", "..."])
        for t in tabla:
            if t["id_referencia"] != id_ant:
                if id_ant > 0:
                    writer.writerow(["Total", "", total])
                    writer.writerow(["", "", ""])
                    total = 0
                if t["distrito"] is not None:
                    writer.writerow(
                        [f"Distrito {t["distrito"]} - {t["descripcion"]} ", "", ""])
                else:
                    writer.writerow([t["descripcion"], "", ""])
                writer.writerow(["Tipo", "Potencia", "Cantidad"])
            writer.writerow([t["tipo"], t["potencia"], t["cantidad"]])
            total += t["cantidad"]
            id_ant = t["id_referencia"]
        writer.writerow(["Total", "", total])


# Funcion que recibe los id's de uno o mas tipos de luminarias y un nombre de archivo .csv, para
# generar dicho archivo con los datos de Postes y Luminarias en base a los tipos de luminarias
# especificados. Adicionalmente añade la cantidad de Luminarias al nombre del archivo.
def rep_luminariaId(ids_luminarias, nom_arch):
    cant = 0
    conexion = pymysql.connect(**DB_CONFIG)
    cursor = conexion.cursor()
    with open(nom_arch, "w") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["id", "latitud", "longitud", "observacion",
                        "id_luminaria", "tipo", "potencia", "estado"])
        for id_lum in ids_luminarias:
            sql = """
                SELECT p.id, p.latitud, p.longitud, p.observacion, pl.id_luminaria, 
                    l.tipo, l.potencia, pl.estado
                FROM poste p
                INNER JOIN poste_luminaria pl ON p.id = pl.id_poste
                INNER JOIN luminaria l ON pl.id_luminaria = l.id
                WHERE pl.id_luminaria = %s
                ORDER BY p.id;
                """
            cursor.execute(sql, (id_lum,))
            pos_lum = cursor.fetchall()
            # conexion.commit()
            for pl in pos_lum:
                writer.writerow([pl["id"], pl["latitud"], pl["longitud"], pl["observacion"],
                                pl["id_luminaria"], pl["tipo"], pl["potencia"], pl["estado"]])
                cant += 1
    cursor.close()
    conexion.close()
    # print(f"{nom_arch}: {cant}")
    nom, ext = os.path.splitext(nom_arch)
    os.rename(nom_arch, f"{nom}-{cant}{ext}")


# sumario()
# rep_luminariaId([0, 1000, 2000, 2125, 3035, 3070,
#                 3150, 4020, 4040], "tmp/Varios.csv")
# rep_luminariaId([6000, 6040, 6050, 6060, 6100, 6150], "tmp/Led.csv")
# rep_luminariaId([1070], "tmp/Sodio70.csv")
# rep_luminariaId([1150], "tmp/Sodio150.csv")
rep_luminariaId([1250], "tmp/Sodio250.csv")
# rep_luminariaId([6035], "tmp/Led35.csv")
