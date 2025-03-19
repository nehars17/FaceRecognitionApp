import boto3
from botocore.exceptions import ClientError
import base64
from flask import jsonify

COLLECTION_ID = 'clientverificationcollection'
AWS_KEY = ''
AWS_SECRET = ''

#command to create rekognition collection id
#aws rekognition create-collection --collection-id my-collection --region ap-southeast-2

def upload_face(name, image):
    # Initialize Rekognition client
    dev = boto3.session.Session(profile_name='default')
    dev_client = dev.client('rekognition', region_name='ap-southeast-1')

    try:
        response = dev_client.index_faces(
            CollectionId=COLLECTION_ID,
            Image={'Bytes': image},  # Assuming image is a byte stream
            ExternalImageId=name,
        )

        if not response.get('FaceRecords'):
            return {'message': 'No face detected in photo!'}

        return {'message': 'Face Uploaded!', 'FaceId': response['FaceRecords'][0]['Face']['FaceId']}

    except ClientError as e:
        return {'message': e.response['Error']['Message']}



def facial_recognition(id_image_bytes, live_image_bytes):
    # Initialize Rekognition client
    dev = boto3.session.Session(profile_name='default')
    dev_client = dev.client('rekognition', region_name='ap-southeast-2')

    try:
        # Compare images
        response = dev_client.compare_faces(
            SourceImage={"Bytes": id_image_bytes},
            TargetImage={"Bytes": live_image_bytes},
            SimilarityThreshold=95
        )

        if response.get("FaceMatches"):
            similarity = response["FaceMatches"][0]["Similarity"]
            return {'message': f"Match found! Similarity: {similarity}%"}
        else:
            return {'message': "No match found."}

    except ClientError as e:
        return {'message': e.response['Error']['Message']}
