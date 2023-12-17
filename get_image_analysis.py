import base64, requests, os
from io import BytesIO
import cv2

# load env
from dotenv import load_dotenv
load_dotenv('.env')

def http_request(method, base_url, query_params=None, headers=None, json_body=None):
    try:
        if method in ('POST', 'PUT'):
            response = requests.post(base_url, params=query_params, headers=headers, json=json_body)

        elif method == 'GET':
            response = requests.get(base_url, headers=headers, params=query_params)
        
        status_code = response.status_code
        response_body = response.json() if response.headers.get('content-type') == 'application/json' else response.text

    except Exception as e:
        status_code = 504
        response_body = str(e.args)
    
    return status_code, response_body


print(os.getenv('AZURE_CV_ENDPOINT'))
print(os.getenv('AZURE_CV_KEY'))

image_path = 'images/resort.jpg'

# convert image file to cv2 format
image = cv2.imread(image_path)

# resize image using cv2
image = cv2.resize(image, (224, 224))

# convert cv2 image to base64
_, encode = cv2.imencode('.jpg', image)
image_base64 = base64.b64encode(encode)

# Decode base64 string back to bytes, convert bytes to file-like object
image_bytes = base64.b64decode(image_base64)
image_file = BytesIO(image_bytes)

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': os.getenv('AZURE_CV_KEY')
}
params = {'api-version': '2023-04-01-preview', 'features': 'denseCaptions'}
payload = {
    'file': image
}
r = requests.post(os.getenv('AZURE_CV_ENDPOINT'), headers=headers, params=params, data=image_file)
print(r.json())

captions = []
for caption in r.json()['denseCaptionsResult']['values']:
    captions.append(caption['text'])

print(captions)
print(' '.join(captions))
print(image_base64)