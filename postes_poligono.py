# Programa que toma los puntos de un archivo .csv y genera otro archivo .csv con los puntos
# contenidos dentro de un polígono especificado en un archivo KML.
import csv
import xml.etree.ElementTree as ET
from shapely.geometry import Point, Polygon

# Archivos
archivo_poligono_kml = "tmp/Casco Viejo 2.kml"
archivo_puntos_csv = "tmp/PostesDistrito2.csv"
archivo_salida_csv = "tmp/PostesCascoViejo2.csv"

# Leer polígono desde archivo KML
NS = {"kml": "http://www.opengis.net/kml/2.2"}
tree = ET.parse(archivo_poligono_kml)
root = tree.getroot()
coords_text = root.find(".//kml:Polygon//kml:coordinates", NS).text.strip()
coords = [tuple(map(float, c.split(",")[:2])) for c in coords_text.split()]
poligono = Polygon(coords)

# Leer puntos CSV y filtrar
puntos_dentro = []

with open(archivo_puntos_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        lat = float(row["latitud"])
        lon = float(row["longitud"])
        punto = Point(lon, lat)
        if poligono.contains(punto):
            puntos_dentro.append(row)

# Guardar resultado en nuevo CSV
with open(archivo_salida_csv, mode='w', newline='', encoding='utf-8') as f_out:
    if puntos_dentro:
        writer = csv.DictWriter(f_out, fieldnames=puntos_dentro[0].keys())
        writer.writeheader()
        writer.writerows(puntos_dentro)
    else:
        print("⚠️ No se encontraron puntos dentro del polígono.")

print(f"✅ {len(puntos_dentro)} puntos guardados en '{archivo_salida_csv}'")
