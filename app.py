from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # Import CORS
import base64
import os
from face import upload_face, facial_recognition
from ocr import *

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

details = {
   #details
}

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
# Function to decode Base64 to image
def decode_base64_to_image(base64_data):
    # Strip out the base64 metadata prefix if it exists
    base64_str = base64_data.split(',')[1] if ',' in base64_data else base64_data
    image_data = base64.b64decode(base64_str)
    return image_data

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

        # Decode base64 to raw bytes
        # live_image_bytes = base64.b64decode(live_image.split(',')[1])  # Remove data URL prefix if present
        # id_image_bytes = base64.b64decode(id_image.split(',')[1])


        # Perform face recognition
        print("Performing face recognition...")
        face_match = facial_recognition(live_image, id_image_bytes)

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
