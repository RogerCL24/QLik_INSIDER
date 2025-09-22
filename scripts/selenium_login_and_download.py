from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Opciones headless (sin interfaz gráfica)
opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=opts)

try:
    # Página de demo (Herokuapp login)
    url = "https://the-internet.herokuapp.com/login"
    driver.get(url)

    print("Página cargada:", driver.title)

    # Localizar campos de login
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    login_btn = driver.find_element(By.CSS_SELECTOR, "button.radius")

    # Rellenar (credenciales dummy)
    username.send_keys("tomsmith")
    password.send_keys("SuperSecretPassword!")
    login_btn.click()

    # Comprobar si el login funcionó
    msg = driver.find_element(By.ID, "flash").text
    print("Mensaje después de login:", msg)

finally:
    driver.quit()

