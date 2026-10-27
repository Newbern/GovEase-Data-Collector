from __gov.helpers import cls, data, intrested
from __gov.pdf_generator import create
from __gov.pdf_filter import custom
from __gov.county_lookup import county
from __gov.state_lookup import state, money
from __gov.goveease import collecting
from time import sleep
from dotenv import load_dotenv
import os
load_dotenv()


while True:
    cls()
    print("========== Main Menu ==========")
    print("|  1. PDF File                |")
    print("|  2. Acerage Solver          |")
    print("|  3. Lookup Systems          |")
    print("|  4. GoveEase Data Collecter |")
    print("|                             |")
    print("|                             |")
    print("===============================")
    cho = input("\nPick a Number >>>")
    cls()

    if cho == "1":
        while True:
            print("========= PDF Generator ========")
            print("|  1. Intrested PDF File       |")
            print("|  2. Custom Filter PDF        |")
            print("|  B. Back                     |")
            print("|                              |")
            print("|                              |")
            print("|                              |")
            print("|                              |")
            print("|                              |")
            print("================================")
            choice = input("\nPick a Number >>>")
            if choice == "1":
                create()
                break
            elif choice == "2":
                custom()
                break
            elif choice == "B" or choice == "b" or choice == "3":
                break

        input("Press Enter...")
    elif cho == "2":
        print("Sorting Data...")
        #sleep(3)
        cls()
        intrested()
        input("Press Enter...")
    elif cho == "3":
        while True:
            print("========== Tax Lookup ==========")
            print("|  1. State                    |")
            print("|  2. County                   |")
            print("|  3. Map                      |")
            print("|  4. Tax's Due                |")
            print("|  B. Back                     |")
            print("|                              |")
            print("|                              |")
            print("|                              |")
            print("================================")
            choice = input("\nPick a Number >>>")
            if choice == "1":
                state()
                break
            elif choice == "2":
                county()
                break
            elif choice == "3":
                map()
                break
            elif choice == "4":
                money()
      
            elif choice == "B" or choice == "b" or choice == "4":
                break
            cls()

    elif cho == "4":
        while True:
            print("========== GovEase Data Collecter ==========")
            print("|  1. Start                                |")
            print("|  2. Read Username & Password             |")
            print("|  3. Past Years                           |")
            print("|  B. Back                                 |")
            print("|                                          |")
            print("|                                          |")
            print("============================================")
            choice = input("\nPick a Number >>>")
            cls()
            if choice == "1":
                collecting()
                break
            elif choice == "2":
                USER = os.getenv("USER")
                PASS = os.getenv("PASSWORD")
                print(f"Username: {USER}\nPassword: {PASS}")
                print("If you would like to change your password go to (__gov/.env/ ) and open it as a notepad and save it\n")
                input("Press Enter...")
            elif choice == "3":
                print("If this is a new year instead of deleting (property_data) just rename it as the tax year")
                input("Press Enter...")
            elif choice == "B" or choice == "b" or choice == "4":
                break
            cls()
    cls()
    


