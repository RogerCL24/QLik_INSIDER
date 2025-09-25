import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Opciones headless
opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=opts)

try:
    # URL del login de Qlik
    url = "https://qliksense.candy.it/hub/stream/59bf718f-396a-4625-b61c-5233bf946956"  # <-- cámbialo por tu URL real
    driver.get(url)

    print("Página cargada:", driver.title)
    wait = WebDriverWait(driver, 10)

    # Localizar los campos
    username = wait.until(EC.presence_of_element_located((By.ID, "username-input")))
    password = driver.find_element(By.ID, "password-input")
    login_btn = driver.find_element(By.ID, "loginbtn")

    # Rellenar credenciales desde GitHub Secrets
    username.send_keys(os.environ["QLIK_USER"])
    password.send_keys(os.environ["QLIK_PASSWORD"])
    login_btn.click()

    # ---- Check 1: mensaje de error ----
    try:
        error_box = wait.until(EC.presence_of_element_located((By.ID, "error-message")))
        error_text = error_box.text.strip()
        if error_text:
            print("❌ Error en login:", error_text)
        else:
            print("✅ No se mostró mensaje de error inmediato")
    except:
        print("⚠️ No se encontró el cuadro de error")

    # ---- Check 2: URL actual ----
    current_url = driver.current_url
    print("URL actual después de login:", current_url)
    if "login" in current_url.lower():
        print("❌ Parece que seguimos en la pantalla de login")
    else:
        print("✅ La URL cambió, probablemente login exitoso")

    # ---- Check 3: elemento típico del hub ----
    try:
        wait.until(EC.presence_of_element_located((By.ID, "hub")))
        print("✅ Login exitoso, el hub está cargado")
    except:
        print("⚠️ No se encontró el hub (quizá login fallido o selector distinto)")

finally:
    driver.quit()
