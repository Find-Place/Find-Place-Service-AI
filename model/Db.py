import os
from model.Embedding_vec import Embedding_vec
# from Photo import Photo
from pymilvus import (
    connections,
    db,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

class Db:
    # 16254, 1000
    def __init__(self, num_entities=16254, dim=1000) -> None:    
        self.num_entities, self.dim = num_entities, dim
        connections.connect("default", host="localhost", port="19530")
        has = utility.has_collection("picture_embedding")
        if has:
            self.database = Collection("picture_embedding")
            print(f"Number of entities in Milvus: {self.database.num_entities}")  # check the num_entities
        else:
            print("Create databsae first")


    # db schema 설정
    def cofig_schema(self):
        fields = [
            FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
            FieldSchema(name="lat", dtype=DataType.DOUBLE),
            FieldSchema(name="lng", dtype=DataType.DOUBLE),
            FieldSchema(name="pan", dtype=DataType.DOUBLE),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
        ]

        schema = CollectionSchema(fields, "picture_embedding has lat, lng, pan")
        picture_embedding = Collection("picture_embedding", schema, consistency_level="Strong")
        self.database = picture_embedding
    
    # 요소 삽입
    def insert(self):
        lat_list = []
        lng_list = []
        pan_list = []
        embedding_vector_list = []
        folder_path = './embedding_vector/'
        for i,filename in enumerate(os.listdir(folder_path)):
            if (i%100 == 0):
                print("Loading... : ", str(i)+f"/{self.num_entities}")
            print(filename)
            vc = Embedding_vec(filename)
            lat_list.append(vc.lat)
            lng_list.append(vc.lng)
            pan_list.append(vc.pan)
            embedding_vector_list.append(vc.embedding_vector)

        entities = [
            [str(i) for i in range(self.num_entities)],
            lat_list,
            lng_list,
            pan_list,
            embedding_vector_list,  # field random, only supports list
        ]

        insert_result = self.database.insert(entities)

        self.database.flush()
        print(f"Number of entities in Milvus: {self.database.num_entities}")

        return "Success to insert"

    # collection 초기화
    def reset_collection(self):
        collections = utility.list_collections()
        for collection in collections:
            utility.drop_collection(collection)

        return "Reset collection completely"

    # index 생성
    def index(self, column= "embeddings", idx_type="IVF_FLAT", metric_type="COSINE"):
        # "IVF_FLAT", "COSINE", "embeddings"
        index = {
            "index_type": idx_type,
            "metric_type": metric_type,
            "params": {"nlist": 128},
        }
        self.database.create_index(column, index)
    
    # 인덱스 삭제
    def delete_index(self):
        self.database.release()
        self.database.drop_index()


if __name__ == "__main__":
    from Embedding_vec import Embedding_vec
    # db에 삽입
    db = Db()
    db.cofig_schema()
    db.insert()
    db.index()

    