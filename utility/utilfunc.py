import re

def extract_lat_lng_pan_to_filename(filename):
    pattern = r'lat_(?P<latitude>-?\d+\.\d+)_lng_(?P<longitude>-?\d+\.\d+)_pan_(?P<pan>-?\d+)_output'
        
    # 정규식을 사용하여 문자열에서 값 추출
    match = re.search(pattern, filename)
    
    # 추출된 값들을 변수에 저장
    result_dict = {
        "lat": float(match.group('latitude')), 
        "lng" : float(match.group('longitude')), 
        "pan": int(match.group('pan'))
    } 
    return result_dict


def generate_google_maps_url(*coordinates):
    lat, lng = coordinates

    # 위도 및 경도를 Google Maps의 URL 형식에 맞게 변환
    lat_str = f"{lat:.7f}"
    lng_str = f"{lng:.7f}"

    # URL 생성
    url = f"https://www.google.co.kr/maps/place/{lat_str}N%20{lng_str}E"
    return url

