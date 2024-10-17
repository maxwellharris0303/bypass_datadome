import requests

proxies = {
    'http': 'http://OzuZXN6ecc5OO0g7:zbG7gRivEglvRk3E@geo-dc.floppydata.com:10080',
    'https': 'http://OzuZXN6ecc5OO0g7:zbG7gRivEglvRk3E@geo-dc.floppydata.com:10080',
}

response = requests.get('https://httpbin.org/ip', proxies=proxies)


print(response.text)

