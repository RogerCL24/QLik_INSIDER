from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Opciones headless
opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=opts)

try:
    # URL de login de Qlik
    url = "https://qliksense.candy.it/hub/stream/59bf718f-396a-4625-b61c-5233bf946956"
    driver.get(url)

    print("Página cargada:", driver.title)

    wait = WebDriverWait(driver, 10)

    # Localizar los campos
    username = wait.until(EC.presence_of_element_located((By.ID, "username-input")))
    password = driver.find_element(By.ID, "password-input")
    login_btn = driver.find_element(By.ID, "loginbtn")

    # Completar credenciales
    username.send_keys(os.environ["QLIK_USER"])
    password.send_keys(os.environ["QLIK_PASSWORD"])
    login_btn.click()

    # Comprobar si hay mensaje de error o login exitoso
    try:
        msg = wait.until(EC.presence_of_element_located((By.ID, "error-message"))).text
        if msg.strip():
            print("Error en login:", msg)
        else:
            print("Login posiblemente exitoso (no hay error)")
    except:
        print("No se encontró mensaje de error, login posiblemente correcto")

finally:
    driver.quit()
