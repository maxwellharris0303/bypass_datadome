import asyncio
import base64
import sys
import time
import traceback

from cdp_socket.exceptions import CDPError
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import random
import json


async def main():
    async with webdriver.Chrome(max_ws_size=2 ** 30) as driver:
        await driver.get("https://keliauk.urm.lt/en/consult_registration")
        await asyncio.sleep(3)
        iframes = await driver.find_element(By.CSS_SELECTOR, "iframe[title=\"Widget containing a Cloudflare security challenge\"]")
        iframe_document = await iframes.content_document

        pointer = await driver.current_pointer
        await pointer.move_to(500, 200, smooth_soft=60, total_time=0.5)
        await pointer.move_to(20, 50, smooth_soft=60, total_time=0.5)
        await pointer.move_to(8, 45, smooth_soft=60, total_time=0.5)
        await pointer.move_to(500, 200, smooth_soft=60, total_time=0.5)
        await pointer.move_to(166, 206, smooth_soft=60, total_time=0.5)
        await pointer.move_to(200, 205, smooth_soft=60, total_time=0.5)
        checkbox = await iframe_document.find_element(By.CSS_SELECTOR, "input[type=\"checkbox\"]")
        await checkbox.click(move_to=True)

        await asyncio.sleep(10)
        cookie_button = await driver.find_element(By.ID, "bf1f70e3eae8f503623659673d5dca1e9")
        await cookie_button.click()

        await asyncio.sleep(3)

        login_button_parent = await driver.find_element(By.CSS_SELECTOR, "button[class=\"btn outline-primary rounded-pill d-block d-lg-inline-block mb-3 px-4 btn-rounded-pill btn-depressed xlistener\"]")
        login_button = await login_button_parent.find_element(By.CSS_SELECTOR, "span[class=\"btn-label\"]")
        await login_button.click()

        await asyncio.sleep(5)

        captcha_img = await driver.find_element(By.CSS_SELECTOR, "img[id=\"captcha_img\"]")
        await captcha_img.screenshot('captchImage.png')
        print(captcha_img.screenshot_as_png)

        await asyncio.sleep(500)



asyncio.run(main())