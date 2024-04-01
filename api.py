from model.Photo import Photo
from model.Db import Db
from http import HTTPStatus
from flask import Flask, request, jsonify
from utility.utilfunc import *

app = Flask(__name__)


@app.route('/sendImage', methods=['POST'])
def sendImage():
    try:
        image_file = request.files['sendingImage']
        path = "./uploads/uploaded_image.jpg"
        image_file.save(path)
    except:
        return jsonify({"error": "File is not transferd", "status": HTTPStatus.NOT_FOUND}), HTTPStatus.NOT_FOUND


    try:
        db = Db().database
        db.load()
    except Exception as e:
        print(e)
        return jsonify({"error": "Milvus database is not operating now", "status": HTTPStatus.INTERNAL_SERVER_ERROR}), HTTPStatus.INTERNAL_SERVER_ERROR

    uploading_photo = Photo("uploaded_image.jpg")

    result, latency = uploading_photo.search_similar_vector(db)
    for i in result:
        print(generate_google_maps_url(i['lat'], i['lng']))
    
    return jsonify({"data": result, "latency" : latency, "status": HTTPStatus.OK})

app.run(debug=True, host="localhost", port=5001)
