import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=opts)

try:
    url = "https://qliksense.candy.it/login"  # tu URL real
    driver.get(url)

    print("Página cargada:", driver.title)
    wait = WebDriverWait(driver, 15)


    # Campos de login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username-input")))
    username.clear()
    username.send_keys(os.environ["QLIK_USER"])

    password = wait.until(EC.element_to_be_clickable((By.ID, "password-input")))
    password.clear()
    password.send_keys(os.environ["QLIK_PASSWORD"])

    login_btn = wait.until(EC.element_to_be_clickable((By.ID, "loginbtn")))
    login_btn.click()


    # ---- Check 1: error-message ----
    try:
        error_box = wait.until(EC.presence_of_element_located((By.ID, "error-message")))
        error_text = error_box.text.strip()
        if error_text:
            print("❌ Error en login:", error_text)
        else:
            print("✅ No se mostró mensaje de error inmediato")
    except:
        print("⚠️ No se encontró cuadro de error")

    # ---- Check 2: URL ----
    current_url = driver.current_url
    print("URL actual:", current_url)
    if "login" in current_url.lower():
        print("❌ Seguimos en login (fallo probable)")
    elif "internal_forms_authentication" in current_url.lower():
        print("⚠️ Redirigió a internal_forms_authentication (login fallido o repetido)")
    else:
        print("✅ La URL cambió, parece login exitoso")

    # ---- Check 3: hub ----
    try:
        wait.until(EC.presence_of_element_located((By.ID, "hub")))
        print("✅ Hub detectado, login exitoso")
    except:
        print("⚠️ No se detectó hub")

finally:
    driver.quit()
