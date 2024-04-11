import geocoder

# 要查詢的經緯度
latitude = 25.05266
longitude = 121.52039

# 使用 geocoder.arcgis 進行反向地理編碼
location = geocoder.arcgis([latitude, longitude], method='reverse')

# 打印反向地理編碼結果
print("Address:", location.address[3:6])
