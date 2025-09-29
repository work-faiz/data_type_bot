import json
import os
import time
import schedule
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from google import genai
from openai import OpenAI
import configparser

config = configparser.ConfigParser()
config.read('config.properties')

config_ini = configparser.ConfigParser()
config_ini.read('creds.ini')



validation_messages = {
        "RecordNumber": {
        "invalid": "Invalid Data Provided In RecordNumber",
        "missing": "RecordNumber Is Missing"
        },
        "Patient Name": {
        "invalid": "Invalid Data Provided In Patient Name",
        "missing": "Patient Name Is Missing"
        },
        "Father Name": {
        "invalid": "Invalid Data Provided In Father Name",
        "missing": "Father Name Is Missing"
        },
        "Address_1": {
        "invalid": "Invalid Data Provided In Address_1",
        "missing": "Address_1 Is Missing"
        },
        "Email Address": {
        "invalid": "Invalid Data Provided In Email Address",
        "missing": "Email Address Is Missing"
        },
        "PhoneNo_1": {
        "invalid": "Invalid Data Provided In PhoneNo_1",
        "missing": "PhoneNo_1 Is Missing"
        },
        "Date Of_Birth": {
        "invalid": "Invalid Data Provided In Date Of_Birth",
        "missing": "Date Of_Birth Is Missing"
        },
        "CovidCase_Number": {
        "invalid": "Invalid Data Provided In CovidCase_Number",
        "missing": "CovidCase_Number Is Missing"
        },
        "BloodType": {
        "invalid": "Invalid Data Provided In BloodType",
        "missing": "BloodType Is Missing"
        },
        "Country": {
        "invalid": "Invalid Data Provided In Country",
        "missing": "Country Is Missing"
        },
        "PostCode": {
        "invalid": "Invalid Data Provided In PostCode",
        "missing": "PostCode Is Missing"
        },
        "Height": {
        "invalid": "Invalid Data Provided In Height",
        "missing": "Height Is Missing"
        },
        "Weight": {
        "invalid": "Invalid Data Provided In Weight",
        "missing": "Weight Is Missing"
        },
        "Gender": {
        "invalid": "Invalid Data Provided In Gender",
        "missing": "Gender Is Missing"
        },
        "PatientId": {
        "invalid": "Invalid Data Provided In PatientId",
        "missing": "PatientId Is Missing"
        },
        "BillingName": {
        "invalid": "Invalid Data Provided In BillingName",
        "missing": "BillingName Is Missing"
        },
        "Phone_No2": {
        "invalid": "Invalid Data Provided In Phone_No2",
        "missing": "Phone_No2 Is Missing"
        },
        "Claim Number": {
        "invalid": "Invalid Data Provided In Claim Number",
        "missing": "Claim Number Is Missing"
        },
        "UHID_Number": {
        "invalid": "Invalid Data Provided In UHID_Number",
        "missing": "UHID_Number Is Missing"
        },
        "BillNumber": {
        "invalid": "Invalid Data Provided In BillNumber",
        "missing": "BillNumber Is Missing"
        },
        "Admission Date_Time": {
        "invalid": "Invalid Data Provided In Admission Date_Time",
        "missing": "Admission Date_Time Is Missing"
        },
        "Symptoms": {
        "invalid": "Invalid Data Provided In Symptoms",
        "missing": "Symptoms Is Missing"
        },
        "HospitalName": {
        "invalid": "Invalid Data Provided In HospitalName",
        "missing": "HospitalName Is Missing"
        },
        "HospitalAddress": {
        "invalid": "Invalid Data Provided In HospitalAddress",
        "missing": "HospitalAddress Is Missing"
        },
        "Hospital_PhoneNo": {
        "invalid": "Invalid Data Provided In Hospital_PhoneNo",
        "missing": "Hospital_PhoneNo Is Missing"
        },
        "Consultant": {
        "invalid": "Invalid Data Provided In Consultant",
        "missing": "Consultant Is Missing"
        },
        "Refer By": {
        "invalid": "Invalid Data Provided In Refer By",
        "missing": "Refer By Is Missing"
        },
        "Policy No": {
        "invalid": "Invalid Data Provided In Policy No",
        "missing": "Policy No Is Missing"
        },
        "Policy Code": {
        "invalid": "Invalid Data Provided In Policy Code",
        "missing": "Policy Code Is Missing"
        },
        "Claim Status": {
        "invalid": "Invalid Data Provided In Claim Status",
        "missing": "Claim Status Is Missing"
        },
        "Adjusted Amount": {
        "invalid": "Invalid Data Provided In Adjusted Amount",
        "missing": "Adjusted Amount Is Missing",
        "dollar": "$ Sign is missing in Adjusted Amount"
        },
        "Total Paid": {
        "invalid": "Invalid Data Provided In Total Paid",
        "missing": "Total Paid Is Missing",
        "dollar": "$ Sign is missing in Total Paid"
        },
        "Card Name": {
        "invalid": "Invalid Data Provided In Card Name",
        "missing": "Card Name Is Missing"
        },
        "Card Number": {
        "invalid": "Invalid Data Provided In Card Number",
        "missing": "Card Number Is Missing"
        }
    }


