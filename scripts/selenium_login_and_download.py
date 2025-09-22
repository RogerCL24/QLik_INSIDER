#!/usr/bin/env python3
"""
Script de ejemplo:
1) Abre la página de login de the-internet
2) Hace login con tomsmith / SuperSecretPassword!
3) Navega a /download
4) Obtiene el primer enlace de descarga y lo descarga con requests
5) Guarda el fichero en /tmp/downloaded_file (nombre original)
Este flujo evita manejar descargas en el navegador headless (prefiero
descargar con requests
usando la URL que encuentre en la página).
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse
import requests
import os
import time
from pathlib import Path

BASE = "https://the-internet.herokuapp.com"
LOGIN = urljoin(BASE, "/login")
DOWNLOAD_PAGE = urljoin(BASE, "/download")
OUT_DIR = Path("/tmp")
OUT_DIR.mkdir(parents=True, exist_ok=True)
opts = Options()

# Usamos modo headless; en GitHub Actions la ruta del binario será especificada en workflow
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--disable-gpu")
# Si necesitas cambiar la ruta del binario (en Actions se establece), puedes hacerlo:
# opts.binary_location = "/usr/bin/chromium-browser"

# crea driver
driver = webdriver.Chrome(options=opts)
try:
    print("Abriendo login...", LOGIN)
    driver.get(LOGIN)
    time.sleep(1)
    # Rellenar formulario
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    time.sleep(2)

    # Comprobación rápida: buscar message de success
    try:
        flash = driver.find_element(By.ID, "flash").text
        print("Flash:", flash.strip())
    except Exception:
        print("No se encontró flash (ok).")

    # Ir a la página de descarga
    driver.get(DOWNLOAD_PAGE)
    time.sleep(1)
    # Buscar el primer enlace de descarga
    link_el = driver.find_element(By.CSS_SELECTOR, "#content a")
    href = link_el.get_attribute("href")
    print("Found href:", href)
    # Asegurarnos de que es absoluto
    download_url = urljoin(DOWNLOAD_PAGE, href)
    # Descargamos con requests
    print("Descargando...", download_url)
    r = requests.get(download_url, timeout=60)
    r.raise_for_status()
    # intentar obtener nombre de fichero
    parsed = urlparse(download_url)
    name = Path(parsed.path).name or "downloaded_file"
    out_path = OUT_DIR / name
    out_path.write_bytes(r.content)
    print("Guardado en:", out_path)

except Exception as e:
    print("Error durante el flujo:", e)
    raise
finally:
    try:
        driver.quit()
    except Exception:
        pass