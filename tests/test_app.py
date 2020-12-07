from chalice.test import Client
from app import app
import json

def test_index():
    with Client(app) as client:
        response = client.http.get('/')
        assert response.json_body == {'hello': 'world'}
        assert response.status_code == 200

# Should not create, missing body
def test_dont_create_folder():
    with Client(app) as client:
        response = client.http.post('/create-directory', headers={ 'Content-Type': 'application/json' }, body= json.dumps({'unkown_key': 'what_not'}))
        assert response.status_code == 400
        assert response.json_body['Message'] == 'BadRequestError: You must send a `platform_name` in your request body'
        assert response.json_body['Code'] == 'BadRequestError'

# Should not generate, missing body
def test_dont_generate_link():
    with Client(app) as client:
        response = client.http.post('/uploads/generate-link', headers={ 'Content-Type': 'application/json' }, body= json.dumps({'unkown_key': 'what_not'}))
        assert response.status_code == 400
        assert response.json_body['Message'] == 'BadRequestError: You must send a filename ,content_type ,platform_name in your request body'
        assert response.json_body['Code'] == 'BadRequestError'

def test_create_folder():
    with Client(app) as client:
        response = client.http.post('/create-directory', headers={ 'Content-Type': 'application/json' }, body= json.dumps({'platform_name': 'test-platform'}))

        assert response.status_code == 200
        assert response.json_body['message'] == 'Platform folder created successfully'
        assert response.json_body['status'] == 'success'
        print(response.json_body['data'])
        assert response.json_body['data'].startswith('test-platform')
        assert response.json_body['data'].endswith('-images')
        assert len(response.json_body['data']) > 30

# def test_generate_folder():
#     with Client(app, stage_name='dev') as client:
#         response = client.http.post('/uploads/generate-link', headers={ 'Content-Type': 'application/json' }, body= json.dumps({'platform_name': 'test-platform', 'filename': 'image1.jpg', 'content_type':'jpg'}))
#         print(response.status_code)
#         print(response.body)
#         assert response.status_code == 200
#         assert response.json_body['message'] == 'Upload policy generated successfully'
#         assert response.json_body['status'] == 'success'
#         assert response.json_body['data']['fields']['Content-Type'] == 'jpg'



# def test_create_folder():
#     with Client(app) as client:
#         response = client.http.get('/create-directory')
#         assert response.json_body == {'hello': 'world'}