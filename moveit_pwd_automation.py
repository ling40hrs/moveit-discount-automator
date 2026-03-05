import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ======================================================
# [!] DISCLAIMER: THIS SCRIPT IS FOR PWD CATEGORY ONLY
# Student and Athlete versions are currently in development.
# ======================================================

# ======================================================
# 1. YOUR DATA CONFIGURATION
# Replace the values below with your actual information.
# ======================================================
USER_DATA = {
    "name": "YOUR_NAME_HERE",
    "phone": "09123456789",
    "email": "yourname@example.com",
    "city": "YOUR_CITY",
    "legal_name": "YOUR_FULL_LEGAL_NAME",
    "birthday": "YYYY-MM-DD",  # Example: 2000-01-01
    "id_no": "YOUR_ID_NUMBER",
    "expiry": "YYYY-MM-DD"     # Example: 2030-12-31
}

# Provide the FULL path to your image files.
# Use the prefix r before the quotes (e.g., r"C:\Users\Name\Desktop\image.png")
PHOTOS = {
    "pwd_and_gov_combined": r"C:\path\to\your\combined_photo.jpg",
    "dual_citizen_proof": "", # Leave empty if not applicable
    "pwd_front": r"C:\path\to\your\pwd_front.jpg",
    "pwd_back": r"C:\path\to\your\pwd_back.jpg",
    "gov_id": r"C:\path\to\your\gov_id.jpg"
}

# ======================================================
# 2. BROWSER SETUP
# ======================================================
edge_options = Options()
# "detach" keeps the browser window open after the script finishes
edge_options.add_experimental_option("detach", True)

# Selenium Manager (v4.6+) handles the Edge Driver automatically
driver = webdriver.Edge(options=edge_options)
actions = ActionChains(driver)

try:
    print("🚀 Initializing Move It Auto-Fill (PWD Version)...")
    driver.get("https://help.moveit.com.ph/passenger/en-ph/18675585189529")
    wait = WebDriverWait(driver, 20)

    # --- STEP 1: CONTACT INFO ---
    print("✍️ Filling contact info...")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys(USER_DATA["name"])
    driver.find_element(By.ID, "phone").send_keys(USER_DATA["phone"])
    
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys(USER_DATA["email"])
    time.sleep(0.5)
    
    # --- STEP 2: CATEGORY (PWD) ---
    # Logic: Uses Keyboard Navigation to interact with Ant Design components
    print("⌨️ Selecting Category: PWD...")
    email_field.send_keys(Keys.TAB)
    time.sleep(0.5)
    actions.send_keys(Keys.ENTER).pause(0.8).send_keys(Keys.ARROW_DOWN).pause(0.5).send_keys(Keys.ENTER).perform()
    time.sleep(1.5)

    # --- STEP 3: REQUEST TYPE (Apply for Special Discount) ---
    print("⌨️ Selecting Request Type...")
    actions.send_keys(Keys.TAB).pause(0.5).send_keys(Keys.ENTER).pause(0.8).send_keys(Keys.ENTER).perform()
    time.sleep(2)

    # --- STEP 4: PWD SUB-FORM ---
    print("📝 Filling PWD specific fields...")
    
    # Registered City
    city_field = wait.until(EC.visibility_of_element_located((By.ID, "request_apply_registered_city")))
    city_field.send_keys(USER_DATA["city"])
    time.sleep(0.5)

    # Legal Name
    legal_name_field = driver.find_element(By.ID, "legal_name")
    legal_name_field.send_keys(USER_DATA["legal_name"])
    time.sleep(0.5)

    # Calendar 1: Birthday
    # AntD inputs are readonly; we tab in and type the string to bypass the popup
    print(f"📅 Entering Birthday: {USER_DATA['birthday']}...")
    legal_name_field.send_keys(Keys.TAB)
    time.sleep(0.8)
    actions.send_keys(USER_DATA["birthday"]).pause(0.5).send_keys(Keys.ENTER).perform()
    time.sleep(0.8)

    # ID Number
    print(f"🔢 Entering ID Number: {USER_DATA['id_no']}...")
    actions.send_keys(Keys.TAB).pause(0.5).send_keys(USER_DATA["id_no"]).perform()
    time.sleep(0.8)

    # Calendar 2: Expiry
    print(f"📅 Entering Expiry: {USER_DATA['expiry']}...")
    actions.send_keys(Keys.TAB).pause(0.8).send_keys(USER_DATA["expiry"]).pause(0.5).send_keys(Keys.ENTER).perform()
    time.sleep(1)

    # --- STEP 5: ATTACH PHOTOS ---
    # Maps the photo paths to the specific AntD Upload slots
    print("📸 Attaching photos to slots...")
    upload_slots = [
        ("pwd_request_apply_id_extra", PHOTOS["pwd_and_gov_combined"]),
        ("pwd_id_front_extra", PHOTOS["pwd_front"]),
        ("pwd_id_back_extra", PHOTOS["pwd_back"]),
        ("id_gov_id_extra", PHOTOS["gov_id"])
    ]

    for container_id, path in upload_slots:
        if path and os.path.exists(path):
            try:
                # Find the parent container to locate the hidden file input
                container = driver.find_element(By.ID, container_id).find_element(By.XPATH, "./ancestor::div[contains(@class, 'ant-form-item')]")
                file_input = container.find_element(By.CSS_SELECTOR, "input[type='file']")
                file_input.send_keys(path)
                print(f"   ✅ Attached: {os.path.basename(path)}")
                time.sleep(1)
            except Exception as e:
                print(f"   ⚠️ Could not attach {os.path.basename(path)}: {e}")
        else:
            print(f"   ⏭️ Skipping: Path not found for {container_id}")

    # --- STEP 6: AGREEMENT CHECKBOX ---
    print("✅ Checking Terms & Conditions agreement...")
    driver.execute_script("document.querySelector('.ant-checkbox-input').click();")

    print("\n" + "="*50)
    print("FINISHED: Data has been successfully pre-filled.")
    print("NEXT STEPS:")
    print("1. Review all fields for accuracy.")
    print("2. Manually solve the reCAPTCHA.")
    print("3. Click 'Submit' to complete your application.")
    print("="*50)

except Exception as e:
    print(f"\n🛑 An error occurred: {e}")
    print("Check if your Internet is stable or if the website structure has changed.")