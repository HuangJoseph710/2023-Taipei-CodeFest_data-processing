import xml.etree.ElementTree as ET
import json
import geocoder

# 解析 KML 文件
tree = ET.parse('臺北市性別友善廁所地圖.kml')
root = tree.getroot()

# 假設 KML 文件使用標準的命名空間
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

# 提取座標名稱和座標點
placemarks = root.findall('.//kml:Placemark', namespaces=namespace)

all_data = []

for placemark in placemarks:
    d = {}

    # 提取座標名稱
    name_element = placemark.find('.//kml:name', namespaces=namespace)
    name = name_element.text if name_element is not None else None

    # 提取座標點
    coordinates_element = placemark.find('.//kml:coordinates', namespaces=namespace)
    coordinates = coordinates_element.text if coordinates_element is not None else None

    # 打印座標名稱和座標點
    print(f"Name: {name}, Coordinates: {coordinates}")
    d['name'] = name
    d['經度'] = round(float(coordinates.split(',')[0]),5)
    d['緯度'] = round(float(coordinates.split(',')[1]),5)
    location = geocoder.arcgis([d['緯度'], d['經度']], method='reverse')
    d['dist'] = location.address[3:6]
    all_data.append(d)

l =[]
i=0
for record in all_data:
    i+=1
    d = {
         "type": "Feature",
         "id": f"{i}",
         "geometry": {
             "type": "Point",
             "coordinates": [record['經度'], record['緯度']]
         },
         "properties": {
             "dist": record['dist'],
             "name": record['name']
          }
        }
    l.append(d)



geojson_data = {
	"type": "FeatureCollection",
	"features": l
}

# 指定要寫入的 GeoJSON 文件路徑
file_path = '臺北市性別友善廁所(經緯度).geojson'

# 使用 json.dump 將 GeoJSON 字典寫入到 GeoJSON 文件中，ensure_ascii 設置為 False
with open(file_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=4, ensure_ascii=False)

print(f'GeoJSON 文件已寫入到 {file_path}')
