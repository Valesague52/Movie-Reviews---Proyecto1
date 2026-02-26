import csv
import json
import os

# Crear carpeta si no existe
os.makedirs('movie/management/commands', exist_ok=True)

# Leer el archivo CSV
csv_file_path = 'data/movies_initial.csv'
json_file_path = 'movie/management/commands/movies.json'

# Crear lista para almacenar los datos
movies_data = []

# Leer CSV
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        movies_data.append(row)

# Guardar como JSON
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(movies_data, json_file, indent=2, ensure_ascii=False)

print(f"✅ Se convirtieron {len(movies_data)} películas a JSON")
print(f"📁 Archivo guardado en: {json_file_path}")