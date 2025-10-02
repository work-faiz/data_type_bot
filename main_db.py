import time
import schedule
import requests
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import NoSuchElementException
import configparser
import db_connection

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
        if re.search(r'\d', response.get("patientname", "")):
            remark_text += validation_messages["Patient Name"]["invalid"] + ", "
        elif response.get("patientname", "").lower() == 'n.a' or response.get("patientname", "").lower() == 'n.a.':
            remark_text += validation_messages["Patient Name"]["missing"] + ", "
        if re.search(r'\d', response.get("fathername", "")):
            remark_text += validation_messages["Father Name"]["invalid"] + ", "
        elif response.get("fathername", "").lower() == 'n.a' or response.get("fathername", "").lower() == 'n.a.':
            remark_text += validation_messages["Father Name"]["missing"] + ", "
        email = response.get("emailaddress", "")
        if re.search(r'\d', email) or not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            remark_text += validation_messages["Email Address"]["invalid"] + ", "
        elif email.lower() == 'n.a' or email.lower() == 'n.a.':
            remark_text += validation_messages["Email Address"]["missing"] + ", "
        phone_no_1 = response.get("phoneno1", "")
        # Check if phone number contains exactly 10 digits and nothing else
        if not re.match(r'^\d{10}$', phone_no_1):
            remark_text += validation_messages["PhoneNo_1"]["invalid"] + ", "
        elif phone_no_1.lower() == 'n.a' or phone_no_1.lower() == 'n.a.':
            remark_text += validation_messages["PhoneNo_1"]["missing"] + ", "
        dob = response.get("dateofbirth", "")
        # Check if DOB matches MM/DD/YYYY or DD/MM/YYYY or YYYY-MM-DD
        # Accept date formats or words like 'unknown', 'N/A', etc.
        if not (
            re.match(r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$", dob) or
            re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", dob) or
            re.match(r"^\d{4}-\d{2}-\d{2}$", dob) or
            re.search(r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b", dob, re.IGNORECASE)
        ):
            remark_text += validation_messages["Date Of_Birth"]["invalid"] + ", "
        elif dob.lower() == 'n.a' or dob.lower() == 'n.a.':
            remark_text += validation_messages["Date Of_Birth"]["missing"] + ", "
        covid_case_number = response.get("covidcasenumber", "")
        # Should be exactly 8 alphanumeric characters
        if not (len(covid_case_number) == 8 and covid_case_number.isalnum()):
            remark_text += validation_messages["CovidCase_Number"]["invalid"] + ", "
        elif covid_case_number.lower() == 'n.a' or covid_case_number.lower() == 'n.a.':
            remark_text += validation_messages["CovidCase_Number"]["missing"] + ", "
        # Blood type should match common patterns: A+, A-, B+, B-, AB+, AB-, O+, O-
        blood_type = response.get("bloodtype", "")
        if not re.match(r"^(A|B|AB|O)[+-]$", blood_type, re.IGNORECASE):
            remark_text += validation_messages["BloodType"]["invalid"] + ", "
        elif blood_type.lower() == 'n.a' or blood_type.lower() == 'n.a.':
            remark_text += validation_messages["BloodType"]["missing"] + ", "
        # Check if Country contains only alphabetic characters and spaces
        country = response.get("country", "")
        if not re.match(r'^[A-Za-z\s]+$', country):
            remark_text += validation_messages["Country"]["invalid"] + ", "
        elif country.lower() == 'n.a' or country.lower() == 'n.a.':
            remark_text += validation_messages["Country"]["missing"] + ", "
        if not re.match(r'^[A-Za-z0-9]+$', response.get("postcode", "")):
            remark_text += validation_messages["PostCode"]["invalid"] + ", "
        elif response.get("postcode", "").lower() == 'n.a' or response.get("postcode", "").lower() == 'n.a.':
            remark_text += validation_messages["PostCode"]["missing"] + ", "
        height = response.get("height", "")
        if not (height.isdigit() and len(height) == 3):
            remark_text += validation_messages["Height"]["invalid"] + ", "
        elif height.lower() == 'n.a' or height.lower() == 'n.a.':
            remark_text += validation_messages["Height"]["missing"] + ", "
        weight = response.get("weight", "")
        if not (weight.isdigit() and len(weight) == 3):
            remark_text += validation_messages["Weight"]["invalid"] + ", "
        elif weight.lower() == 'n.a' or weight.lower() == 'n.a.':
            remark_text += validation_messages["Weight"]["missing"] + ", "
        gender = response.get("gender", "")
        if not re.match(r"^(MALE|FEMALE|OTHER)$", gender):
            remark_text += validation_messages["Gender"]["invalid"] + ", "
        elif gender.lower() == 'n.a' or gender.lower() == 'n.a.':
            remark_text += validation_messages["Gender"]["missing"] + ", "
        
        # Check if BillingName contains only alphabetic characters and spaces
        if not re.match(r'^[A-Za-z\s]+$', response.get("billingname", "")):
            remark_text += validation_messages["BillingName"]["invalid"] + ", "
        elif response.get("billingname", "").lower() == 'n.a' or response.get("billingname", "").lower() == 'n.a.':
            remark_text += validation_messages["BillingName"]["missing"] + ", "
        phone_no_2 = response.get("phoneno2", "")
        if not re.match(r'^\d{10}$', phone_no_2):
            remark_text += validation_messages["Phone_No2"]["invalid"] + ", "
        elif phone_no_2.lower() == 'n.a' or phone_no_2.lower() == 'n.a.':
            remark_text += validation_messages["Phone_No2"]["missing"] + ", "
        hospital_phone_no = response.get("hospitalphoneno", "")
        if not re.match(r'^\d{10}$', hospital_phone_no):
            remark_text += validation_messages["Hospital_PhoneNo"]["invalid"] + ", "
        elif hospital_phone_no.lower() == 'n.a' or hospital_phone_no.lower() == 'n.a.':
            remark_text += validation_messages["Hospital_PhoneNo"]["missing"] + ", "
        # Check if Adjusted Amount contains a dollar sign and the numeric part is an integer
        adjusted_amount = response.get("adjustedamount", "")
        if not (adjusted_amount.startswith("$") and adjusted_amount[1:].isdigit()):
            if not adjusted_amount.startswith("$"):
                remark_text += validation_messages["Adjusted Amount"]["dollar"] + ", "
            else:
                remark_text += validation_messages["Adjusted Amount"]["invalid"] + ", "
        elif adjusted_amount.lower() == 'n.a' or adjusted_amount.lower() == 'n.a.':
            remark_text += validation_messages["Adjusted Amount"]["missing"] + ", "
        total_amount = response.get("totalpaid", "")
        # Check if Total Amount contains a dollar sign and the numeric part is an integer
        if not (total_amount.startswith("$") and total_amount[1:].isdigit()):
            if not total_amount.startswith("$"):
                remark_text += validation_messages["Total Paid"]["dollar"] + ", "
            else:
                remark_text += validation_messages["Total Paid"]["invalid"] + ", "
        elif total_amount.lower() == 'n.a' or total_amount.lower() == 'n.a.':
            remark_text += validation_messages["Total Paid"]["missing"] + ", "
        remark_text = remark_text.rstrip(", ")
        driver.find_element(By.ID, config.get('xpaths', 'remark')).send_keys(remark_text)
        time.sleep(1)
    except Exception as e:
        raise Exception(f"Filling remarks failed: {str(e)}") from e


def fill_individual_form(driver, data):
    try:
        # Check for missing values (None or null)
        for key in data:
            value = data.get(key)
            if value is None or (isinstance(value, str) and value.strip().lower() in ["none", "null", "n.a.", ""]):
                data[key] = "N.A."
        print("Filling form with DB response:")
        driver.find_element(By.ID, config.get('xpaths', 'record_no')).send_keys(data.get("recordnumber", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'patient_name')).send_keys(data.get("patientname", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'father_name')).send_keys(data.get("fathername", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'address')).send_keys(data.get("address1", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'email')).send_keys(data.get("emailaddress", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'phone_no1')).send_keys(data.get("phoneno1", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'dob')).send_keys(data.get("dateofbirth", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'covid_case_no')).send_keys(data.get("covidcasenumber", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'blood_type')).send_keys(data.get("bloodtype", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'country')).send_keys(data.get("country", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'postcode')).send_keys(data.get("postcode", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'height')).send_keys(data.get("height", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'weight')).send_keys(data.get("weight", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'gender')).send_keys(data.get("gender", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'patient_id')).send_keys(data.get("patientid", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'billing_name')).send_keys(data.get("billingname", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'phone_no2')).send_keys(data.get("phoneno2", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'claim_no')).send_keys(data.get("claimnumber", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'uhid_no')).send_keys(data.get("uhidnumber", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'bill_no')).send_keys(data.get("billnumber", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'admission_date_time')).send_keys(data.get("admissiondatetime", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'symptoms')).send_keys(data.get("symptoms", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'hospital_name')).send_keys(data.get("hospitalname", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'hospital_address')).send_keys(data.get("hospitaladdress", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'hospital_phone_no')).send_keys(data.get("hospitalphoneno", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'consultant')).send_keys(data.get("consultant", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'refer_by')).send_keys(data.get("referby", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'policy_no')).send_keys(data.get("policyno", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'policy_code')).send_keys(data.get("policycode", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'claim_status')).send_keys(data.get("claimstatus", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'adjusted_amount')).send_keys(data.get("adjustedamount", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'total_paid')).send_keys(data.get("totalpaid", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'card_name')).send_keys(data.get("cardname", "N.A."))
        driver.find_element(By.ID, config.get('xpaths', 'card_number')).send_keys(data.get("cardnumber", "N.A."))
        fill_remark(driver, data)
        driver.find_element(By.XPATH, config.get('xpaths', 'save_btn')).click()
        print("Form filled and saved successfully.")
        time.sleep(2)  # Wait for save to complete
    except Exception as e:
        raise Exception(f"Filling individual form failed: {str(e)}") from e


def click_on_dynamic_row(driver, documentreference):
    try:
        tr_count = driver.find_elements(By.XPATH, config.get("xpaths", "tr_count"))
        if not tr_count:
            raise Exception(f"Table row not found on page for reference id = {documentreference}")

        for i in range(len(tr_count)):
            inner_html = driver.find_element(By.XPATH, config.get('xpaths', 'row_number').replace("COUNT", str(i+1))).text
            if inner_html.strip().lower() == documentreference.lower():
                image_number = config.get('xpaths', 'image_number')
                image_number = image_number.replace('COUNT', str(i+1))
                image_number = image_number.replace('EMAIL_ID', config_ini.get('creds', 'email'))
                driver.find_element(By.XPATH, image_number).click()
                time.sleep(2)
                return True
        return False
    except Exception as e:
        raise Exception(f"Generating image XPath failed: {str(e)}") from e


def pagination(driver):
    try:
        driver.find_element(By.XPATH, config.get('xpaths', 'next_btn')).click()
        time.sleep(2)  # Wait for the page to load
    except Exception as e:
        raise Exception(f"Pagination failed: {str(e)}") from e



def fill_form(driver, data, row_count):
    try:
        driver.find_element(By.XPATH, config.get('xpaths', 'assigned_covid_bills')).click()
        print("Clicked on Assign Covid Cases")
        time.sleep(2)  # Wait for the page to load
        # Example of filling a few fields, repeat for all fields as needed
        ret_val = click_on_dynamic_row(driver, data['documentreference'])
        if not ret_val:
            while True:
                try:
                    ele = driver.find_element(By.XPATH, config.get("xpaths", "next_btn_disable"))
                except NoSuchElementException:
                    ele = False

                if ele:
                    raise Exception("reach till last page of pagination but filename not found")
                pagination(driver)
                ret_val = click_on_dynamic_row(driver, data['documentreference'])
                if ret_val:
                    break
        print(f"Processing record: {data['recordnumber']} and form count: {row_count}")
        fill_individual_form(driver, data)
    except Exception as e:
        raise Exception(f"Form filling failed: {str(e)}") from e


def is_between_9am_9pm():
    now = datetime.datetime.now().time()  # local time
    start = datetime.time(9, 0)   # 09:00
    end = datetime.time(21, 0)    # 21:00 (9 PM)
    return start < now < end  # strictly greater than 9:00 and strictly less than 21:00


def main():
    try:
        if not is_between_9am_9pm():
            print("09:00 AM - 09:00 PM window slot is over...")
            return True
        if db_connection.can_we_start(config):
            print("We can start...")
            url = config_ini.get("creds", "url")  # Replace with actual URL
            driver = setup_edge_driver()
            driver.get(url)
            login(driver)
            print("Login successful.")
            row_count = 0
            while True:
                row_count += 1
                start_time = time.time()
                print("Started processing...")
                data = db_connection.get_data(config)
                if not data:
                    print("No data found in database...")
                    break
                
                fill_form(driver, data, row_count)
                print(f"Form filling process completed for record number = {data['recordnumber']}.")
                db_connection.save_data(data['id'])
                end_time = time.time()
                print(f"Processing completed in {end_time - start_time:.2f} seconds.")
            driver.find_element(By.XPATH, config.get('xpaths', 'logout_btn')).click()
            driver.find_element(By.XPATH, config.get('xpaths', 'logout')).click()
            time.sleep(1)
            driver.quit()
            
        else:
            print("OPEN Data count is less than 10 or no data found...")
            return
    except Exception as e:
        try:
            print(f"An error occurred: {str(e)}")
            driver.find_element(By.XPATH, config.get('xpaths', 'logout_btn')).click()
            driver.find_element(By.XPATH, config.get('xpaths', 'logout')).click()
            time.sleep(1)
            driver.quit()
        except Exception as e:
            print(f"Final error occurred: {str(e)}")
        try:
            db_connection.save_data_error(data['id'], str(e))
        except Exception as err:
            print(f"exception occurred at saving error remark in DB, {err}")


if __name__ == "__main__":
    main()
    schedule.every(10).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
