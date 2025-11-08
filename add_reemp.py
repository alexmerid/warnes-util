# Este programa permite modificar la tabla poste_luminaria para actualizar la columna
# reemp de las luminarias que han sido cargadas cuando no existía la columna reemp.
# Sólo afecta a las luminarias que pertenezcan a postes con una luminaria.

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

sql = """
SELECT id, id_poste 
FROM poste_luminaria  
WHERE reemp  IS NULL AND fecha_inst IS NOT NULL
ORDER BY id_poste;
"""
cursor.execute(sql)
resultados = cursor.fetchall()

c = 0
for fila in resultados:
    c += 1
    cursor.execute(
        "SELECT id FROM poste_luminaria WHERE id_poste = %s AND fecha_desinst is not null;", (fila['id_poste'],))
    id_reemp = cursor.fetchone()
    # print(fila, id_reemp['id'])
    cursor.execute(
        "UPDATE poste_luminaria SET reemp = %s WHERE id = %s", (id_reemp['id'], fila['id']))
    conexion.commit()
print(f"Se procesaron {c} luminarias")

cursor.close()
conexion.close()