def make_chatgpt_call(text):
    try:
        gpt_client = OpenAI(api_key=config_ini.get('openai', 'api_key'))
        response = gpt_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
            {
                "role": "system",
                "content": "You are a data extraction expert. Classify the provided text and return the result in JSON format."
            },
            {
                "role": "user",
                "content": f"""
                    I want you to classify the provided text into specific categories and populate the corresponding JSON structure accordingly. 
                    Here is the text I want you to process: '{text}'. 

                    Here is an example of how I want the JSON to be populated: {{"RecordNumber": "HUSA_912394", "Patient Name": "Badgernet David", "Father Name": "Adjudge Cocaine", "Address_1": "12711 Mitchill Avinui #7", "Email Address": "eyedocbernsie@hotmail.com", "PhoneNo_1": "718-322-2710", "Date_Of_Birth": "09/30/1959", "CovidCase_Number": "975M1843", "BloodType": "B+", "Country": "USA", "PostCode": "43730", "Height": "173.51", "Weight": "168.90", "Gender": "MALE", "PatientId": "HVS65466", "BillingName": "Badgernet David", "Phone_No2": "(263)-654-7654", "Claim Number": "FR-DLIO9_12832", "UHID_Number": "BaX_OlaCp_12991", "BillNumber": "GITR_1013i7", "Admission Date_Time": "Wednesday, May 20, 2020 8:57:00 PM", "Symptoms": "LOSS OF TASTE OR SMELL", "HospitalName": "Boone Hospital Center", "hospitalAddress": "6000 N. Canon Dil Pajaro", "Hospital_PhoneNo": "6890362197", "Consultant": "Luckle Mickey", "Refer By": "self", "Policy No": "BaX#_O,lacM-41220", "Policy Code": "a_iyZ/9265", "Claim Status": "yes", "Adjusted Amount": "$250", "Total Paid": "$350", "Card Name": "MasterCard", "Card Number": "0528 0011 0895 1767"}}. 
                    I want you to also ensure accuracy in the classification of each field and follow the same structure. The output must be in JSON format.
                    I want you to also know that the classification should be done in sequential order as per the categories listed in the JSON structure.
                """
            }
            ]
        )
        response_json = response.choices[0].message.content
        # Handle unexpected response format
        return response_json
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if e.status == "RESOURCE_EXHAUSTED":
            return e.status
        return None


def make_gemini_call(text):
    try:
        client = genai.Client(api_key=config_ini.get('google', 'api_key'))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction="You are a data extraction expert with extensive experience in parsing and classifying complex information from unstructured text.",
            ),
            contents = f""" 
                I want you to classify the provided text into specific categories and populate the corresponding JSON structure accordingly. 
                Here is the text I want you to process: '{text}'. 

                Here is an example of how I want the JSON to be populated: {{"RecordNumber": "HUSA_912394", "Patient Name": "Badgernet David", "Father Name": "Adjudge Cocaine", "Address_1": "12711 Mitchill Avinui #7", "Email Address": "eyedocbernsie@hotmail.com", "PhoneNo_1": "718-322-2710", "Date_Of_Birth": "09/30/1959", "CovidCase_Number": "975M1843", "BloodType": "B+", "Country": "USA", "PostCode": "43730", "Height": "173", "Weight": "168", "Gender": "MALE", "PatientId": "HVS65466", "BillingName": "Badgernet David", "Phone_No2": "(263)-654-7654", "Claim Number": "FR-DLIO9_12832", "UHID_Number": "BaX_OlaCp_12991", "BillNumber": "GITR_1013i7", "Admission Date_Time": "Wednesday, May 20, 2020 8:57:00 PM", "Symptoms": "LOSS OF TASTE OR SMELL", "HospitalName": "Boone Hospital Center", "hospitalAddress": "6000 N. Canon Dil Pajaro", "Hospital_PhoneNo": "6890362197", "Consultant": "Luckle Mickey", "Refer By": "self", "Policy No": "BaX#_O,lacM-41220", "Policy Code": "a_iyZ/9265", "Claim Status": "yes", "Adjusted Amount": "$250", "Total Paid": "$350", "Card Name": "MasterCard", "Card Number": "0528 0011 0895 1767"}}. 
                I want you to also ensure accuracy in the classification of each field and follow the same structure. The output must be in JSON format.
                I want you to also know that the classification should be done in sequential order as per the categories listed in the JSON structure.
            """
        )
        print(response.text)
        return response.text
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if e.status == "RESOURCE_EXHAUSTED":
            return e.status
        return None


