print("Importing module...")
from model.Photo import Photo
from model.Db import Db
from http import HTTPStatus
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sendImage', methods=['POST'])
def sendImage():
    image_file = request.files['sendingImage']
    path = "./uploads/uploaded_image.jpg"
    image_file.save(path)
    
    db = Db().database
    db.load()

    uploading_photo = Photo("uploaded_image.jpg")

    result,latency = uploading_photo.search_similar_vector(db)
    print("result : ", result)
    return jsonify({"data": result, "latency" : latency, "status": HTTPStatus.OK})

app.run(debug=True, host="localhost",port=5001)