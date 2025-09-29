import os
import csv
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
opts.add_argument("--window-size=1920,1080")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=opts)

try:
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    driver.get(url)

    print("Página cargada:", driver.title)
    wait = WebDriverWait(driver, 15)

    # ---- Login ----
    username = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
    username.clear()
    username.send_keys("Admin")

    password = driver.find_element(By.NAME, "password")
    password.clear()
    password.send_keys("admin123")

    login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_btn.click()

    print("Login realizado...")
    
    # Esperar a que el menú lateral exista
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxd-main-menu")))

  # Ahora buscar Directory de forma robusta
    directory_menu = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@href, '/directory/viewDirectory')]"
        ))
    )
    
    
   # Asegurarse de que está visible en viewport
    driver.execute_script("arguments[0].scrollIntoView(true);", directory_menu)
    directory_menu.click()

    print("Entramos en Directory...")

    # Esperar a que existan tarjetas de empleados
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "orangehrm-directory-card")))

    cards = driver.find_elements(By.CLASS_NAME, "orangehrm-directory-card")
    print(f"Se encontraron {len(cards)} empleados")

    employees = []
    for card in cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, ".orangehrm-directory-card-header").text
            # en cada card también aparece el job title y location, pero en otras etiquetas <p>
            info = card.find_elements(By.CSS_SELECTOR, "p.oxd-text")
            job_title = info[1].text if len(info) > 1 else ""
            location = info[2].text if len(info) > 2 else ""
            employees.append([name, job_title, location])
        except Exception as e:
            print("Error en card:", e)
            continue

    # ---- Guardar en CSV ----
    os.makedirs("output", exist_ok=True)
    with open("output/employees.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Job Title", "Location"])
        writer.writerows(employees)

    print(f"Datos guardados en output/employees.csv ({len(employees)} empleados)")

finally:
    driver.quit()
