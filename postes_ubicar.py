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


# Función para generar un archivo csv con la información de los postes de
# una referencia específica.
def postesRef(nomarch, ref_ini, ref_fin=0):
    conexion = pymysql.connect(**DB_CONFIG)
    cursor = conexion.cursor()
    if ref_fin > 0:
        cursor.execute(
            "SELECT id, latitud, longitud FROM poste WHERE id_referencia BETWEEN %s AND %s", (ref_ini, ref_fin))
    else:
        # Si no se especifica ref_fin, se toma solo la ref_ini
        cursor.execute(
            "SELECT id, latitud, longitud FROM poste WHERE id_referencia = %s", (ref_ini,))
    if cursor.rowcount == 0:
        print(f"⚠️ No se encontraron postes con la(s) referencia(s) especificada(s)")
        cursor.close()
        conexion.close()
        return
    postes = cursor.fetchall()
    with open(nomarch, "w") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(postes[0].keys())  # Escribir encabezados
        for poste in postes:
            writer.writerow(poste.values())
    cursor.close()
    conexion.close()


# Funcion para cambiar el id_referencia de los postes cuyos id están en un archivo csv.
def cambiarRef(nomarch, ref):
    conexion = pymysql.connect(**DB_CONFIG)
    cursor = conexion.cursor()
    with open(nomarch, "r") as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            id_poste = fila["id"]
            cursor.execute(
                "UPDATE poste SET id_referencia = %s WHERE id = %s", (ref, id_poste))
    conexion.commit()
    cursor.close()
    conexion.close()


postesRef("tmp/PostesDistrito6.csv", 6000, 6999)
# cambiarRef("tmp/PostesCascoViejo2.csv", 2003)
