import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from Photo import Photo

folder_path = './embedding_vector/'

# 최대 유사도와 파일 이름 초기화
max_similarity = -1
max_similarity_file = ""

input_photo = Photo('example.png')
input_photo_vector = input_photo.transform_embedding_vector()


# 폴더 내의 모든 파일에 대해 반복
for i,filename in enumerate(os.listdir(folder_path)):
    if filename.endswith(".json"):
        # 파일 읽기
        with open(os.path.join(folder_path, filename), 'r') as file:
            print(filename)            
            # JSON 데이터 로드
            data_dict = json.load(file)
        
        # 이전 벡터 가져오기
        original_vector = np.array([data_dict.get("image_features", [])])
        
        # 코사인 유사도 계산
        similarity = cosine_similarity(input_photo_vector, original_vector)[0][0]

        # 최대 유사도 업데이트
        if similarity > max_similarity:
            max_similarity = similarity
            max_similarity_file = filename

# 결과 출력
print(f"가장 높은 코사인 유사도를 갖는 파일: {max_similarity_file}")
print(f"코사인 유사도: {max_similarity}")