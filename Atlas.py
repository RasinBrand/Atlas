from Auth import API
from colorama import Fore, Style
from sys import platform
from psnawp_api import PSNAWP
from datetime import datetime, time
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from alive_progress import alive_bar

import os
import sys
import platform
import time
import socket
import re
import uuid
import psutil
import subprocess
import requests
import geocoder
import geopy
import logging
                
auth = API("https://api.blitzware.xyz/api",
                    "Atlas", "ac6b8cbc52519b86847076ab22c14a570fa385cacf3be53cf48862700836e3d2", "1.4.14")

username, email, password, two_factor_code, key = "", "", "", "", ""

DRock = f"{Fore.GREEN + Style.BRIGHT + "DRock" + Style.RESET_ALL}"
FrankAustin = f"{Fore.LIGHTCYAN_EX + Style.BRIGHT + "FrankAustin" + Style.RESET_ALL}"

present_time = datetime.now()

if sys.platform == 'darwin':
    loc = Nominatim(user_agent="GetLoc") 
elif sys.platform == 'win32' or 'linux': 
    geo = geocoder.ip('me')
    location = geo
    geolocator = Nominatim(user_agent="GetLoc")
    loc = geolocator.geocode(location)
# Basic Functions

def success_message(message):
    print(f"{Fore.GREEN + Style.BRIGHT}Success{Style.RESET_ALL}: {message}")
    
def finished_message(message):
    print(f"{Fore.GREEN + Style.BRIGHT}Finished!{Style.RESET_ALL} {message}")
    
def error_message(message):
    print(f"{Fore.RED + Style.BRIGHT}Error{Style.RESET_ALL} - {Fore.YELLOW + message + Style.RESET_ALL}")
    
def connection_error(message):
    print(f"{Fore.RED + Style.BRIGHT}Connection Error{Style.RESET_ALL} - {Fore.YELLOW + message + Style.RESET_ALL}")
    
def info_message(message):
    print(f"{Fore.BLUE + Style.BRIGHT}Info{Style.RESET_ALL}: {message}")
    
def indifferent_message(message):
    print(f"{Fore.YELLOW + Style.BRIGHT}Indifferent{Style.RESET_ALL}: {message}")
    
def title_message(message):
    print(f"\n=== {Fore.GREEN + Style.BRIGHT + message + Style.RESET_ALL} ===\n")

def location_message(message):
    print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}Location{Style.RESET_ALL}: {message}")

def status_message(message):
    print(f"{Fore.CYAN + Style.BRIGHT}Status{Style.RESET_ALL}: {message}")

def ShowName():
    print(f'{Fore.WHITE} █████╗ ████████╗ ██╗       █████╗   ██████╗{Style.DIM + Style.RESET_ALL}')
    print(f'{Fore.WHITE}██╔══██╗╚══██╔══╝ ██║      ██╔══██╗ ██╔════╝{Style.DIM + Style.RESET_ALL}')
    print(f'{Fore.WHITE}███████║   ██║    ██║      ███████║ ╚█████╗ {Style.DIM + Style.RESET_ALL}')
    print(f'{Fore.WHITE}██╔══██║   ██║    ██║      ██╔══██║  ╚═══██╗{Style.DIM + Style.RESET_ALL}')
    print(f'{Fore.WHITE}██║  ██║   ██║    ███████╗ ██║  ██║ ██████╔╝{Style.DIM + Style.RESET_ALL}')
    print(f'{Fore.WHITE}╚═╝  ╚═╝   ╚═╝    ╚══════╝ ╚═╝  ╚═╝ ╚═════╝ {Style.DIM + Style.RESET_ALL}')
    print('                                       \n                                             ')

def ShowVersion():
    print(f"\nVersion: {Fore.CYAN + auth.app_version + Style.RESET_ALL}\n")

def WipeScreen():  # Clears the console of all text
    if sys.platform == 'linux':
        os.system('cls||clear') # Clears Console On Linux
    elif sys.platform == "darwin":
        os.system('clear') # Clears Console On Mac
    elif sys.platform == "win32":
        os.system('cls') # Clears Console On Windows

