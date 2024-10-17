import requests
url = 'https://ip.smartproxy.com/json'
proxy = '102.129.210.92:12323'
# proxy = 'gate.smartproxy.com:15555'
username = '14a70624eb09e'
password = 'b5c02347c0'

proxies = {
    'http': f'http://{username}:{password}@{proxy}',
    'https': f'http://{username}:{password}@{proxy}'
}

response = requests.get(url, proxies=proxies)
print(response.json())