import boto3
from botocore.exceptions import ClientError

# Initialize Rekognition client

rekognition_client = boto3.client('rekognition', region_name='ap-southeast-2')  # Use your desired region

def detect_text(image_bytes):
    try:
        # Call Rekognition's DetectText API
        response = rekognition_client.detect_text(
            Image={'Bytes': image_bytes}
        )

        # Extract and display detected text
        detected_text = []
        for item in response['TextDetections']:
            detected_text.append(item['DetectedText'])

        return detected_text

    except ClientError as e:
        return f"Error: {e.response['Error']['Message']}"

# Example usage
if __name__ == "__main__":
    # Read the image file
    with open("ID.png", "rb") as image_file:
        image_bytes = image_file.read()

    # Detect text in the image
    text = detect_text(image_bytes)
    print("Detected Text:", text)