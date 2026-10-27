
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import pandas as pd
import re
from datetime import timedelta

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --------------------LOGIN INFO ----------------------------
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------ACRE DETECTION FUNCTIONS---------------------
from __gov.helpers import cls
from __gov.acerage_solver import acerage

# --------------DRIVER SETUP----------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

#-----------------LOGIN--------------------------------------
def login():
    
    driver.get("https://liveauctions.govease.com/Account/Login")

    USER = os.getenv("USER")
    PASS = os.getenv("PASSWORD")

    #email = "patricklstaley@gmail.com"
    #password = "HS3>KMfv&>;8AL4"

    driver.find_element(By.ID, "UserName").send_keys(USER)
    driver.find_element(By.ID, "Password").send_keys(PASS)

    submit_buttons = driver.find_elements(By.XPATH, "//form//button[@type='submit']")
    if submit_buttons:
        submit_buttons[0].click()
    cls()
    print("✅ Login complete")


# ---------------UTILITY FUNCTIONS----------------------------

def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))

def print_status(county_name, i, total, parcel, owner, acreage, building, face, legal_desc, elapsed, remaining):
    cls()
    print("====================================================")
    print(f"🏁 COUNTY: {county_name}")
    print("====================================================\n")
    print(f"Parcel Progress : {i}/{total}")
    print("----------------------------------------------------")
    print(f"Parcel         : {parcel}")
    print(f"Owner          : {owner}")
    print(f"Half Acre+     : {acreage}")
    print(f"Building Value : ${building}")
    print(f"Face Value     : ${face}")
    print(f"Legal Desc     : {legal_desc[:60]}{'...' if len(legal_desc)>60 else ''}")
    print("----------------------------------------------------")
    print(f"Elapsed Time   : {elapsed}")
    print(f"ETA Remaining  : {remaining}")
    print("====================================================\n")