def setup_edge_driver():
    """Setup Edge driver with HTTP-friendly options"""
    edge_options = Options()
    
    # Basic options
    edge_options.add_argument("--incognito")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--disable-extensions")
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-infobars")
    edge_options.add_argument("--disable-notifications")
    edge_options.add_argument("--disable-popup-blocking")
    edge_options.add_argument("--disable-features=PopupBlocking")

    # arguments to remove save password prompts
    edge_options.add_argument("--disable-save-password-bubble")
    edge_options.add_argument("--disable-password-manager-reauthentication")
    edge_options.add_argument("--disable-password-generation")
    edge_options.add_argument("--disable-password-manager")
    
    # Enhanced HTTP/HTTPS handling
    edge_options.add_argument('--ignore-certificate-errors')
    edge_options.add_argument('--ignore-ssl-errors')
    edge_options.add_argument('--allow-running-insecure-content')
    edge_options.add_argument('--allow-insecure-localhost')
    edge_options.add_argument('--disable-web-security')
    edge_options.add_argument('--allow-http-screen-capture')
    edge_options.add_argument('--disable-features=VizDisplayCompositor')
    
    # Aggressive SSL/HTTPS disabling
    edge_options.add_argument('--disable-ssl')
    edge_options.add_argument('--disable-ssl-version-fallback')
    edge_options.add_argument('--disable-tls')
    edge_options.add_argument('--disable-tls-version-fallback')
    edge_options.add_argument('--disable-background-timer-throttling')
    edge_options.add_argument('--disable-backgrounding-occluded-windows')
    edge_options.add_argument('--disable-renderer-backgrounding')
    edge_options.add_argument('--disable-features=NetworkService')
    edge_options.add_argument('--disable-features=TranslateUI')
    edge_options.add_argument('--disable-features=BlinkGenPropertyTrees')
    edge_options.add_argument('--disable-features=HttpsUpgrades')
    edge_options.add_argument('--disable-features=AutomaticHttpsUpgrades')
    edge_options.add_argument('--disable-features=HttpsFirstModeV2')
    edge_options.add_argument('--disable-features=HttpsFirstModeV2ForEngagedSites')
    edge_options.add_argument('--disable-features=HttpsOnlyMode')
    edge_options.add_argument('--disable-features=HttpsOnlyModeForEngagedSites')
    edge_options.add_argument('--disable-features=HttpsOnlyModeForEngagedSitesV2')
    edge_options.add_argument('--disable-features=HttpsOnlyModeV2')
    edge_options.add_argument('--disable-features=HttpsOnlyModeV2ForEngagedSites')
    edge_options.add_argument('--disable-features=HttpsOnlyModeV2ForEngagedSitesV2')
    
    # Experimental options for better HTTP handling
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    # Disable password manager and save password prompts
    edge_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    
    # Preferences to handle mixed content and HTTP
    edge_options.add_experimental_option('prefs', {
        'profile.default_content_setting_values.insecure_private_network': 1,
        'profile.default_content_setting_values.notifications': 2,
        'profile.managed_default_content_settings.images': 1,
        'profile.managed_default_content_settings.javascript': 1,
        'profile.managed_default_content_settings.plugins': 1,
        'profile.managed_default_content_settings.popups': 2,
        'profile.managed_default_content_settings.geolocation': 2,
        'profile.managed_default_content_settings.media_stream': 2,
        # Force allow mixed content (HTTP in HTTPS pages)
        'profile.default_content_setting_values.mixed_script': 1,
        'profile.default_content_setting_values.mixed_content': 1,
        # Disable HTTPS-only mode
        'profile.default_content_setting_values.https_only': 2,
        # Disable SSL/TLS
        'profile.default_content_setting_values.ssl_error_override_allowed': 1,
    })
    
    # Initialize Edge driver

    # You may need to download msedgedriver.exe manually and provide its path below
    EDGE_DRIVER_PATH = r"C:\path\to\msedgedriver.exe"  # <-- Update this path

    driver = webdriver.Edge(service=EdgeService(executable_path=EDGE_DRIVER_PATH), options=edge_options)
    
    
    return driver



