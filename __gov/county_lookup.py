from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from __gov.helpers import data, parse_number, clean_legal, is_yes, cls

def get_county_search_url(county_name):

    county = county_name.lower()

    if county == "colbert":
        return "https://colbertproperty.assurancegov.com/Property/Search"

    return f"https://{county}property.countygovservices.com/Property/Search"


def county():

    info = data()
    parcels = [
        clean_legal(r.get("Parcel Number", ""))
        for r in (info[0])
        if is_yes(r) and parse_number(r.get("True Improvements", "")) == 0
    ]

    county_name = info[1]
    cls()

    url = get_county_search_url(county_name)

    print("\nUsing URL:", url)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 20)

    driver.get(url)

    print("\nCOUNTY LOOKUP MODE")
    print("ENTER = next parcel")
    print("number = jump")
    print("b = back to menu\n")

    i = 0
   
    while i < len(parcels):

        parcel = parcels[i]

        print(f"[{i+1}/{len(parcels)}] Parcel:", parcel)

        try:

            wait.until(EC.element_to_be_clickable((By.ID, "parcel"))).click()

            search_box = wait.until(
                EC.presence_of_element_located((By.ID, "pt-search-editor-1"))
            )

            search_box.clear()
            search_box.send_keys(parcel)

            driver.find_element(By.ID, "pt-search-button").click()

            row = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "tbody.k-table-tbody tr")
                )
            )

            details_link = row.find_element(By.CSS_SELECTOR, "a.btn-primary")
            details_url = details_link.get_attribute("href")

            print("Opening:", details_url)

            driver.get(details_url)

        except Exception as e:

            print("Lookup failed:", e)

        cmd = input("Next (ENTER), jump #, or 'b': ").strip()

        if cmd.lower() == "b":
            break

        elif cmd.isdigit():
            i = int(cmd) - 1
            driver.get(url)
            continue

        i += 1
        driver.get(url)

    driver.quit()


def colbert():
    print("hi")