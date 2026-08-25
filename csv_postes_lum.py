# Programa para generar un archivo .csv con la información de los postes y luminarias.
import pymysql
import csv

# Configuración de la conexión
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'warnes',
    'cursorclass': pymysql.cursors.DictCursor
}


# Función para generar el archivo .csv con la información de los postes y luminarias.
def postes_luminarias(ref_ini, ref_fin, nom_arch):
    query = """
        SELECT p.id AS id_poste, p.latitud, p.longitud, pl.id_luminaria, pl.codigo, pl.fecha_inst    
        FROM poste p INNER JOIN poste_luminaria pl ON p.id = pl.id_poste  
        WHERE p.id_referencia BETWEEN %s AND %s
        AND pl.fecha_desinst is null;
    """
    conexion = pymysql.connect(**DB_CONFIG)
    cursor = conexion.cursor()
    cursor.execute(query, (ref_ini, ref_fin))
    tabla = cursor.fetchall()
    cursor.close()
    conexion.close()
    with open(nom_arch, "w", encoding="utf-8-sig", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["Poste - Código", "Latitud", "Longitud",
                        "ID Luminaria", "Fecha Instalación"])
        for t in tabla:
            poste_codigo = (
                f"{t['id_poste']}: {t['codigo']}" if t["codigo"] is not None else str(t["id_poste"]))
            writer.writerow([poste_codigo, t["latitud"], t["longitud"],
                            t["id_luminaria"], t["fecha_inst"]])


postes_luminarias(2523, 2526, "tmp/D-02_023-026.csv")
