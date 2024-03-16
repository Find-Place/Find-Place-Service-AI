import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import webbrowser
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image


class Photo:
    def __init__(self, input_image_path) -> None:
        self.path = input_image_path
    

    def transform_embedding_vector(self):
        model = models.resnet50(weights='ResNet50_Weights.DEFAULT')
        model.eval()

        # 이미지를 로드하고 전처리
        transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
        
        image = transform(Image.open(self.path).convert("RGB")).unsqueeze(0)

        # 특징 추출
        with torch.no_grad():
            features = model(image)

        # 텐서를 리스트로 변환
        features_list = features.squeeze().tolist()

        return np.array([features_list])

    


