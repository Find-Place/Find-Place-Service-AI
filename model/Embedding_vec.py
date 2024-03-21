import re, os, json
import numpy as np
from utilfunc import extract_lat_lng_span_to_filename

class Embedding_vec:

    def __init__(self, file_name) -> None:
        location_info = extract_lat_lng_span_to_filename(file_name)
        self.lat, self.lng, self.span = location_info
        
        folder_path = '../embedding_vector/'
        
        with open(os.path.join(folder_path, file_name), 'r') as file:         
            data_dict = json.load(file)
    
        old_vector = np.array([data_dict.get("image_features", [])])
        old_vector_arr = np.array([old_vector])


        self.embedding_vector = old_vector_arr[0][0]