def convert_img_to_text(file_path, tried=2):
    try:
        url = "http://127.0.0.1:8000/extract_text/"

        files = { "image": open(file_path, 'rb') }
        while tried > 0:
            tried -= 1
            response = requests.post(url, files=files, timeout=300)
            if response.status_code == 200:
                return response.json().get("extracted_text", ""), response.status_code
        return response.text, response.status_code
    except Exception as e:
        raise Exception(f"Image to text conversion failed: {str(e)}") from e


def login(driver):
    try:
        driver.find_element(By.ID, "Email").send_keys(config_ini.get('creds', 'email'))
        driver.find_element(By.ID, "Password").send_keys(config_ini.get('creds', 'passw'))
        driver.find_element(By.XPATH, config.get('xpaths', 'submit')).click()
    except Exception as e:
        raise Exception(f"Login failed: {str(e)}") from e


def fill_remark(driver, response):
    try:
        remark_text = ""
        if re.search(r'\d', response.get("Patient Name", "")):
            remark_text += validation_messages["Patient Name"]["invalid"] + ", "
        if re.search(r'\d', response.get("Father Name", "")):
            remark_text += validation_messages["Father Name"]["invalid"] + ", "
        email = response.get("Email Address", "")
        if re.search(r'\d', email) or not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            remark_text += validation_messages["Email Address"]["invalid"] + ", "
        phone_no_1 = response.get("PhoneNo_1", "")
        # Check if phone number contains exactly 10 digits and nothing else
        if not re.match(r'^\d{10}$', phone_no_1):
            remark_text += validation_messages["PhoneNo_1"]["invalid"] + ", "
        
        dob = response.get("Date_Of_Birth", "")
        # Check if DOB matches MM/DD/YYYY or DD/MM/YYYY or YYYY-MM-DD
        # Accept date formats or words like 'unknown', 'N/A', etc.
        if not (
            re.match(r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$", dob) or
            re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", dob) or
            re.match(r"^\d{4}-\d{2}-\d{2}$", dob) or
            re.search(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b", dob, re.IGNORECASE)
        ):
            remark_text += validation_messages["Date Of_Birth"]["invalid"] + ", "
        
        covid_case_number = response.get("CovidCase_Number", "")
        # Should be exactly 8 alphanumeric characters
        if not (len(covid_case_number) == 8 and covid_case_number.isalnum()):
            remark_text += validation_messages["CovidCase_Number"]["invalid"] + ", "
        
        # Blood type should match common patterns: A+, A-, B+, B-, AB+, AB-, O+, O-
        blood_type = response.get("BloodType", "")
        if not re.match(r"^(A|B|AB|O)[+-]$", blood_type, re.IGNORECASE):
            remark_text += validation_messages["BloodType"]["invalid"] + ", "
        
        # Check if Country contains only alphabetic characters and spaces
        country = response.get("Country", "")
        if not re.match(r'^[A-Za-z\s]+$', country):
            remark_text += validation_messages["Country"]["invalid"] + ", "
        
        if not re.match(r'^[A-Za-z0-9]+$', response.get("PostCode", "")):
            remark_text += validation_messages["PostCode"]["invalid"] + ", "
        height = response.get("Height", "")
        if not (height.isdigit() and len(height) == 3):
            remark_text += validation_messages["Height"]["invalid"] + ", "
        weight = response.get("Weight", "")
        if not (weight.isdigit() and len(weight) == 3):
            remark_text += validation_messages["Weight"]["invalid"] + ", "
        gender = response.get("Gender", "")
        if not re.match(r"^(MALE|FEMALE|OTHER)$", gender):
            remark_text += validation_messages["Gender"]["invalid"] + ", "
        
        # Check if BillingName contains only alphabetic characters and spaces
        if not re.match(r'^[A-Za-z\s]+$', response.get("BillingName", "")):
            remark_text += validation_messages["BillingName"]["invalid"] + ", "
        phone_no_2 = response.get("Phone_No2", "")
        if not re.match(r'^\d{10}$', phone_no_2):
            remark_text += validation_messages["Phone_No2"]["invalid"] + ", "
        hospital_phone_no = response.get("Hospital_PhoneNo", "")
        if not re.match(r'^\d{10}$', hospital_phone_no):
            remark_text += validation_messages["Hospital_PhoneNo"]["invalid"] + ", "
        # Check if Adjusted Amount contains a dollar sign and the numeric part is an integer
        adjusted_amount = response.get("Adjusted Amount", "")
        if not (adjusted_amount.startswith("$") and adjusted_amount[1:].isdigit()):
            if not adjusted_amount.startswith("$"):
                remark_text += validation_messages["Adjusted Amount"]["dollar"] + ", "
            else:
                remark_text += validation_messages["Adjusted Amount"]["invalid"] + ", "
        total_amount = response.get("Total Paid", "")
        # Check if Total Amount contains a dollar sign and the numeric part is an integer
        if not (total_amount.startswith("$") and total_amount[1:].isdigit()):
            if not total_amount.startswith("$"):
                remark_text += validation_messages["Total Paid"]["dollar"] + ", "
            else:
                remark_text += validation_messages["Total Paid"]["invalid"] + ", "
        remark_text = remark_text.rstrip(", ")
        driver.find_element(By.ID, config.get('xpaths', 'remark')).send_keys(remark_text)
        time.sleep(1)
    except Exception as e:
        raise Exception(f"Filling remarks failed: {str(e)}") from e


def fill_individual_form(driver, response):
    try:
        # Check for missing values (None or null)
        for key in response:
            value = response.get(key)
            if value is None or (isinstance(value, str) and value.strip().lower() in ["none", "null", "n.a.", ""]):
                response[key] = "N.A."
        print("Filling form with response:")
        driver.find_element(By.ID, config.get('xpaths', 'record_no')).send_keys(response.get("RecordNumber", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'patient_name')).send_keys(response.get("Patient Name", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'father_name')).send_keys(response.get("Father Name", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'address')).send_keys(response.get("Address_1", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'email')).send_keys(response.get("Email Address", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'phone_no1')).send_keys(response.get("PhoneNo_1", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'dob')).send_keys(response.get("Date_Of_Birth", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'covid_case_no')).send_keys(response.get("CovidCase_Number", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'blood_type')).send_keys(response.get("BloodType", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'country')).send_keys(response.get("Country", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'postcode')).send_keys(response.get("PostCode", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'height')).send_keys(response.get("Height", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'weight')).send_keys(response.get("Weight", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'gender')).send_keys(response.get("Gender", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'patient_id')).send_keys(response.get("PatientId", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'billing_name')).send_keys(response.get("BillingName", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'phone_no2')).send_keys(response.get("Phone_No2", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'claim_no')).send_keys(response.get("Claim Number", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'uhid_no')).send_keys(response.get("UHID_Number", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'bill_no')).send_keys(response.get("BillNumber", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'admission_date_time')).send_keys(response.get("Admission Date_Time", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'symptoms')).send_keys(response.get("Symptoms", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'hospital_name')).send_keys(response.get("HospitalName", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'hospital_address')).send_keys(response.get("hospitalAddress", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'hospital_phone_no')).send_keys(response.get("Hospital_PhoneNo", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'consultant')).send_keys(response.get("Consultant", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'refer_by')).send_keys(response.get("Refer By", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'policy_no')).send_keys(response.get("Policy No", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'policy_code')).send_keys(response.get("Policy Code", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'claim_status')).send_keys(response.get("Claim Status", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'adjusted_amount')).send_keys(response.get("Adjusted Amount", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'total_paid')).send_keys(response.get("Total Paid", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'card_name')).send_keys(response.get("Card Name", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'card_number')).send_keys(response.get("Card Number", "N.A."))
        fill_remark(driver, response)
        driver.find_element(By.XPATH, config.get('xpaths', 'save_btn')).click()
        print("Form filled and saved successfully.")
        time.sleep(2)  # Wait for save to complete
    except Exception as e:
        raise Exception(f"Filling individual form failed: {str(e)}") from e


def click_on_dynamic_row(driver, row_no):
    try:
        image_number = config.get('xpaths', 'image_number')
        image_number = image_number.replace('COUNT', str(row_no))
        image_number = image_number.replace('EMAIL_ID', config_ini.get('creds', 'email'))
        driver.find_element(By.XPATH, image_number).click()
        time.sleep(2)
    except Exception as e:
        raise Exception(f"Generating image XPath failed: {str(e)}") from e

def sort_images(file_list):
    try:
        file_name_map = {}
        for file in file_list:
            file_name, file_ext = os.path.splitext(file)
            file_name_map[file_name] = file
        sorted_files = sorted(file_name_map.keys(), key=lambda x: int(re.search(r'(\d+)', x).group(1)))
        return sorted_files, file_name_map
    except Exception as e:
        raise Exception(f"Sorting images failed: {str(e)}") from e


def pagination(driver, page_no):
    try:
        if page_no and int(page_no) > 1:
            while int(page_no) > 1:
                driver.find_element(By.XPATH, config.get('xpaths', 'next_btn')).click()
                page_no = int(page_no) - 1
                time.sleep(2)  # Wait for the page to load
    except Exception as e:
        raise Exception(f"Pagination failed: {str(e)}") from e


def fill_form(driver, row_no, page_no):
    try:
        driver.find_element(By.XPATH, config.get('xpaths', 'assign_covid')).click()
        print("Clicked on Assign Covid Cases")
        time.sleep(2)  # Wait for the page to load
        # Example of filling a few fields, repeat for all fields as needed
        pagination(driver, page_no)
        if row_no:
            click_on_dynamic_row(driver, int(row_no))
            ss_path = os.path.join(os.getcwd(), 'screenshot_path')
            if not os.path.exists(ss_path):
                print("screenshot_path folder not found...")
                return
            sorted_files, file_name_map = sort_images(os.listdir(ss_path))
            row_count = 0
            for single_path in sorted_files:
                # break
                row_count += 1
                single_path = file_name_map[single_path]
                print(f"Processing file: {single_path} and form count: {row_count}")
                file_path = os.path.join(ss_path, single_path)
                print("started Converting image to text...")
                text, status_code = convert_img_to_text(file_path)
                print("Image to text conversion completed.")
                if status_code != 200:
                    print(f"Service Failure: Failed to convert image to text. Status code: {status_code}")
                    return
                print("started AI API call... ",time.strftime("%H:%M:%S", time.localtime()))
                response_json = make_chatgpt_call(text.strip())
                response_json = json.loads(response_json) if response_json else "RESOURCE_EXHAUSTED"
                if response_json == "RESOURCE_EXHAUSTED":
                    print("ChatGPT API quota exhausted. Trying Gemini API...")
                    response_json = make_gemini_call(text.strip())
                    print("Gemini API call completed.")
                    if response_json == "RESOURCE_EXHAUSTED":
                        print("API quota exhausted. Exiting.")
                        return
                    if response_json:
                        print("Gemini API response received.")
                        response_json = json.loads(response_json.replace("```","").replace("\n", "")[4:])
                    else:
                        print("Failed to get a valid response from Gemini API.")
                        return
                print("Ended AI API call. ", time.strftime("%H:%M:%S", time.localtime()))
                fill_individual_form(driver, response_json)
                os.remove(file_path)  # Clean up the processed file
                print("waiting for 2 seconds...")
                time.sleep(2)
                if row_count % 10 == 0:
                    print("Processed 10 rows, selecting second image.")
                    driver.find_element(By.XPATH, config.get('xpaths', 'assigned_covid_bills')).click()
                    time.sleep(3)
                    pagination(driver, page_no)
                    row_no = int(row_no) + 1
                    click_on_dynamic_row(driver, row_no)
        else:
            print("row number not provided...")
            return
        
    except Exception as e:
        raise Exception(f"Form filling failed: {str(e)}") from e

def main():
    try:
        start_time = time.time()
        print("Starting processing...")
        
        # Make Gemini API call
        url = "https://us.dataeditar.com/"  # Replace with actual URL
        driver = setup_edge_driver()
        driver.get(url)
        login(driver)
        print("Login successful. | Enter below details")
        row_no = input("Enter row number to fill>> ")
        page_no = input("Enter page number>> ")
        fill_form(driver, row_no, page_no)
        print("Form filling process completed.")
        driver.find_element(By.XPATH, config.get('xpaths', 'logout_btn')).click()
        driver.find_element(By.XPATH, config.get('xpaths', 'logout')).click()
        time.sleep(1)
        driver.quit()
        end_time = time.time()
        print(f"Processing completed in {end_time - start_time:.2f} seconds.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.find_element(By.XPATH, config.get('xpaths', 'logout_btn')).click()
        driver.find_element(By.XPATH, config.get('xpaths', 'logout')).click()
        time.sleep(1)
        driver.quit()


main()

# if __name__ == "__main__":
#     main()
#     schedule.every(2).minutes.do(main)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