def getting_countys():
    driver.find_element(By.XPATH, "//span[contains(@class,'select2-selection')]").click()
    time.sleep(2)

    county_elements = driver.find_elements(By.XPATH, "//ul[contains(@class,'select2-results__options')]//li")
    counties = []

    for el in county_elements:
        name = el.text.strip()
        raw = el.get_attribute("id") or ""
        match = re.search(r"(al\|[a-z]+?\|\d+)", raw)
        if match:
            parts = match.group(1).split("|")
            counties.append({
                "name": name.replace("AL - ", ""),
                "slug": parts[1],
                "id": parts[2]
            })

    print("\nSelect a county by number, or 0 for ALL COUNTIES:\n")
    for idx, county in enumerate(counties, start=1):
        print(f"{idx}: {county['name']}")

    while True:
        choice = input("\nYour choice: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(counties):
                break
        print("Invalid choice. Try again.")

    selected_counties = counties if choice == 0 else [counties[choice - 1]]
    SAVE_AS_ALL = choice == 0

    return selected_counties


def page_scraper(selected_counties):
    all_results = []

    for county in selected_counties:
        cls()
        print(f"\n====================================================")
        print(f"🏁 Starting county: {county['name']}")
        print(f"====================================================\n")

        BASE_URL = f"https://liveauctions.govease.com/al/{county['slug']}/{county['id']}/biddownauctions/"
        links = []
        page = 1

        while True:
            page_url = BASE_URL + str(page)
            driver.get(page_url)
            time.sleep(3)

            elements = driver.find_elements(By.XPATH, "//a[contains(@href,'biddownparcel')]")
            if not elements:
                print(f"⛔ No more pages at {page}")
                break

            for el in elements:
                href = el.get_attribute("href")
                if href:
                    links.append(href)

            print(f"📄 Page {page} collected")
            page += 1

        links = list(set(links))
        print(f"🔗 Total parcels: {len(links)}")
    return links, county['name']
           

def data_scraper(url_and_name):
    links = url_and_name[0]
    county = url_and_name[1]
    script_start_time = time.time()
    results = []
    yes_count = 0
    no_count = 0
    unknown_count = 0
    unknown_list = []


    for i, url in enumerate(links, start=1):
        elapsed = time.time() - script_start_time
        avg_time = elapsed / i if i > 0 else 0
        remaining = (len(links) - i) * avg_time
        elapsed_str = format_time(elapsed)
        remaining_str = format_time(remaining)

        try:
            driver.get(url)
            time.sleep(3)
            body_text = driver.find_element(By.TAG_NAME, "body").text

            legal_description = "NOT FOUND"
            building_value = ""
            face_value = ""
            parcel_number = ""
            owner = "NOT FOUND"

            # LEGAL DESCRIPTION
            try:
                legal_div = driver.find_element(
                    By.XPATH,
                    "//span[contains(text(),'Legal Description')]/ancestor::div[contains(@class,'row')]"
                )
                full_text = legal_div.text
                match_desc = re.search(r"Legal Description\s*[:\-]?\s*(.*)", full_text, re.IGNORECASE)
                if match_desc:
                    legal_description = match_desc.group(1).strip()
                else:
                    legal_description = full_text.strip()
            except:
                legal_description = "NOT FOUND"

            # OWNER (CORRECTED)
            try:
                owner = driver.find_element(
                    By.XPATH,
                    "//span[normalize-space()='Primary Owner']/following::span[@class='no-translate'][1]"
                ).text.strip()
            except:
                owner = "NOT FOUND"

            # HALF ACRE CHECK
            half_acre = acerage(legal_description)

            # BUILDING VALUE
            match = re.search(r"Building Value\s*\$?([\d,\.]+)", body_text, re.IGNORECASE)
            if match:
                building_value = match.group(1)

            # FACE VALUE
            match = re.search(r"Face Value\s*\$?([\d,\.]+)", body_text, re.IGNORECASE)
            if match:
                face_value = match.group(1)

            # PARCEL
            try:
                parcel_div = driver.find_element(
                    By.XPATH,
                    "//span[contains(text(),'Parcel')]/following-sibling::span"
                )
                parcel_number = parcel_div.text.split("\n")[0].strip()
            except:
                match = re.search(r"Parcel\s*[:#]?\s*([\dA-Z\.\s-]+)", body_text, re.IGNORECASE)
                if match:
                    parcel_number = match.group(1).strip()

            # COUNTING
            if half_acre == "YES":
                yes_count += 1
            elif half_acre == "NO":
                no_count += 1
            else:
                unknown_count += 1
                unknown_list.append({
                    "Owner": owner,
                    "County Name": county,
                    "Parcel Number": parcel_number,
                    "Unique #": "N/A",
                    "True Improvements": building_value,
                    "True Land": face_value,
                    "Legal Text": legal_description,
                    "URL": url
                })

            display_parcel = parcel_number.replace(" ", "-")

            results.append({
                "Owner": owner,
                "County Name": county,
                "Parcel Number": parcel_number,
                "Unique #": "N/A",
                "True Improvements": building_value,
                "True Land": face_value,
                "Legal Text": legal_description,
                "URL": url,
                "Half Acre Or More": half_acre,
            })

            print_status(
                county,
                i,
                len(links),
                display_parcel,
                owner,
                half_acre,
                building_value,
                face_value,
                legal_description,
                elapsed_str,
                remaining_str
            )
        except Exception as e:
            print(f"❌ Parcel error: {e}")
    
    # Saving CSVs File
    script_folder = os.path.dirname(os.path.abspath(__file__))
    script_folder = os.path.dirname(script_folder) # back one folder

    data_folder = os.path.join(script_folder, "property_data")
    unknown_folder = os.path.join(script_folder, "property_data/unknown")
    os.makedirs(data_folder, exist_ok=True)  # 👈 make sure it exists

    filename = f"{county}_parcels.csv".replace(" ", "_")
    csv_path = os.path.join(data_folder, filename)  # 👈 save inside /test
    df = pd.DataFrame(results)
    df = df.sort_values(by="Owner")
    df.to_csv(csv_path, index=False)

    unknown_filename = f"UNKNOWN_{county}_parcels.csv".replace(" ", "_")
    unknown_csv_path = os.path.join(unknown_folder, unknown_filename)
    udf = pd.DataFrame(unknown_list)
    udf = udf.sort_values(by="Owner")
    udf.to_csv(unknown_csv_path, index=False)

    print(f"💾 Saved: {csv_path}")

    driver.quit()
    return script_start_time, yes_count, no_count, unknown_count
    
def finish_product(items):
    script_start_time = items[0]
    yes_count = items[1]
    no_count = items[2]
    unknown_count = items[3]


    cls()
    total_time = time.time() - script_start_time
    print("\n====================================================")
    print("🚀 SCRAPING COMPLETE")
    print("====================================================")
    print(f"⏱ Total runtime : {format_time(total_time)}")
    print("\nACREAGE RESULTS")
    print("------------------------------------")
    print(f"YES (≥ 0.5 acres) : {yes_count}")
    print(f"NO  (< 0.5 acres) : {no_count}")
    print(f"UNKNOWN           : {unknown_count}")
    print("------------------------------------")
    print(f"TOTAL PARCELS     : {yes_count + no_count + unknown_count}")
    print("====================================================")
    input("Press Enter...")
    
def collecting():
    cls()
    try:
        print("Loading...")
        login()
    except Exception as e:
        print(e)
            
    try:
        finish_product(data_scraper(page_scraper(getting_countys())))
    except Exception as e:
        print(f"🔥 County failed: {e}")
        input("puase")
    
    



