import boto3
from botocore.exceptions import ClientError
import base64
from flask import jsonify

ID = '<YOUR_COLLECTION_ID>'
AWS_KEY = '<YOUR_AWS_KEY>'
AWS_SECRET = '<YOUR_AWS_SECRET_KEY>'


def upload_face(name, image):
    # --- use this for named profiles in ~/.aws/config file
    dev = boto3.session.Session(profile_name='personal-aws')

    # --- or use keys
    # dev = boto3.session.Session(aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET)
    dev_client = dev.client('rekognition', region_name='ap-southeast-2')

    try:

        response = dev_client.index_faces(
            CollectionId=ID,
            Image={
                'Bytes': base64.b64decode(image),
            },
            ExternalImageId=name,
        )

        if len(response['FaceRecords']) == 0:
            return jsonify({'message': 'No face detected in photo!'})

        if response['FaceRecords'][0]['Face']['FaceId'] is not None:
            return jsonify({'message': 'Face Uploaded!'})

    except ClientError as e:

        return jsonify({'message': e.response['Error']['Message']})


def facial_recognition(image):
    # -- named profile
    dev = boto3.session.Session(profile_name='personal-aws')

    # dev = boto3.session.Session(aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET)
    dev_client = dev.client('rekognition', region_name='ap-southeast-2')

    try:
        response = dev_client.search_faces_by_image(
            CollectionId=ID,
            Image={
                'Bytes': base64.b64decode(image),
            },
            MaxFaces=1,
        )

        if len(response['FaceMatches']) > 1:
            return jsonify({'message': 'Too many faces found'})

        elif len(response['FaceMatches']) == 0:
            return jsonify({'message': 'No face match!'})

        elif len(response['FaceMatches']) == 1:
            return jsonify({
                'message': 'Face Found!',
                'id': response['FaceMatches'][0]['Face']['ExternalImageId'],
                'confidence': response['FaceMatches'][0]['Face']['Confidence']
            })

    except ClientError as e:

        return jsonify({'message': e.response['Error']['Message']})
