import capsolver
import os
import base64

import requests
import json



# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         image_bytes = image_file.read()
#         base64_data = base64.b64encode(image_bytes).decode("utf-8")
#     return base64_data

# image_path = "element_screenshot.png"
# base64_data = image_to_base64(image_path)
# print(base64_data)

def solver_captcha(base64_data):
    url = 'https://api.capsolver.com/createTask'
    headers = {
        'Host': 'api.capsolver.com',
        'Content-Type': 'application/json'
    }

    data = {
    "clientKey": "CAI-CA8F5D78B888FEB049BE5444950CAA9F",
    "task": {
        "type": "ImageToTextTask",
        "websiteURL": "https://keliauk.urm.lt/en/user/login",
        "module": "common",
        "body": base64_data
    }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print the response
    return response.json()['solution']['text']