from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request
from PIL import Image
import perfect_test
import base64


url = "https://keliauk.urm.lt/en/consult_registration"

# options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")

driver = webdriver.Chrome()
driver.maximize_window() 
driver.get(url)
sleep(5)

iframes = driver.find_element(By.CSS_SELECTOR, "iframe[title=\"Widget containing a Cloudflare security challenge\"]")
iframe_document = iframes.content_document

pointer = driver.current_pointer
pointer.move_to(500, 200, smooth_soft=60, total_time=0.5)
pointer.move_to(20, 50, smooth_soft=60, total_time=0.5)
pointer.move_to(8, 45, smooth_soft=60, total_time=0.5)
pointer.move_to(500, 200, smooth_soft=60, total_time=0.5)
pointer.move_to(166, 206, smooth_soft=60, total_time=0.5)
pointer.move_to(200, 205, smooth_soft=60, total_time=0.5)
iframe_document.find_element(By.CSS_SELECTOR, "input[type=\"checkbox\"]").click(move_to=True)

sleep(7)
try:
    cookie_button = driver.find_element(By.ID, "bf1f70e3eae8f503623659673d5dca1e9")
    cookie_button.click()
except:
    sleep(4)
    try:
        cookie_button = driver.find_element(By.ID, "bf1f70e3eae8f503623659673d5dca1e9")
        cookie_button.click()
    except:
        pass
sleep(3)

try:
    login_button_parent = driver.find_element(By.CSS_SELECTOR, "button[class=\"btn outline-primary rounded-pill d-block d-lg-inline-block mb-3 px-4 btn-rounded-pill btn-depressed xlistener\"]")
    login_button = login_button_parent.find_element(By.CSS_SELECTOR, "span[class=\"btn-label\"]")
    login_button.click()
except:
    sleep(3)
    try:
        login_button_parent = driver.find_element(By.CSS_SELECTOR, "button[class=\"btn outline-primary rounded-pill d-block d-lg-inline-block mb-3 px-4 btn-rounded-pill btn-depressed xlistener\"]")
        login_button = login_button_parent.find_element(By.CSS_SELECTOR, "span[class=\"btn-label\"]")
        login_button.click()
    except:
        pass
sleep(4)

captcha_img = driver.find_element(By.CSS_SELECTOR, "img[id=\"captcha_img\"]")
driver.save_screenshot('captchaImage.png')

location = captcha_img.location
size = captcha_img.size

# Capture the screenshot of the element
driver.save_screenshot('screenshot.png')

# Crop the screenshot to the element's dimensions
left = int(location['x'])
top = int(location['y'])
right = int(location['x'] + size['width'])
bottom = int(location['y'] + size['height'])

screenshot = Image.open('screenshot.png')
element_screenshot = screenshot.crop((left, top, right, bottom))
element_screenshot.save('element_screenshot.png')

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        base64_data = base64.b64encode(image_bytes).decode("utf-8")
    return base64_data

image_path = "element_screenshot.png"
base64_data = image_to_base64(image_path)
captcha_text = perfect_test.solver_captcha(base64_data)


email_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder=\"info@pastas.lt\"]")
email_input.write("maneshimalikam@gmail.com")

pwd_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"password\"]")
pwd_input.write("EuroGlobe$2024")

captcha_input = driver.find_element(By.CSS_SELECTOR, "input[name=\"captcha\"]")
captcha_input.write(captcha_text)

submit_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"btn primary px-5 rounded-pill btn-success btn-rounded-pill btn-depressed xlistener\"]")
print(submit_button.text)
submit_button.click()

sleep(1000)