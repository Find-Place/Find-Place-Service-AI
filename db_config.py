import time,os
from Embedding_vec import Embedding_vec
from Photo import Photo

import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

fmt = "\n=== {:30} ===\n"
search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = 16254, 1000
connections.connect("default", host="localhost", port="19530")

fields = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
    FieldSchema(name="lat", dtype=DataType.DOUBLE),
    FieldSchema(name="lng", dtype=DataType.DOUBLE),
    FieldSchema(name="pan", dtype=DataType.DOUBLE),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dim),
    
]

schema = CollectionSchema(fields, "picture_embedding has lat, lng, pan")

print(fmt.format("Create collection `picture_embedding`"))
picture_embedding = Collection("picture_embedding", schema, consistency_level="Strong")

################################################################################
# 3. insert data
# We are going to insert 3000 rows of data into `hello_milvus`
# Data to be inserted must be organized in fields.
#
# The insert() method returns:
# - either automatically generated primary keys by Milvus if auto_id=True in the schema;
# - or the existing primary key field from the entities if auto_id=False in the schema.

print(fmt.format("Start inserting entities"))
rng = np.random.default_rng(seed=19530)

lat_list = []
lng_list = []
pan_list = []
embedding_vector_list = []
folder_path = './embedding_vector/'
for i,filename in enumerate(os.listdir(folder_path)):
    if (i%100 == 0):
        print("Loading... : ", str(i)+f"/{num_entities}")
    
    vc = Embedding_vec(filename)
    lat_list.append(vc.lat)
    lng_list.append(vc.lng)
    pan_list.append(vc.pan)
    embedding_vector_list.append(vc.embedding_vector)

entities = [
    [str(i) for i in range(num_entities)],
    lat_list,
    lng_list,
    pan_list,
    embedding_vector_list,  # field random, only supports list
]

insert_result = picture_embedding.insert(entities)

picture_embedding.flush()
print(f"Number of entities in Milvus: {picture_embedding.num_entities}")  # check the num_entities


# collection 초기화
# collections = utility.list_collections()

# for collection in collections:
#     utility.drop_collection(collection)

################################################################################
# 4. create index
# We are going to create an IVF_FLAT index for picture_embedding collection.
# create_index() can only be applied to `FloatVector` and `BinaryVector` fields.
print(fmt.format("Start Creating index IVF_FLAT"))
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "COSINE",
    "params": {"nlist": 128},
}

picture_embedding.create_index("embeddings", index)


# index 삭제
# picture_embedding.release()
# picture_embedding.drop_index()

print(fmt.format("Start loading"))
picture_embedding.load()

# search based on vector similarity
print(fmt.format("Start searching based on vector similarity"))
vectors_to_search = Photo('./uploads/jeonjeong.jpg').transform_embedding_vector()

search_params = {
    "metric_type": "COSINE",
    "params": {"nprobe": 10},
}

start_time = time.time()
result = picture_embedding.search(vectors_to_search, "embeddings", search_params, limit=3, output_fields=['lat', 'lng', 'pan'])
end_time = time.time()

result_filename = []
for hits in result:
    for hit in hits:
        print(f"hit: {hit}, lat field: {hit.entity.get('lat')}, lng field: {hit.entity.get('lng')}, pan field: {hit.entity.get('pan')}")
        result_filename.append(f"screenshot_lat_{hit.entity.get('lat')}_lng_{hit.entity.get('lng')}_pan_{int(hit.entity.get('pan'))}_output")
print(search_latency_fmt.format(end_time - start_time))
print(result_filename)