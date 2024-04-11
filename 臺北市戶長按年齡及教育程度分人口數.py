import pandas as pd
import json


excel_file_path = '臺北市戶長按年齡及教育程度分人口數.xlsx'


excel_data = pd.read_excel(excel_file_path)


data_dict = excel_data.to_dict(orient='records')

data=[]

for record in data_dict:
    if record['年份'] == '110年底':
        data.append(record)

education_data = {}

# 遍歷資料，分別計算不同教育程度別和性別的數量
for entry in data:
    education_level = entry['教育程度別']
    gender = entry['性別']
    total = entry['總計']

    # 如果教育程度別還沒有在字典中，則新增一個空字典
    if education_level not in education_data:
        education_data[education_level] = {}

    # 將數量存入對應的位置
    education_data[education_level][gender] = total

# 打印結果
male = []
female = []
for education_level, gender_data in education_data.items():
    #print(f"教育程度別: {education_level}")
    if education_level == '總計':
        continue

    for gender, total in gender_data.items():
        #print(f"性別: {gender}, 總計: {total}")
        
        if gender == '男':
            male.append(total)
        elif gender == '女':
            female.append(total)


final_data = {
	"data": [
		{
			"name": "男",
			"data": male
		},
		{
			"name": "女",
			"data": female
		}
	]
}


# file_path = '男女(教育程度).json'
# with open(file_path, 'w', encoding='utf-8') as json_file:
#     json.dump(final_data, json_file, indent=4, ensure_ascii=False)

# print(f'JSON 文件已寫入到 {file_path}')




#歷史資料
male = []
female = []

for record in data_dict:
    if record['教育程度別'] == "總計":
        data.append(record)
        print(record)
        d={}
        d["y"] = record['總計']
        d['x'] = f"{eval(record['年份'][:-2])+1911}-01-01T00:00:00Z"
        if record['性別'] == '男':
            male.append(d)
        elif record['性別'] == '女':
            female.append(d)



final_data = {
	"data": [
		{
			"name": "男",
			"data": male
		},
		{
			"name": "女",
			"data": female
		}
	]
}

file_path = '男女每年平均所得(歷史資料).json'
with open(file_path, 'w', encoding='utf-8') as json_file:
    json.dump(final_data, json_file, indent=4, ensure_ascii=False)

print(f'JSON 文件已寫入到 {file_path}')













