import typing
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import asyncio
import re
import whisper  # Make sure you have the whisper library installed

# driver = webdriver.Chrome()

# driver.get("https://hermes.com")

async def download_audio(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    # 从响应中读取音频数据并写入临时文件
                    audio_data = await response.read()
                    tmp_file.write(audio_data)
                    # 获取临时文件的路径
                    tmp_file_path = tmp_file.name
                print("Audio file downloaded successfully.")
                return tmp_file_path
            else:
                print(f"Failed to download audio file: {response.status}")
                return None

async def solve_captcha(driver: typing.Union[Chrome, Target]):
    try:
        # noinspection PyTypeChecker
        iframe = await driver.find_element(By.XPATH, '//iframe', timeout=10)
        # Get the src attribute of the iframe
        iframe_src = await iframe.get_attribute('src')
        if iframe_src.startswith('https://geo.captcha-delivery.com/captcha/'):
            print('click')
            content = await iframe.content_document

            # click use audio captcha button
            captcha_audio_button = await content.find_element(By.ID, 'captcha__audio__button')
            await captcha_audio_button.click()

            # find audio element
            audio_element = await content.find_element(By.XPATH, '//audio[@class="audio-captcha-track"]')

            # find audio url
            audio_url = await audio_element.get_attribute('src')
            print('Audio src is: ' + audio_url)

            # download audio file
            audio_file_path = await download_audio(audio_url)
            print('Audio path is: ' + audio_file_path)

            # use whisper to transcribe speech to text
            model = whisper.load_model("base")
            result = model.transcribe(audio_file_path, fp16=False)
            matches = re.findall(r'\d', result['text'])
            solution = matches[-6:]
            print(solution)

            # enter solution
            for i in range(6):
                audio_input = (await content.find_elements(By.XPATH, '//input[@class="audio-captcha-inputs"]'))[i]
                await audio_input.click()  # Ensure the input field is focused
                # await asyncio.sleep(0.1)  # Add a small delay if necessary
                await audio_input.write(solution[i])

            print('Captcha Solved!')
            await asyncio.sleep(5)
        else:
            print('No captcha found!')
    except NoSuchElementException:
        print('No captcha found!')