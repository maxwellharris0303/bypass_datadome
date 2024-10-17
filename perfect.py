import json
import requests

# Load headers from the JSON file
with open('data.json', 'r') as json_file:
    headers_data = json.load(json_file)

headers = {}
for header_name, header_value in headers_data.items():
    headers[header_name] = header_value

headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Accept-Language'] = 'en-US,en;q=0.9'
headers['Sec-Fetch-Dest'] = 'empty'
headers['Sec-Fetch-Mode'] = 'cors'
headers['Sec-Fetch-Site'] = 'same-site'
# print(headers)

url = "https://bck.hermes.com/product?locale=fi_en&productsku=H394079T%252002"
response = requests.get(url, headers=headers)

# Check if the response is in JSON format
if response.headers.get('content-type') == 'application/json':
    # Parse the JSON response
    json_data = response.json()
    
    # Prettify the JSON
    prettified_json = json.dumps(json_data, indent=4)
    
    print(prettified_json)
else:
    print("Response is not in JSON format.")