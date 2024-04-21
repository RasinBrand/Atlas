import hashlib
import requests
import subprocess
import time
import os
import re

class Security:
    @staticmethod
    def calculate_response_hash(data):
        sha256_hash = hashlib.sha256(data.encode()).hexdigest()
        return sha256_hash

    @staticmethod
    def calculate_file_hash(filename):
        sha256_hash = hashlib.sha256()
        with open(filename, "rb") as f:
            while True:
                data = f.read(65536)  # 64 KB buffer
                if not data:
                    break
                sha256_hash.update(data)
        return sha256_hash.hexdigest()


class Utilities:
    @staticmethod
    def hwid():
        try:
            output = subprocess.check_output(
                ["wmic", "diskdrive", "get", "serialnumber"]).decode("utf-8")
            lines = output.strip().split("\n")
            if len(lines) > 1:
                return lines[1].strip().rstrip(".")
        except Exception as ex:
            return "Error hwid: " + str(ex)
        return ""

    @staticmethod
    def ip():
        external_ip = requests.get("http://icanhazip.com").text.strip()
        return external_ip


class API:
    def __init__(self, api_url, app_name, app_secret, app_version):
        self.api_url = api_url
        self.app_name = app_name
        self.app_secret = app_secret
        self.app_version = app_version
        self.initialized = False
        self.app_data = self.ApplicationData()
        self.user_data = self.UserData()

    class ErrorData:
        def __init__(self):
            self.code = ""
            self.message = ""

    class ApplicationData:
        def __init__(self):
            self.id = ""
            self.name = ""
            self.status = 0
            self.hwidCheck = 0
            self.developerMode = 0
            self.integrityCheck = 0
            self.freeMode = 0
            self.twoFactorAuth = 0
            self.programHash = ""
            self.version = ""
            self.downloadLink = ""

    class UserData:
        def __init__(self):
            self.id = ""
            self.username = ""
            self.email = ""
            self.expiryDate = ""
            self.lastLogin = ""
            self.lastIP = ""
            self.hwid = ""
            self.token = ""

    def initialize(self):
        if self.initialized:
            print("Application is already initialized!")
            time.sleep(3)
            exit(0)
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            data = {
                "name": self.app_name,
                "secret": self.app_secret,
                "version": self.app_version
            }
            response = requests.post(
                f"{self.api_url}/applications/initialize", headers=headers, json=data)

            if response.status_code == 200:
                response_hash = response.headers.get("X-Response-Hash")
                recalculated_hash = Security.calculate_response_hash(
                    response.text)
                if response_hash != recalculated_hash:
                    print("Possible malicious activity detected!")
                    time.sleep(3)
                    exit(0)
                response_data = response.json()
                self.app_data = self.ApplicationData()
                self.app_data.__dict__.update(response_data)
                self.initialized = True

                if self.app_data.status == 0:
                    print(
                        "Looks like this application is offline, please try again later!")
                    time.sleep(3)
                    exit(0)

                if self.app_data.freeMode == 1:
                    print("Application is in Free Mode!")

                if self.app_data.developerMode == 1:
                    print(
                        "Application is in Developer Mode, bypassing integrity and update check!")
                    dir_path = os.path.dirname(os.path.abspath(__file__))
                    file_name = "Atlas.py"  # Specify the file name, change this if needed
                    full_path = os.path.join(dir_path, file_name)
                    with open(f"{os.getcwd()}/integrity.txt", "w") as f:
                        hash = Security.calculate_file_hash(full_path)
                        f.write(hash)
                    print(
                        "Your application's hash has been saved to integrity.txt, please refer to this when your application is ready for release!")
                else:
                    if self.app_data.version != self.app_version:
                        print(
                            f"Update {self.app_data.version} available, redirecting to update!")
                        time.sleep(3)
                        os.startfile(self.app_data.downloadLink)
                        exit(0)
                    if self.app_data.integrityCheck == 1:
                        dir_path = os.path.dirname(
                            os.path.abspath(__file__))
                        file_name = "main.py"  # Specify the file name, change this if needed
                        full_path = os.path.join(dir_path, file_name)
                        if self.app_data.programHash != Security.calculate_file_hash(full_path):
                            print(
                                "File has been tampered with, couldn't verify integrity!")
                            time.sleep(3)
                            exit(0)
            else:
                error_data = response.json()
                error_code = error_data.get("code")
                error_message = error_data.get("message")
                print(f"{error_code}: {error_message}")
                time.sleep(3)
                exit(0)
        except Exception as ex:
            print(f"An error occurred: {str(ex)}")
            time.sleep(3)
            exit(0)

    def register(self, username, password, email, license):
        if not self.initialized:
            print("Please initialize your application first!")
            time.sleep(3)
            return False
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            data = {
                "username": username,
                "password": password,
                "email": email,
                "license": license,
                "hwid": Utilities.hwid(),
                "lastIP": Utilities.ip(),
                "id": self.app_data.id
            }
            response = requests.post(
                f"{self.api_url}/users/register", headers=headers, json=data)

            if response.status_code == 201:
                response_hash = response.headers.get("X-Response-Hash")
                recalculated_hash = Security.calculate_response_hash(
                    response.text)
                if response_hash != recalculated_hash:
                    print("Possible malicious activity detected!")
                    time.sleep(3)
                    exit(0)

                response_data = response.json()
                self.user_data = self.UserData()
                self.user_data.__dict__.update(response_data)
                return True
            else:
                error_data = response.json()
                error_code = error_data.get("code")
                error_message = error_data.get("message")
                print(f"{error_code}: {error_message}")
                time.sleep(3)
                return False
        except Exception as ex:
            print(f"An error occurred: {str(ex)}")
            time.sleep(3)
            return False

    def login(self, username, password, two_factor_code):
        if not self.initialized:
            print("Please initialize your application first!")
            time.sleep(3)
            return False
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            data = {
                "username": username,
                "password": password,
                "twoFactorCode": two_factor_code,
                "hwid": Utilities.hwid(),
                "lastIP": Utilities.ip(),
                "appId": self.app_data.id
            }
            response = requests.post(
                f"{self.api_url}/users/login", headers=headers, json=data)

            if response.status_code == 200:
                response_hash = response.headers.get("X-Response-Hash")
                recalculated_hash = Security.calculate_response_hash(
                    response.text)
                if response_hash != recalculated_hash:
                    print("Possible malicious activity detected!")
                    time.sleep(3)
                    exit(0)

                response_data = response.json()
                self.user_data = self.UserData()
                self.user_data.__dict__.update(response_data)
                return True
            else:
                error_data = response.json()
                error_code = error_data.get("code")
                error_message = error_data.get("message")
                print(f"{error_code}: {error_message}")
                time.sleep(3)
                return False
        except Exception as ex:
            print(f"An error occurred: {str(ex)}")
            time.sleep(3)
            return False

    def login_license_only(self, license):
        if not self.initialized:
            print("Please initialize your application first!")
            time.sleep(3)
            return False
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            data = {
                "license": license,
                "hwid": Utilities.hwid(),
                "lastIP": Utilities.ip(),
                "appId": self.app_data.id
            }
            response = requests.post(
                f"{self.api_url}/licenses/login", headers=headers, json=data)

            if response.status_code == 200:
                response_hash = response.headers.get("X-Response-Hash")
                recalculated_hash = Security.calculate_response_hash(
                    response.text)
                if response_hash != recalculated_hash:
                    print("Possible malicious activity detected!")
                    time.sleep(3)
                    exit(0)

                response_data = response.json()
                self.user_data = self.UserData()
                self.user_data.__dict__.update(response_data)
                return True
            else:
                error_data = response.json()
                error_code = error_data.get("code")
                error_message = error_data.get("message")
                print(f"{error_code}: {error_message}")
                time.sleep(3)
                return False
        except Exception as ex:
            print(f"An error occurred: {str(ex)}")
            time.sleep(3)
            return False

    def extend(self, username, password, license):
        if not self.initialized:
            print("Please initialize your application first!")
            time.sleep(3)
            return False
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            data = {
                "username": username,
                "password": password,
                "license": license,
                "hwid": Utilities.hwid(),
                "appId": self.app_data.id
            }
            response = requests.put(
                f"{self.api_url}/users/upgrade", headers=headers, json=data)

            if response.status_code == 200:
                response_hash = response.headers.get("X-Response-Hash")
                recalculated_hash = Security.calculate_response_hash(
                    response.text)
                if response_hash != recalculated_hash:
                    print("Possible malicious activity detected!")
                    time.sleep(3)
                    exit(0)

                response_data = response.json()
                self.user_data = self.UserData()
                self.user_data.__dict__.update(response_data)
                return True
            else:
                error_data = response.json()
                error_code = error_data.get("code")
                error_message = error_data.get("message")
                print(f"{error_code}: {error_message}")
                time.sleep(3)
                return False
        except Exception as ex:
            print(f"An error occurred: {str(ex)}")
            time.sleep(3)
            return False

    def log(self, username, action):
        if not self.initialized:
            print("Please initialize your application first!")
            return
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.user_data.token}"
            }
            data = {
                "username": username,
                "action": action,
                "ip": Utilities.ip(),
                "appId": self.app_data.id
            }
            response = requests.post(
                f"{self.api_url}/appLogs/", headers=headers, json=data)

            if not response.status_code == 201:
                error_data = response.json()
                error_code = error_data.get("code")
                error_message = error_data.get("message")
                print(f"{error_code}: {error_message}")
        except Exception as ex:
            print(f"An error occurred: {str(ex)}")

    def download_file(self, fileId):
        if not self.initialized:
            print("Please initialize your application first!")
            return
        try:
            headers = {
                "Authorization": f"Bearer {self.user_data.token}"
            }
            response = requests.get(
                f"{self.api_url}/files/{fileId}/download", headers=headers)

            if response.status_code == 200:
                content_disposition = response.headers.get(
                    "content-disposition")
                if content_disposition:
                    parts = content_disposition.split('=')
                    if len(parts) == 2:
                        filename = parts[1].strip('"')
                        output_path = os.path.join(os.getcwd(), filename)
                        with open(output_path, "wb") as file:
                            file.write(response.content)
                else:
                    print(
                        "Content-Disposition header not found. Unable to determine the file name.")
            else:
                error_data = response.json()
                error_code = error_data.get("code")
                error_message = error_data.get("message")
                print(f"{error_code}: {error_message}")
        except Exception as ex:
            print(f"An error occurred: {str(ex)}")