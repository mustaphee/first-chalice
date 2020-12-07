from enum import unique
from platform import platform
from chalice import Chalice, BadRequestError
from chalicelib.utils.ResponseHelper import SuccessResponse
from os import environ as env
import uuid
import boto3
S3_CLIENT = boto3.resource('s3')

app = Chalice(app_name='first-chalice')
demo_db = {}

@app.route('/')
def index():
    return {'hello': 'world'}


# Create a unique S3 folder for a platform. This will
# be appended when generating direct upload policy link
@app.route('/create-directory', methods=['POST'])
def create_folder():
    # Collect platform id and platform name
 
    # Collect required fields
    fields = ['platform_name']

    req = app.current_request.json_body
    if not req:
        raise BadRequestError('You must send a `platform_name` in your request body')
    if not req.get('platform_name'):
        raise BadRequestError('You must send a `platform_name` in your request body')

    platform_name = req.get('platform_name')
    # Generate random id, concatenate with platform_name and images to make unique bucket id 
    random_id = uuid.uuid4()

    platform_folder = platform_name +'-'+ random_id.hex + '-images'

    # save folder
    demo_db[platform_name] = platform_folder
    return SuccessResponse('Platform folder created successfully', platform_folder)




# Upload a sample text file to S3. S3 bucket are really a flat folder concepts
# hence, creating a folder can be done by attaching a 'folder name' appended with
# forward slash mimic to folder structures

@app.route('/uploads/generate-link', methods=['POST'])
def generateUploadLink():
    # This uploads a file to a particular folder in a S3 bucket 
    # Assuming that there is a generic bucket for image in the env
    # and there's a saved directory in the db for this platform
    # This will generate a direct upload link to be used on client-side
    # to ensure upload to the particular 'folder' for the platform 

    # Collect required fields
    fields = ['filename', 'content_type', 'platform_name']

    req = app.current_request.json_body
    # TODO: Replace with Pydantic or a custom request body validator
    for field in fields:
        if not req.get(field):
            raise BadRequestError('You must send a {0} in your request body'.format(' ,'.join(fields)))

    filename = req.get('filename')
    content_type = req.get('content_type')
    folder = demo_db.get(req['platform_name'])

    if not folder:
        raise BadRequestError('Unknown platform name ' + req.get('platform_name'))

    try:
        presigned_post = S3_CLIENT.meta.client.generate_presigned_post(
            Bucket = env.get('BUCKET_ID'),
            Key = folder +'/'+filename,
            Fields = {"acl": "public-read", "Content-Type": content_type},
            ExpiresIn = 3600
        )
        return SuccessResponse('Upload policy generated successfully', presigned_post)
    except Exception as error:
        raise error


# Here we can use bucket to classify each platform's image uploads. While i dont 
# think this is an elegant way of doing this (too many bucket, for too litle content
# , i think), having a bucket for all images seems to be better
@app.route('/create-bucket', methods=['POST'])
def createS3Bucket():

    req = app.current_request.json_body
    # TODO: Replace with Pydantic or a custom request body validator
    if not req.get('platform_name'):
        raise BadRequestError('You must send a `platform_name` in your request body')

    platform_name = req.get('platform_name')
    # Generate random id, concatenate with platform_name and images to make unique bucket id 
    random_id = uuid.uuid4()

    bucket_name = platform_name +'-'+ random_id.hex + '-images'
    session = boto3.session.Session()
    try:
        response = S3_CLIENT.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
            'LocationConstraint': session.region_name})

        return SuccessResponse('Bucket created successfully', response.name)
    except Exception as error:
        raise error

