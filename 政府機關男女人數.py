import pandas as pd
import geopandas as gpd
import geocoder
import json
import pandas as pd
from shapely.geometry import LineString, Point, Polygon

   


excel_file_path = '政府單位男女人數.xlsx'


excel_data = pd.read_excel(excel_file_path)


data_dict = excel_data.to_dict(orient='records')

for record in data_dict:
    total = record['男性員工人數'] + record['女性員工人數']
    record['男性比例'] =round(record['男性員工人數']/total*100,2)
    record['女性比例'] = round(record['女性員工人數']/total*100,2)
    record['經度'] = round(eval(record['緯經度'].split(',')[1]),4)
    record['緯度'] = round(eval(record['緯經度'].split(',')[0]),4)
    
# print(data_dict)


#a.男女.json
male_total = 0
female_total = 0
for record in data_dict:
    male_total += record['男性員工人數']
    female_total += record['女性員工人數']
print(male_total, female_total)
final_data = {
	"data": [
		{
			"name": "男生人數",
			"data": [male_total]
		},
		{
			"name": "女生人數",
			"data": [female_total]
		}
	]
}

# file_path = '男女(輸出).json'
# with open(file_path, 'w', encoding='utf-8') as json_file:
#     json.dump(final_data, json_file, indent=4, ensure_ascii=False)

# print(f'JSON 文件已寫入到 {file_path}')


#b.空間資料

geo_list = []
i = 0
for record in data_dict:
    i += 1
    geo_dict = {
		"type": "Feature",
		"id": "atry0915",
		"geometry": {
			"type": "Point",
			"coordinates": [121.5436, 25.0261],
			"malePercentage":42.3
		}
	}
    geo_dict["id"] = f"{i}"
    geo_dict["geometry"]["coordinates"] = [record['經度'],record['緯度']]
    geo_dict["geometry"]["malePercentage"] = record['男性比例']
    geo_list.append(geo_dict)

geojson_data = {"type": "FeatureCollection"}
geojson_data["features"] = geo_list

# 指定要寫入的 GeoJSON 文件路徑
file_path = 'output.geojson'

# 使用 json.dump 將 GeoJSON 字典寫入到 GeoJSON 文件中，ensure_ascii 設置為 False
with open(file_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=4, ensure_ascii=False)

print(f'GeoJSON 文件已寫入到 {file_path}')