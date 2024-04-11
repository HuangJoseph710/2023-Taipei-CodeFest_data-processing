import pandas as pd
import json

excel_file_path = '台北市男女每年平均所得.xlsx'

excel_data = pd.read_excel(excel_file_path)

data_dict = excel_data.to_dict(orient='records')

all_average = []
male_average = []
female_average = []

for record in data_dict:
    print(record['年別'])
    record['年別'] = f"{eval(record['年別'][:-1])+1911}-01-01T00:00:00Z"
    d = {"y":record['所得收入總計'],"x":f"{record['年別']}"}
    if record['性別'] == '總平均':
        all_average.append(d)
    elif record['性別'] == '男':
        male_average.append(d)
    else:
        female_average.append(d)
    
final_data = {
	"data": [
		{
			"name": "總平均",
			"data": all_average
		},
		{
			"name": "男生平均",
			"data": male_average
		},
		{
			"name": "女生平均",
			"data": female_average
		}
	]
}

file_path = '男女每年平均所得(輸出).json'
with open(file_path, 'w', encoding='utf-8') as json_file:
    json.dump(final_data, json_file, indent=4, ensure_ascii=False)

print(f'JSON 文件已寫入到 {file_path}')







