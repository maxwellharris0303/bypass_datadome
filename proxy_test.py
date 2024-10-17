import requests

# proxies = {
#     'http': 'http://brd-customer-hl_541e29d0-zone-residential_proxy1-country-us-session-c7d7c6a79d737275b2ac-const:b6wj9r5p2wqi@brd.superproxy.io:22225',
#     'https': 'http://brd-customer-hl_541e29d0-zone-residential_proxy1-country-us-session-c7d7c6a79d737275b2ac-const:b6wj9r5p2wqi@brd.superproxy.io:22225',
# }

# response = requests.get('https://httpbin.org/ip', proxies=proxies)


# print(response.text)



# proxies = {
#     'http': 'http://sp0m4mdxe7:t=JeJzm5CXn253bxcp@us.smartproxy.com:10009',
#     'https': 'http://sp0m4mdxe7:t=JeJzm5CXn253bxcp@us.smartproxy.com:10009'
# }

# response = requests.get('https://httpbin.org/ip', proxies=proxies)
# # gate.visitxiangtan.com:10000

# print(response.text)


import requests
url = 'https://ip.smartproxy.com/json'
proxy = '89.42.81.219:12323'
# proxy = 'gate.smartproxy.com:15555'
username = '14a51f7dce1cf'
password = 'e041b7ba43'

proxies = {
    'http': f'http://{username}:{password}@{proxy}',
    'https': f'http://{username}:{password}@{proxy}'
}

response = requests.get(url, proxies=proxies)
print(response.json())