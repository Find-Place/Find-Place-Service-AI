
import time
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np


class Photo:
    pk_num = 0
    search_latency_fmt = "search latency = {:.4f}s"

    def __init__(self, filename) -> None:
        self.filename = filename
        filepath = f'./uploads/{self.filename}'

        model = models.resnet50(weights='ResNet50_Weights.DEFAULT')
        model.eval()

        # 이미지를 로드하고 전처리
        transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
        
        image = transform(Image.open(filepath).convert("RGB")).unsqueeze(0)

        # 특징 추출
        with torch.no_grad():
            features = model(image)

        # 텐서를 리스트로 변환
        features_list = features.squeeze().tolist()
        self.embedded_vector = np.array([features_list])
    


    def search_similar_vector(self, database, metric_type="COSINE"):        
        vectors_to_search = self.embedded_vector

        search_params = {
            "metric_type": metric_type,
            "params": {"nprobe": 10},
        }

        start_time = time.time()
        result = database.search(vectors_to_search, "embeddings", search_params, limit=5, output_fields=['lat', 'lng', 'pan'])
        end_time = time.time()

        location_info = []

        for hits in result:
            for i, hit in enumerate(hits):
                # print(f"hit: {hit}, lat field: {hit.entity.get('lat')}, lng field: {hit.entity.get('lng')}, pan field: {hit.entity.get('pan')}")
                # location_info.append(f"screenshot_lat_{hit.entity.get('lat')}_lng_{hit.entity.get('lng')}_pan_{int(hit.entity.get('pan'))}_output")
                loc_dic = {
                    "rank": i+1,
                    "lat" : hit.entity.get('lat'),
                    "lng" : hit.entity.get('lng'),
                    "pan" : hit.entity.get('pan')
                }
                location_info.append(loc_dic)
        latency = end_time - start_time
        latency_fm = self.search_latency_fmt.format(latency)
        print(latency_fm)

        return location_info, latency