def ShowPlatform(): # Shows current users OS / Platform
    if sys.platform == 'linux':
        print(f"{Fore.LIGHTBLUE_EX}Platform{Style.RESET_ALL}: {Fore.LIGHTCYAN_EX}Linux {platform.release() + Style.RESET_ALL}\n") # Linux
    elif sys.platform == "darwin":
       print(f"{Fore.LIGHTBLUE_EX}Platform{Style.RESET_ALL}: {Fore.LIGHTWHITE_EX}Mac {platform.release() + Style.RESET_ALL}\n") # Mac
    elif sys.platform == "win32":
        print(f"{Fore.LIGHTBLUE_EX}Platform{Style.RESET_ALL}: {Fore.LIGHTGREEN_EX}Windows {platform.release() + Style.RESET_ALL}\n") # Windows
    
def GetNPSSO():
    print(f"{Fore.LIGHTBLUE_EX}Step 1{Style.RESET_ALL}: Log into your Playstation account ( https://my.playstation.com/ )\n")
    print(f"{Fore.LIGHTBLUE_EX}Step 2{Style.RESET_ALL}: After you have logged in, paste this link in your browser and go ( https://ca.account.sony.com/api/v1/ssocookie )")
    print(f'    {Fore.LIGHTYELLOW_EX}Note{Style.RESET_ALL}: You should see something like this ( "npsso":"<64 character npsso code>" )\n')
    print(f"{Fore.LIGHTBLUE_EX}Step 3{Style.RESET_ALL}: Copy your NPSSO code and paste it below!\n")
    print(f'{Fore.LIGHTYELLOW_EX}Note{Style.RESET_ALL}: If this automatically takes you back to the main screen, you have probably made too many requests, try again later!')
    print(f'\nType {Fore.LIGHTGREEN_EX}"return"{Style.RESET_ALL} or {Fore.LIGHTGREEN_EX}[0]{Style.RESET_ALL} to go back!')

    code = input("\n\nPaste code here: ")
    
    if len(code) == 64: # this checks if the user input is 64 characters long
        try:
            WipeScreen() # Clears all text on the screen
        
            info_message("Attempting Connection...")

            custom_npsso = code 
            custom_psnawp = PSNAWP(custom_npsso)
            custom_client = custom_psnawp.me()

            def ShowCustomPSNMenu():
                success_message("NPSSO Code Accepted!\n\n")

                print(f"Welcome: {Fore.LIGHTBLUE_EX + custom_client.online_id + Style.RESET_ALL}")
                print(f"Account ID: {Fore.LIGHTMAGENTA_EX + custom_client.account_id + Style.RESET_ALL}")
                print(f"\n\n[1] Show {Fore.GREEN}Friends{Style.RESET_ALL}\n[2] Show {Fore.RED}Blocked{Style.RESET_ALL} List\n[3] Show {Fore.BLUE}Played Games{Style.RESET_ALL} 🐛\n[0] Return")

            WipeScreen()

            ShowCustomPSNMenu()

            option = int(input("\nChoose an option: "))

            if option == 0:
                WipeScreen()
                MainMenu()  

            elif option == 1:
                print(f"\nFreinds: \n")
                friends_list = custom_client.friends_list()
                for friend in friends_list:
                    print(f"{Fore.LIGHTCYAN_EX + friend.online_id + Style.RESET_ALL}\n ID: {Fore.LIGHTYELLOW_EX + friend.account_id + Style.RESET_ALL}\n")

                finished_message("[1] To export as in a txt file \n[0] To Return!")
                return_option = int(input("Return: "))

                if return_option == 0:
                    WipeScreen()
                    ShowCustomPSNMenu()
                    
                if return_option == 1:
                    dir_path = os.path.dirname(os.path.abspath(__file__))
                    file_name = "Atlas.py"
                    full_path = os.path.join(dir_path, file_name )
                    new_path = os.path.dirname + "/Playstation"
                    
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)
                    elif os.path.exists(new_path):
                        with open(f"{os.getcwd()}/Friends.txt", "w") as f:
                            ...      
                            

            elif option == 2:
                print("\nBlocked List: \n")
                blocked_list = custom_client.blocked_list()
                for blocked in blocked_list:
                    print(f"{Fore.RED + blocked.online_id + Style.RESET_ALL}\n : {Fore.LIGHTRED_EX + blocked.account_id + Style.RESET_ALL}\n") 

                finished_message("[0] to Return!")
                return_option = int(input("Return: "))

                if return_option == 0:
                    WipeScreen()
                    ShowCustomPSNMenu()

            
            elif option == 3:
                print("\nPlayed Games: \n") # Buggy
                titles_with_stats = custom_client.title_stats()
                for title in titles_with_stats:
                    print(f"Title: {Fore.LIGHTCYAN_EX + title.name + Style.RESET_ALL} \n ID: {Fore.LIGHTYELLOW_EX + title.title_id + Style.RESET_ALL} \n Play Count: {title.play_count} \n Play Time: {title.play_duration}\n")

                        
        except Exception as ex:
            error_message(ex)
      
    elif code == "":
        error_message("NPSSO code can not be null.")
        time.sleep(5)
        MainMenu()

    elif code == "return" or code == "0":
        WipeScreen()
        MainMenu()

