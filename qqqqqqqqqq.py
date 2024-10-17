from seleniumwire import webdriver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('start-maximized')
PROXY_USERNAME = "user-spo8thgt4t-sessionduration-30"
PROXY_PASSWORD = "7=52dyzzl8FOMfVafk"
seleniumwire_options = {
    'proxy': {
        'http': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@gate.visitxiangtan.com:10022',
        'verify_ssl': False,
    },
}
driver = webdriver.Chrome(
    options=chrome_options,
    seleniumwire_options=seleniumwire_options,
)

driver.get("https://httpbin.org/ip")