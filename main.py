from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep
import random



profile_directory = 'C:/Profile 555'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--user-data-dir=' + profile_directory)
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument("--disable-blink-features=VideoPlayback")
# chrome_options.add_argument('--headless=new')
driver = webdriver.Chrome(options=chrome_options)

# sku = input("Plesae input sku: ")
url = "https://wordpress.com"
# url = f"https://bck.hermes.com/product?locale=ca_en&productsku=H4E0102DAG432"
driver.get(url, wait_load=True)
# headers = driver.execute_script("""
#     var xhr = new XMLHttpRequest();
#     xhr.open('GET', arguments[0], false);
#     xhr.send(null);
#     return xhr.getAllResponseHeaders();
# """, url)

# print(headers)


# print(driver.get_cookie('x-xsrf-token'))

sleep(5000)

def mouse_move_action():

    page_height_driver = driver.execute_script("return document.documentElement.clientHeight")
    page_width_driver = driver.execute_script("return document.documentElement.clientWidth")

    # print(page_height_driver, page_width_driver)

    pointer = driver.current_pointer
    pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
    pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
    pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
    pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
    pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))
    pointer.move_to(random.uniform(50, page_width_driver - 50), random.uniform(50, page_height_driver - 50), smooth_soft=random.randint(40, 60), total_time=random.uniform(0.2, 0.5))

mouse_move_action()
menu_button = driver.find_element(By.CSS_SELECTOR, "nav[aria-label=\"Navigation menu\"]")
menu_button.click(move_to=True)
sleep(5)
mouse_move_action()
list_element = driver.find_element(By.CSS_SELECTOR, "li[class=\"nav-item has-sub-item\"]")
list_element.click(move_to=True)
sleep(3)
mouse_move_action()
ul_element = driver.find_element(By.CSS_SELECTOR, "ul[class=\"sub-nav expanded\"]")
ul_element.find_element(By.TAG_NAME, 'li').click(move_to=True)
sleep(3)
mouse_move_action()
driver.find_element(By.CSS_SELECTOR, "a[class=\"link-menu\"]").click(move_to=True)
sleep(5)
try:
    mouse_move_action()
    driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]").click(move_to=True)
except:
    sleep(3)
    mouse_move_action()
    driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]").click(move_to=True)
driver.sleep(7)
try:
    description = driver.find_element(By.CSS_SELECTOR, "p[class=\"product-attribute-font-description\"]").text
    print(description)
    print(driver.find_element(By.CSS_SELECTOR, "script[id=\"hermes-state\"]").text)
except:
    try:
        mouse_move_action()
        driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]").click(move_to=True)
    except:
        sleep(3)
        mouse_move_action()
        driver.find_element(By.CSS_SELECTOR, "span[class=\"product-item-name\"]").click(move_to=True)
    driver.sleep(7)
    description = driver.find_element(By.CSS_SELECTOR, "p[class=\"product-attribute-font-description\"]").text
    print(description)
    print(driver.find_element(By.CSS_SELECTOR, "script[id=\"hermes-state\"]").text)

file_path = 'data.txt'
file = open(file_path, 'w', encoding='utf-8')

file.write(driver.find_element(By.CSS_SELECTOR, "script[id=\"hermes-state\"]").text)


file.close()


# start_time = datetime.now()
# formatted_time = start_time.strftime("%Y-%m-%d:%H:%M:%S")
# print(formatted_time)

# FILE_NAME = "followers_with_story.txt"
# initial_count = 0
# count_with_stories = 0
# total_stories_count = 0
# break_flag = 0
# count_request = 0
# while(True):
#     try:
#         followers_list = dialog_element.find_elements(By.CSS_SELECTOR, "div[class=\"x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3\"]")
#         followers_list = followers_list[initial_count:]
#         next_count = len(followers_list)
#         print(f"Followers count: {next_count}")

#         index = 0
#         for _ in range(next_count):
#             driver.execute_script("arguments[0].scrollIntoView(true);", followers_list[index])
#             try:
#                 follower_with_story = followers_list[index].find_element(By.CSS_SELECTOR, "div[class=\"_aarf _aarg\"]")

#                 follower_id = followers_list[index].find_element(By.CSS_SELECTOR, "span[class=\"_ap3a _aaco _aacw _aacx _aad7 _aade\"]").text
#                 print(follower_id)
#                 with open(FILE_NAME, 'a') as file:
#                     file.write(follower_id + ", ")

#                 # follower_with_story.click(move_to=True)
#                 # sleep(random.randint(2, 3))
#                 # count_with_stories += 1
#                 # print(f"Followers with story: {count_with_stories}")
            
#                 # next_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label=\"Next\"]", timeout=15)
#                 # stories = driver.find_elements(By.CSS_SELECTOR, "div[class=\"x1lix1fw xm3z3ea x1x8b98j x131883w x16mih1h x1iyjqo2 x36qwtl x6ikm8r x10wlt62 x1n2onr6\"]")
#                 # stories_count = len(stories)
#                 # total_stories_count += stories_count
#                 # print(f"Stories count: {stories_count}")
#                 # print(f"Total stories count: {total_stories_count}")
#                 # while(True):
#                 #     try:
#                 #         message_field = driver.find_element(By.TAG_NAME, "textarea")
#                 #         message_field.click()
#                 #         sleep(1)
#                 #         try:
#                 #             emot_icons = driver.find_elements(By.CSS_SELECTOR, "span[class=\"xcg35fi xo5v014 x1skpowl x1c2o835 xfczyey xsdrrl\"]")
#                 #             emot_icons[random.randint(0, len(emot_icons) - 1)].click()
#                 #         except:
#                 #             pass
#                 #         sleep(1)
#                 #         like_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label=\"Like\"]")
#                 #         like_button.click()
#                 #         sleep(0.2)
#                 #         next_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label=\"Next\"]")
#                 #         next_button.click()
#                 #         sleep(0.5)
#                 #     except:
#                 #         try:
#                 #             next_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label=\"Next\"]")
#                 #             next_button.click()
#                 #             sleep(0.5)
#                 #         except:
#                 #             break
#             except:
#                 pass
#             sleep(random.uniform(0.2, 0.5))
#             index += 1

#         initial_count += next_count
#         if next_count == 0:
#             break_flag += 1
#             if break_flag >= 5:
#                 break

#         print(initial_count)
        
#         sleep(3)
#         count_request += 1
#         print(f"\nCount request: {count_request}")

#         current_time = datetime.now()
#         passed_time = current_time - start_time
#         passed_time_to_seconds = int(passed_time.total_seconds())
#         print(f"Passed time: {passed_time_to_seconds}")
#         if count_request == 200:
#             if 3600 - passed_time_to_seconds > 0:
#                 sleep(3600 - passed_time_to_seconds)
#                 count_request = 0
#                 start_time = current_time
#     except:
#         sleep(10)
#         pass

# current_time = datetime.now()
# formatted_time = current_time.strftime("%Y-%m-%d:%H:%M:%S")
# print(formatted_time)