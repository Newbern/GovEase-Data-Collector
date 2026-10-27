from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from __gov.helpers import data, parse_number, clean_legal, is_yes, cls


def state():
    info = data()
    parcels = [
        clean_legal(r.get("Parcel Number", ""))
        for r in (info[0])
        if is_yes(r) and parse_number(r.get("True Improvements", "")) == 0
    ]

    county_name = info[1]
    cls()

    url = f"https://altags.com/{county_name}_Revenue/Property.aspx"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 15)

    driver.get(url)

    print("\nSTATE LOOKUP MODE (ALTAGS)")
    print("ENTER = next parcel")
    print("number = jump")
    print("b = back to menu\n")

    i = 0

    while i < len(parcels):

        parcel = parcels[i]

        print(f"[{i+1}/{len(parcels)}] Parcel:", parcel)

        try:

            dropdown = wait.until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_ddlSearchType"))
            )

            Select(dropdown).select_by_visible_text("Parcel Number")

            search_box = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_tbSearch")

            search_box.clear()
            search_box.send_keys(parcel)

            driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_btnSearch").click()

            wait.until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_realpropdiv"))
            )

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


def money():
    info = data()

    parcels = [
        clean_legal(r.get("Parcel Number", ""))
        for r in (info[0])
        if is_yes(r) and parse_number(r.get("True Improvements", "")) == 0
    ]

    county_name = info[1]
    cls()

    url = f"https://altags.com/{county_name}_Revenue/Property.aspx"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 15)

    driver.get(url)

    print("\nRUNNING STATE TAX CHECK...\n")

    moneys = []

    for i, parcel in enumerate(parcels, start=1):

        print(f"[{i}/{len(parcels)}] Checking:", parcel)

        try:
            dropdown = wait.until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_ddlSearchType"))
            )

            Select(dropdown).select_by_visible_text("Parcel Number")

            search_box = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_tbSearch")

            search_box.clear()
            search_box.send_keys(parcel)

            driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_btnSearch").click()

            wait.until(
                EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder2_realpropdiv"))
            )

            # 🔥 GET TAXES DUE
            tax_element = driver.find_element(
                By.XPATH, "//div[contains(text(),'Taxes Due')]"
            )

            tax_text = tax_element.text.replace("Taxes Due:", "").strip()

        except Exception as e:
            print("Error:", e)
            tax_text = "ERROR"

        moneys.append({
            "parcel": parcel,
            "taxes_due": tax_text
        })

        driver.get(url)

    driver.quit()

    # ✅ EXPORT
    import pandas as pd
    df = pd.DataFrame(moneys)
    df.to_csv("moneys.csv", index=False)

    print("\nDONE — saved to moneys.csv")


