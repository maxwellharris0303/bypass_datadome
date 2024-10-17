from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium_driverless import webdriver

profile_directory = 'C:/Users/Administrator/AppData/Local/Temp/GoLogin/profiles/65d4d997df2388620b554954/Default'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--user-data-dir=' + profile_directory)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://example.com")

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://example.com")