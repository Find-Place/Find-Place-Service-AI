import re
def extract_lat_lng_pan_to_filename(filename):
    pattern = r'lat_(?P<latitude>-?\d+\.\d+)_lng_(?P<longitude>-?\d+\.\d+)_pan_(?P<pan>-?\d+)_output'
        
    # 정규식을 사용하여 문자열에서 값 추출
    match = re.search(pattern, filename)
    
    # 추출된 값들을 변수에 저장
    result_dict = [ 
        float(match.group('latitude')), 
        float(match.group('longitude')), 
        int(match.group('pan'))
    ]
    return result_dict
