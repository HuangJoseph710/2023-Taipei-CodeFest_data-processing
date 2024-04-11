import pandas as pd
import json

excel_file_path = '婦幼安全警示地點.xlsx'

excel_data = pd.read_excel(excel_file_path)

data_dict = excel_data.to_dict(orient='records')

final_data = {
  "data": [
    {
      "name": "",
      "data": [
        { "x": "北投區", "y": 0 },
        { "x": "士林區", "y": 0 },
        { "x": "內湖區", "y": 0 },
        { "x": "南港區", "y": 0 },
        { "x": "松山區", "y": 0 },
        { "x": "信義區", "y": 0 },
        { "x": "中山區", "y": 0 },
        { "x": "大同區", "y": 0 },
        { "x": "中正區", "y": 0 },
        { "x": "萬華區", "y": 0 },
        { "x": "大安區", "y": 0 },
        { "x": "文山區", "y": 0 }
      ]
    }
  ]
}


for record in data_dict:
    record['區'] = record['地點位置'][3:6]
    record['經度'] = round(eval(record['經緯度'].split(',')[1]),5)
    record['緯度'] = round(eval(record['經緯度'].split(',')[0]),5)
    for i in final_data['data'][0]['data']:
        if i['x'] == record['區']:
            i['y'] += 1
    

# file_path = '婦幼安全警示地點(輸出).json'
# with open(file_path, 'w', encoding='utf-8') as json_file:
#     json.dump(final_data, json_file, indent=4, ensure_ascii=False)

# print(f'JSON 文件已寫入到 {file_path}')

l =[]
i=0
for record in data_dict:
    i+=1
    d = {
         "type": "Feature",
         "id": f"{i}",
         "geometry": {
             "type": "Point",
             "coordinates": [record['經度'], record['緯度']]
         },
         "properties": {
             "dist": record['區'],
             "light_count": record['地點位置'][6:]
          }
        }
    l.append(d)
    


geojson_data = {
	"type": "FeatureCollection",
	"features": l
}

# 指定要寫入的 GeoJSON 文件路徑
file_path = '婦幼安全警示地點(經緯度).geojson'

# 使用 json.dump 將 GeoJSON 字典寫入到 GeoJSON 文件中，ensure_ascii 設置為 False
with open(file_path, 'w', encoding='utf-8') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=4, ensure_ascii=False)

print(f'GeoJSON 文件已寫入到 {file_path}')


