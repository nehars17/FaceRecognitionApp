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
    status = "Unverified"
    try:
        # Add print statements before every critical action
        print("Checking if both images are uploaded...")

        # Ensure both images are uploaded
        if "file" not in request.files or "id_image" not in request.files:
            print("No file part")
            return jsonify({"error": "Both live image and ID image are required"}), 400

        # Retrieve images from request
        print("Retrieving live and ID images...")
        live_image = request.files['file'].read()
        id_image_bytes = request.files['id_image'].read()

        print(f"Live Image: {len(live_image)} bytes")
        print(f"ID Image: {len(id_image_bytes)} bytes")

        # Perform face recognition
        print("Performing face recognition...")
        face_match = facial_recognition(id_image_bytes, live_image)

        # Perform text detection on ID image
        print("Detecting text in ID image...")
        detected_text = detect_text(id_image_bytes)
        print(f"Detected Text: {detected_text}")

        # Validate detected text with expected details
        print("Validating detected text...")
        count = len(details)
        for key in details:
            if details[key] in detected_text:
                count -= 1

        if count == 0 and 'Match found!' in face_match['message']:
            status = "Verified"

        print(f"Verification status: {status}")

        # Return structured JSON response
        print(face_match)
        return jsonify({
            "status": status,
            "face_match": face_match,
            "detected_text": detected_text
        })

    except Exception as e:
        print(f"Error in /compare: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
