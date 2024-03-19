import re, os, json
import numpy as np

class Embedding_vec:

    def __init__(self, file_name) -> None:
        pattern = r'lat_(?P<latitude>-?\d+\.\d+)_lng_(?P<longitude>-?\d+\.\d+)_pan_(?P<pan>-?\d+)_output'
        
        # 정규식을 사용하여 문자열에서 값 추출
        match = re.search(pattern, file_name)
        
        # 추출된 값들을 변수에 저장
        self.lat = float(match.group('latitude'))
        self.lng = float(match.group('longitude'))
        self.pan = int(match.group('pan'))
        
        folder_path = '../embedding_vector/'
        
        with open(os.path.join(folder_path, file_name), 'r') as file:         
            data_dict = json.load(file)
    
        old_vector = np.array([data_dict.get("image_features", [])])
        old_vector_arr = np.array([old_vector])


        self.embedding_vector = old_vector_arr[0][0]