def ShowDeviceInfo():
    
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    try:
        title_message("System Information")
        print(f"Platform: {platform.system()}")
        print(f"Release: {platform.release()}")
        print(f"Version: {platform.version()}")
        print(f"Architecture: {platform.architecture()}")
        print(f"Machine Type: {platform.machine()}")
        print(f"Processor: {platform.processor()}")
        print(f"Hostname: {socket.gethostname()}")
        try:
            if sys.platform == 'win32':
                print(f"GUID: {subprocess.check_output('wmic csproduct get uuid').split('\n')[1].strip()}") # Fix Later
        except Exception as e:
            indifferent_message(f"{e}")
            
        print(f"IP Address: {socket.gethostbyname(socket.gethostname())}")
        print(f"MAC Address: {''.join(re.findall('...', '%012x' % uuid.getnode()))}")
        
        title_message("Boot Information")
        boot_time = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time)
        print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.min}:{bt.second}")
        
        
        title_message("CPU Information")
        print(f"Physical Cores: {psutil.cpu_count(logical=False)}")
        print(f"Total Cores: {psutil.cpu_count(logical=True)}")
        print(f"Max Frequency: {psutil.cpu_freq().max:.2f}Mhz")
        print(f"Min Frequency: {psutil.cpu_freq().min:.2f}Mhz")
        print(f"Current Frequency: {psutil.cpu_freq().current:.2f}Mhz")
        print(f"CPU Usage Per Core: ")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            print(f"    {Fore.LIGHTYELLOW_EX}Core{Style.RESET_ALL} {i}: {percentage}%")
        print(f"Total CPU Usage: {psutil.cpu_percent()}%")
        
        title_message("Memory Information")
        svmem = psutil.virtual_memory()
        print(f"Total: {get_size(svmem.total)}")
        print(f"Available: {get_size(svmem.free)}")
        print(f"Used: {get_size(svmem.used)}")
        print(f"Percentage: {get_size(svmem.percent)}%")
        print(f"RAM: {str(round(psutil.virtual_memory().total / (1024.0 **3)))}GB")
        
        title_message("Disk Information")
        print("Partitions & Usage: \n")
        
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"=== {Fore.GREEN + Style.BRIGHT}Device{Style.RESET_ALL}: {partition.device} ===")
            print(f"    Mountpoint: {partition.mountpoint}")
            print(f"    File System Type: {partition.fstype}")
            
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError as e:
                print(f"{Fore.RED}Error{Style.RESET_ALL}: {e}")
            
            print(f"    Total Size: {get_size(partition_usage.total)}")
            print(f"    Used: {get_size(partition_usage.used)}")
            print(f"    Free: {get_size(partition_usage.free)}")
            print(f"    Percentage: {get_size(partition_usage.percent)}%\n")
        
        disk_io = psutil.disk_io_counters()
        print(f"Total Read: {get_size(disk_io.read_bytes)}")
        print(f"Total Write: {get_size(disk_io.write_bytes)}")
        
        title_message("Network Information")
        if_address = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_address.items():
            for address in interface_addresses:
                print(f"=== {Fore.CYAN + Style.BRIGHT}Interface{Style.RESET_ALL}: {interface_name} ===")
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"    IP Address: {address.address}")
                    print(f"    Netmask: {address.netmask}")
                    print(f"    Broadcast IP: {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"    MAC Address: {address.address}")
                    print(f"    Netmask: {address.netmask}")
                    print(f"    Broadcast IP: {address.broadcast}")
        net_io = psutil.net_io_counters()
        info_message(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        info_message(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
        
    except Exception as e:
        error_message(f"{e}")

def ShowLocalWeather():
    if sys.platform == 'darwin':
        WipeScreen()
        error_message("Weather services are currently unavailable for MacOS")
        time.sleep(2)
        WipeScreen()
        MainMenu()

    elif sys.platform == 'win32' or 'linux': 
        try:
                new_location = f"{location}".replace("<[OK] Ipinfo - Geocode [", "")
                print_loc = re.sub("]>", "", new_location)
                city = new_location
                url = "https://www.google.com/search?q="+"weather"+city
                html = requests.get(url).content
                soup = BeautifulSoup(html, 'html.parser')
                # Getting Temp
                temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
                # Time and sky description
                str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
                # Formatting Data
                data = str.split('\n')
                time = data[0]
                sky = data[1]
                # List all div tags
                # list having all div tags having particular class name
                listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
                # particular list with required data
                strd = listdiv[5].text
                # formatting the string
                pos = strd.find('Wind')
                other_data = strd[pos:]
                info_message(f"Temperature: {temp} 🌡️")
                info_message(f"Time: {time} ⌚")
                info_message(f"Weather: {sky} 🛰️")
        except Exception as ex:
            error_message(f"{ex}")

# Menus
def MainLoginMenu():
        print("\n[1] Login\n[2] Register\n[3] Upgrade\n[4] License Key Only\n[5] Exit")

def LoginMenu():
    username = input("\nEnter Username: ")
    password = input("\nEnter Password: ")
    two_factor_code = input("\nEnter 2FA ( If Enabled ): ")
    if not auth.login(username, password, two_factor_code):
        error_message("\nLogin Failed! Make sure you entered the correct login information.")
        time.sleep(5)
        exit(0)
    else:
        WipeScreen()
        print(f"{Fore.GREEN}Welcome! {username + Style.RESET_ALL}")
        time.sleep(2)
        WipeScreen()
        MainMenu()
            
def RegisterMenu():
    username = input("\nEnter Username: ")
    password = input("\nEnter Password: ")
    email = input("\nEnter Email: ")
    key = input("\nEnter Key: ")
    if not auth.register(username, password, email, key):
        error_message("Make sure your license key is valid and correct.")
        time.sleep(5)
        exit(0)
    else:
        WipeScreen()
        success_message("Registered!")
        LoginMenu()

def UpgradeMenu():
    username = input("\nEnter Username: ")
    password = input("\nEnter Password: ")
    key = input("\nEnter Key: ")
    if not auth.extend(username, password, key):
        error_message("There are currently no upgrades.")
        time.sleep(5)
        exit(0)
    else:
        WipeScreen()
        success_message("Upgraded!")
            
def LicenseKeyOnlyMenu():
    key = input("\n\nEnter Key: ")
    if not auth.login_license_only(key):
        error_message("Make sure you are registered.")
        time.sleep(5)
        exit(0)
    else:
        WipeScreen()
        success_message("Logged in!")

def SpooferMenu():
    WipeScreen()
    
    print("\n[1] Email Spoofer 📬\n[2] Arp Spoofer 🔌\n[3] IP Spoofer 🛜\n[0] Return")
    
    option = int(input("Choose an option: "))
    
    if option == 0:
        WipeScreen()
        MainMenu()
        
    elif option == 1:
        ...
               
    elif option == 2: 
        ...
    elif option == 3:
        ...
        
def WeatherMenu():
   if sys.platform == 'darwin':
        error_message("Weather Menu & Location Services are currently down for MacOS")
        time.sleep(6)
        WipeScreen()
   elif sys.platform == 'win32' or 'linux': 
        WipeScreen()

        new_location = f"{location}".replace("<[OK] Ipinfo - Geocode [", "")
        print_loc = re.sub("]>", "", new_location)

        try: 
            location_message(f"{print_loc}\n")

            ShowLocalWeather()

            print("\n\n[0] To return")
            option = int(input("Choose an option: "))

            if option == 0:
                WipeScreen()
                MainMenu()
            elif option > 0:
                error_message(f"{option} is an Invalid Option")
                time.sleep(2)
                WipeScreen()
                WeatherMenu()

        except Exception as e:
            error_message(f"Could not geo-locate or {e}")
    
def MainMenu():
    WipeScreen()
    ShowName()

    ShowPlatform()
    
    print(f"""
{Fore.GREEN + Style.BRIGHT}[1]{Style.RESET_ALL} Device Information         {Fore.GREEN + Style.BRIGHT}[2]{Style.RESET_ALL} Spoofer      
{Fore.GREEN + Style.BRIGHT}[3]{Style.RESET_ALL} Weather Check              {Fore.GREEN + Style.BRIGHT}[4]{Style.RESET_ALL} Calculator ⭐ 
{Fore.GREEN + Style.BRIGHT}[5]{Style.RESET_ALL} Playstation                {Fore.GREEN + Style.BRIGHT}[6]{Style.RESET_ALL} Credits   
{Fore.GREEN + Style.BRIGHT}[7]{Style.RESET_ALL} Exit\n
""")
    
    ShowVersion()
    
    option = int(input("\nChoose an option: "))        
    
    if option == 0:
        error_message(f"{option} is an Invalid Option")
        time.sleep(2)
        WipeScreen()
        MainMenu()
    
    elif option == 1:
        WipeScreen()
        
        DeviceMenu()
    
    elif option == 2:
        WipeScreen()
        
        SpooferMenu()
    
    elif option == 3:
        WipeScreen()
        WeatherMenu()

    elif option == 4:
        WipeScreen()
        CalculatorMenu()

    elif option == 5:
        WipeScreen()
        
        #DevPlaystationMenu()
        GetNPSSO()
        
    elif option == 6:
        WipeScreen()
        
        CreditsMenu()

    if option == 7:
        WipeScreen()
        
        exit()
        
    elif option > 7:
        error_message(f"{option} is an Invalid Option")
        time.sleep(2)
        WipeScreen()
        MainMenu()

def AuthMenu(): 
    MainLoginMenu()
        
    ShowVersion()
    
    option = int(input("\nChoose an option: "))
    
    if option == 0:
        error_message(f"{option} is an Invalid Option")
        time.sleep(2)
        WipeScreen()
        MainMenu()
    
    elif option == 1:
        WipeScreen()
        LoginMenu()
            
    elif option == 2:
        WipeScreen()
        RegisterMenu()
        
    elif option == 3:
        WipeScreen()
        UpgradeMenu()
        
    elif option == 4:
        WipeScreen()
        LicenseKeyOnlyMenu()
        
    elif option == 5:
        exit(0)
    
    elif option > 5:
        error_message(f"{option} is an Invalid Option")
        time.sleep(2)
        WipeScreen()
        MainMenu()
        
    else:
        WipeScreen()
        error_message(f"{option} is an Invalid Option\n\n")
        
        AuthMenu()

def CreditsMenu():
    print(f"{FrankAustin}")
    print(f"    Main Dev")
    
    print(f"{DRock}")
    print(f"    Student Dev")
    
    print("\n\n[0] Return")
    
    option = int(input("\nChoose an option: "))
    
    if option == 0:
        WipeScreen()
        MainMenu()

def DeviceMenu():
    WipeScreen()
    ShowDeviceInfo()
  
    print("\n\n[0] To return")
    
    option = int(input("Return: "))
    if option == 0:
        WipeScreen()
        MainMenu()

def CalculatorMenu():
    info_message("Enter your first set of digits!")
    
    num1 = int(input())
    
    WipeScreen()
    
    print("\n[1] Add\n[2] Subtract\n[3] Multiply\n[4] Devide\n[5] Return")
    
    initial_option = int(input("Choose an option: "))
    
    if initial_option == 1: # Add
        WipeScreen()
        status_message(f"{num1} + ...")
        info_message("\nEnter the second set!\n")
        
        num2 = int(input())
        
        WipeScreen()
        status_message(f"{num1} + {num2}")
        
        print("\n[1] Add\n[2] Subtract\n[3] Multiply\n[4] Devide\n[5] Complete\n[6] Return")
        
        addition_option = int(input("Choose an option: "))
        
        if addition_option == 1: # Add
            WipeScreen()
            status_message(f"{num1} + {num2} + ...")
            info_message("\nEnter the third set!\n")
        
            num3 = int(input())

            WipeScreen()
            status_message(f"{num1} + {num2} + {num3}")

            print("\n[1] Add\n[2] Subtract\n[3] Multiply\n[4] Devide\n[5] Complete\n[6] Return")
            
            third_addition_option = int(input("Choose an option: "))
            
            if third_addition_option == 1: # Add
                WipeScreen()
                status_message(f"{num1} + {num2} + {num3} + ...")
                info_message("\nEnter the fourth set!\n")

                num4 = int(input())

                WipeScreen()
                status_message(f"{num1} + {num2} + {num3} + {num4}")

                print("\n[1] Add\n[2] Subtract\n[3] Multiply\n[4] Devide\n[5] Complete\n[6] Return")

                fourth_addition_option = int(input("Choose an option: "))
                
                if fourth_addition_option == 1: # Add
                    WipeScreen()
                    status_message(f"{num1} + {num2} + {num3} + {num4} = {num1 + num2 + num3 + num4}")
                    time.sleep(5)
                    WipeScreen()
                    CalculatorMenu()
                elif fourth_addition_option == 2: # Subtract
                    WipeScreen()
                    status_message(f"{num1} + {num2} + {num3} - {num4} = {num1 + num2 + num3 - num4}")
                    time.sleep(5)
                    WipeScreen()
                    CalculatorMenu()
                elif fourth_addition_option == 3: # Multiply
                    WipeScreen()
                    status_message(f"{num1} + {num2} + {num3} x {num4} = {num1 + num2 + num3 * num4}")
                    time.sleep(5)
                    WipeScreen()
                    CalculatorMenu()
                elif fourth_addition_option == 4: # Divide
                    WipeScreen()
                    status_message(f"{num1} + {num2} + {num3} ÷ {num4} = {num1 + num2 + num3 / num4}")
                    time.sleep(5)
                    WipeScreen()
                    CalculatorMenu()
                elif fourth_addition_option == 5: # Complete
                    ...
                elif fourth_addition_option == 6: # Return
                    WipeScreen()
                    CalculatorMenu()
                
                
            elif third_addition_option == 2: # Subtract
                ...
            elif third_addition_option == 3: # Multiply
                ...
            elif third_addition_option == 4: # Divide
                ...
            elif third_addition_option == 5: # Complete
                WipeScreen()
                status_message(f"{num1} + {num2} + {num3} = {num1 + num2 + num3}")
            elif third_addition_option == 6: # Return
                WipeScreen()
                CalculatorMenu()
        elif addition_option == 2: # Subtract
            WipeScreen()
            status_message(f"{num1} + {num2} - ...")
            info_message("\nEnter the third set!\n")
            num3 = int(input())

            WipeScreen()
            status_message(f"{num1} + {num2} - {num3}")
        elif addition_option == 3: # Multiply
            WipeScreen()
            status_message(f"{num1} + {num2} x ...")
            info_message("\nEnter the third set!\n")
            num3 = int(input())

            WipeScreen()
            status_message(f"{num1} + {num2} x {num3}")
        elif addition_option == 4: # Divide
            WipeScreen()
            status_message(f"{num1} + {num2} ÷ ...")
            info_message("\nEnter the third set!\n")
            num3 = int(input())

            WipeScreen()
            status_message(f"{num1} + {num2} ÷ {num3}")
        elif addition_option == 5: # Complete
            WipeScreen()
            status_message(f"{num1} + {num2} = {num1 + num2}")
            time.sleep(5)
            WipeScreen()
            CalculatorMenu()
        elif addition_option == 6: # Return
            WipeScreen()
            CalculatorMenu()      
    elif initial_option == 2: # Subtract
        ...       
    elif initial_option == 3: # Multiply
        ... 
    elif initial_option == 4: # Divide
        ...   
    elif initial_option == 5: # Complete
        WipeScreen()
        MainMenu()
    elif initial_option == 6: # Return
        WipeScreen()
        MainMenu()
    
# Progress bar
def progressbar():
    for total in 7350, 0:
        with alive_bar(total) as bar:
            for _ in range(7350):
                time.sleep(.0008)
                bar()

# Start Code

status_message("Connecting...")
auth.initialize()
time.sleep(3)

if auth.initialized:
    WipeScreen()
    status_message("Connected!")
    progressbar()
    WipeScreen()
    #AuthMenu() # For Release
    MainMenu()
    
else:
    connection_error("Authentication services could not initialize.. Exiting in 5 seconds")
    time.sleep(5)
    exit(0)
    