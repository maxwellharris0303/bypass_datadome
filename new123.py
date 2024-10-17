# from selenium_profiles.webdriver import Chrome
from selenium import webdriver
from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By  # locate elements
from seleniumwire import webdriver

from time import sleep


driver = webdriver.Chrome()

# get url
driver.get('https://www.cityline.com/')  # test fingerprint
sleep(5000)
