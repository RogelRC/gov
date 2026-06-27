import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CARPETA = os.path.abspath("gacetas")
CSV = "gacetas.csv"

os.makedirs(CARPETA, exist_ok=True)

options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": CARPETA,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
})
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

with open(CSV, newline="", encoding="utf-8") as f:
    enlaces = list(csv.DictReader(f))

total = len(enlaces)

for i, fila in enumerate(enlaces, 1):
    url = fila["url"]
    nombre = url.split("/")[-1]
    destino = os.path.join(CARPETA, nombre)

    if os.path.exists(destino):
        print(f"[{i}/{total}] Ya existe, saltando: {nombre}")
        continue

    print(f"[{i}/{total}] Descargando: {nombre}")
    driver.get(url)

    while not os.path.exists(destino):
        time.sleep(1)

    print(f"[{i}/{total}] Listo: {nombre}")

driver.quit()
print(f"\nListo. Archivos en carpeta '{CARPETA}'")