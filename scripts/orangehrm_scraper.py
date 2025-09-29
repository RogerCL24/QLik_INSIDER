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

    # ---- Ir a Directory ----
    directory_menu = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Directory']"))
    )
    directory_menu.click()

    print("Entramos en Directory...")

    # ---- Esperar a la tabla ----
    table_rows = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.oxd-table-body div.oxd-table-card")
        )
    )

    print(f"Encontradas {len(table_rows)} filas de empleados")

    # ---- Extraer datos ----
    employees = []
    for row in table_rows:
        try:
            name = row.find_element(By.CSS_SELECTOR, "div:nth-child(2)").text
            job_title = row.find_element(By.CSS_SELECTOR, "div:nth-child(3)").text
            location = row.find_element(By.CSS_SELECTOR, "div:nth-child(4)").text
            employees.append([name, job_title, location])
        except:
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
