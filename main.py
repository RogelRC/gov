from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

URL = "https://www.gacetaoficial.gob.cu/es/busqueda-avanzada"

AÑOS = list(range(2026, 1995, -1))

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

todos_los_enlaces = []

for anno in AÑOS:
    print(f"\n=== Año {anno} ===")

    try:
        driver.get(URL)

        select_tipo = wait.until(
            EC.presence_of_element_located((By.ID, "selectB"))
        )
        Select(select_tipo).select_by_value("1")

        Select(driver.find_element(By.ID, "anno")).select_by_value(str(anno))

        driver.find_element(By.ID, "b_search").click()

        pagina = 1

        while True:
            print(f"  Página {pagina}...")

            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.flaticon")))
            except Exception:
                print(f"  Sin resultados para {anno}.")
                break

            time.sleep(0.2)

            for elem in driver.find_elements(By.CSS_SELECTOR, "a.flaticon"):
                href = elem.get_attribute("href")
                if href and href.endswith(".pdf"):
                    todos_los_enlaces.append({"anno": anno, "url": href})
                    print(f"    ✓ {href}")

            try:
                siguiente = driver.find_element(
                    By.CSS_SELECTOR,
                    "li.pager-next a, a[title='Go to next page'], a.next-page"
                )
                siguiente.click()
                pagina += 1
                time.sleep(0.3)
            except Exception:
                print(f"  Fin de páginas para {anno}.")
                break

    except Exception as e:
        print(f"  Error en año {anno}: {e}. Continuando...")
        continue

driver.quit()

with open("gacetas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["anno", "url"])
    writer.writeheader()
    writer.writerows(todos_los_enlaces)

print(f"\nGuardados {len(todos_los_enlaces)} enlaces en gacetas.csv")