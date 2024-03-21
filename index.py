print("Importing module...")
from model.Photo import Photo
from model.Db import Db
# print("import db_excute")
# from db_excute import create_db, drop, connect_db
import webbrowser

def generate_google_maps_url(lat, lng):

        # 위도 및 경도를 Google Maps의 URL 형식에 맞게 변환
        lat_str = f"{lat:.7f}"
        lng_str = f"{lng:.7f}"

        # URL 생성
        url = f"https://www.google.co.kr/maps/place/{lat_str}N%20{lng_str}E"
        return url

def open_url_in_default_browser(url):
    # 기본 브라우저로 URL 열기
    webbrowser.open(url)


# db = Db().database

# a = Db()
# a.cofig_schema()
# a.insert()
# a.index()

db = Db().database
print("connect db")
db.load()


print("uploading photo")
uploading_photo = Photo('jeongmun.png')

print("Start to serach most smilarilty vector")
lat,lng,pan = uploading_photo.search_similar_vector(db)


google_maps_url = generate_google_maps_url(lat,lng)
open_url_in_default_browser(google_maps_url)