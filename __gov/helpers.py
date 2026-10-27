
# ----------------CHAT GPT DATA -----------------------
def get_csv_files():
    folder = os.path.dirname(os.path.abspath(__file__))  # same folder as script
    folder = os.path.dirname(folder) # back one folder
    folder = os.path.join(folder, "property_data")
    try:
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".csv")]
    except Exception as e:
        print("Error accessing folder:", e)
        return []

def choose_file(files):
    while True:
        print("\nSelect a CSV file:\n")
        for i, f in enumerate(files):
            print(f"{i+1}. {os.path.basename(f)}")  # show only filename
        try:
            choice = int(input("\nChoice: "))
            if 1 <= choice <= len(files):
                return files[choice - 1]  # return full path
        except:
            pass
        print("Invalid choice.\n")

def load_data(file):
    with open(file, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

# -----------------------Steven DATA -----------------------
import os
import csv
import os
import re
from __gov.acerage_solver import acerage



def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def data():
    files = get_csv_files()
    if not files:
        print("No CSV files found.")
        input("Press Enter...")
        return
    csv_file = choose_file(files)
    data_rows = load_data(csv_file)
    # Sort by Owner alphabetically
    data_rows = sorted(data_rows, key=lambda x: x.get("Owner","").upper())
     # Get County Name from the first row
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        first_row = next(reader, None)  # Returns None if file is empty
        county = first_row["County Name"] if first_row else None
    
    return data_rows, county

def parse_number(value):
    try:
        return float(str(value).replace(',', '').replace('$',''))
    except:
        return 0

def clean_legal(text):
    return str(text).strip() if text else "N/A"

def is_yes(row):
    # Checking if there is Acerage
    return acerage(row)
    input(">>>")

def intrested():
    page_count = 0
    info = data()
    county_name = info[1]
    max = 0
    cls()
    for r in (info[0]):
        if is_yes(r) and parse_number(r.get("True Improvements",""))==0:
            max += 1
    for r in (info[0]):
        if is_yes(r) and parse_number(r.get("True Improvements",""))==0:
            if page_count == 0:
                print(f"{county_name.upper()} COUNTY")
                print("\n")
            page_count += 1
            parcel = r.get("Parcel Number", "N/A")
            pinn = r.get("Unique #","N/A")
            owner = r.get("Owner", "N/A")
            building_value = parse_number(r.get("True Improvements",""))
            face = parse_number(r.get("True Land",""))
            legal = clean_legal(r.get("Legal Text",""))
            print("------------------------------------------------")
            print(f"Property #{page_count}\n")
            print(f"Owner: {owner}")
            print(f"Building Value: ${building_value}")
            print(f"Parcel: {parcel}")
            print(f"PINN: {pinn}")
            print(f"Face Value: ${face}")
            print(f"Legal Description: {legal}\n")
            print("------------------------------------------------")
            input(f"[{page_count}/{max}]Press Enter for Next Property...") 
            cls()



def owner_state(data_row):
    if data_row.get("Address 5") != "AL":
        return False
    else:
        return True

def owner_isnt_state(data_row):
    if data_row.get("Address 5") == "AL":
        return False
    else:
        return True





def filter_system(data_row, choice):
    if choice == "a":
        return owner_state(data_row)
    elif choice == "b":
        return owner_isnt_state(data_row)


