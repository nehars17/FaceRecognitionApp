from flask import Flask, request, render_template, jsonify
import base64
import os
from face import upload_face, facial_recognition
from ocr import *
UPLOAD_FOLDER = '/static/img/'

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '<SOMETHING_SUPER_SECRET>'


details={"name":"NEHA D/O RAM SINGASAN", "Date of birth":"07-07-2003", "Country": "SINGAPORE", "Sex":"F"}

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        data = request.json  # Expecting JSON data
        if "file" not in data or "name" not in data:
            return jsonify({'message': 'Missing file or name'}), 400

        # Extract and decode image
        image_data = base64.b64decode(data['file'].split(',')[1])
        name = data['name'].replace(" ", "")

        response = upload_face(name=name, image=image_data)
        return jsonify(response)

    except Exception as e:
        return jsonify({'message': f"Error: {str(e)}"}), 500


@app.route('/compare', methods=['POST'])
def compare_image():
    status="unverified"
    try:
        data = request.json
        if "file" not in data:
            return jsonify({'message': 'Missing file'}), 400

        live_image = base64.b64decode(data['file'].split(',')[1])

        with open("sg-nric.jpg", "rb") as id_file:
            id_image_bytes = id_file.read()

        response = facial_recognition(id_image_bytes, live_image)
        response2 = detect_text(id_image_bytes)
        print(response2)
        count = len(details)
        for key in details:
            if details[key] in response2:
                count-=1

        if count==0:
            status="details verified"
        print(status)
        return jsonify(response)

    except Exception as e:
        print(f"Error in /compare: {e}")  # Log the error
        return jsonify({'message': f"Error: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True)
