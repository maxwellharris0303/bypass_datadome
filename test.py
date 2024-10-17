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


async def on_request(params, global_conn):
    url = params["request"]["url"]
    method = params["request"]["method"]
    print(params)
    print("=========================")
    if "product?" in url and method == "GET":
        headers = params["request"]["headers"]
        print("=========================")
        headers['Host'] = 'bck.hermes.com'
        for header_name, header_value in headers.items():
            print(f"'{header_name}' : '{header_value}'")
        print("=========================")
        with open('data.json', 'w') as json_file:
            json.dump(headers, json_file)
        
    _params = {"requestId": params['requestId']}
    if params.get('responseStatusCode') in [301, 302, 303, 307, 308]:
        # redirected request
        print("QQQQQQQ")
        # return await global_conn.execute_cdp_cmd("Fetch.continueResponse", _params)
    else:
        try:
            body = await global_conn.execute_cdp_cmd("Fetch.getResponseBody", _params, timeout=1)
        except CDPError as e:
            if e.code == -32000 and e.message == 'Can only get response body on requests captured after headers received.':
                # print(params, "\n", file=sys.stderr)
                traceback.print_exc()
                await global_conn.execute_cdp_cmd("Fetch.continueResponse", _params)
            else:
                raise e
        else:
            start = time.perf_counter()
            body_decoded = base64.b64decode(body['body'])

            # modify body here

            body_modified = base64.b64encode(body_decoded).decode("ascii")
            fulfill_params = {"responseCode": 200, "body": body_modified, "responseHeaders": params["responseHeaders"]}
            fulfill_params.update(_params)
            if params["responseStatusText"] != "":
                # empty string throws "Invalid http status code or phrase"
                fulfill_params["responsePhrase"] = params["responseStatusText"]

            _time = time.perf_counter() - start
            if _time > 0.01:
                # print(f"decoding took long: {_time} s")
                aaa = "sdf"
            await global_conn.execute_cdp_cmd("Fetch.fulfillRequest", fulfill_params)
            # print("Mocked response", url)


async def main():
    async with webdriver.Chrome(max_ws_size=2 ** 30) as driver:
        driver.base_target.socket.on_closed.append(lambda code, reason: print(f"chrome exited"))

        global_conn = driver.base_target
        await global_conn.execute_cdp_cmd("Fetch.enable",
                                          cmd_args={"patterns": [{"requestStage": "Response", "urlPattern": "*"}]})
        await global_conn.add_cdp_listener("Fetch.requestPaused", lambda data: on_request(data, global_conn))

        await driver.get("https://www.worten.pt")
        await asyncio.sleep(3000)
        cookie_button = await driver.find_element(By.CSS_SELECTOR, "button[id=\"onetrust-accept-btn-handler\"]")
        await cookie_button.click()
        await asyncio.sleep(2)
        
        login_button = await driver.find_element(By.CSS_SELECTOR, "span[class=\"mc-header-log-in__text\"]")
        await login_button.click()

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

        await asyncio.sleep(3000)
        input_email = await driver.find_element(By.CSS_SELECTOR, "input[id=\"user-account\"]")
        await input_email.write("example3423@gmail.com")
        await asyncio.sleep(1.5)
        continue_button = await driver.find_element(By.CSS_SELECTOR, "button[id=\"submit-button\"]")
        await continue_button.click()

        await asyncio.sleep(3)
        input_password = await driver.find_element(By.CSS_SELECTOR, "input[id=\"pwdInputInLoginDialog\"]")
        await input_password.write("sdfgert345dfst@$#wertg234")

        register_button = await driver.find_element(By.CSS_SELECTOR, "button[id=\"submit-button\"]")
        await register_button.click()

        await asyncio.sleep(5)
        login_button = await driver.find_element(By.CSS_SELECTOR, "div[class=\"_1MI18fma _2eKJ81QH _2PffkKmv\"]")
        await login_button.click()



        await asyncio.sleep(1000)

        page_height_driver = await driver.execute_script("return document.documentElement.clientHeight")
        page_width_driver = await driver.execute_script("return document.documentElement.clientWidth")
        print(page_height_driver, page_width_driver)

        # print(page_height_driver, page_width_driver)

        pointer = await driver.current_pointer
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
        try:
            accept_cookies_button = await driver.find_element(By.CSS_SELECTOR, "button[id=\"onetrust-accept-btn-handler\"]")
            await accept_cookies_button.click(move_to=True)
        except:
            pass
        menu_button = await driver.find_element(By.CSS_SELECTOR, "nav[aria-label=\"Navigation menu\"]")
        await menu_button.click(move_to=True)
        await asyncio.sleep(5)
        list_element = await driver.find_element(By.CSS_SELECTOR, "li[class=\"menu-list-item ng-star-inserted\"]")
        await list_element.click(move_to=True)
        await asyncio.sleep(3)
        ul_element = await driver.find_element(By.TAG_NAME, "h-menu-secondary-entry")
        await ul_element.click(move_to=True)
        await asyncio.sleep(3)
        link = await driver.find_element(By.TAG_NAME, "h-menu-link")
        await link.click(move_to=True)
        await asyncio.sleep(7)
        product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
        await product.click(move_to=True)
        await asyncio.sleep(7)
        try:
            add_to_cart_button = await driver.find_element(By.CSS_SELECTOR, "button[data-testid=\"Add to cart\"]")
        except:
            await asyncio.sleep(7)
            product = await driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]")
            await product.click(move_to=True)

        while True:
            # time.sleep(10) # no. cloudflare would hang
            await asyncio.sleep(120)

            pointer = await driver.current_pointer
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
            await pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))

            partner_products_element = await driver.find_element(By.CSS_SELECTOR, "h-product-page-grid[id=\"product-page-cross-sell-perfect-partner\"]")
            partner_products = await partner_products_element.find_elements(By.TAG_NAME, "li")
            print(len(partner_products))
            await partner_products[random.randint(0, len(partner_products) - 1)].click(move_to=True)
            print("new product")


asyncio.run(main())