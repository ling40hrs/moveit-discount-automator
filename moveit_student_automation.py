import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import traceback

# Student-only Move It autofill script.
# Edit `USER_DATA` and `PHOTOS` for your information and files.

# --- Configuration -------------------------------------------------------
# Leave optional fields blank if not applicable. Required: name, phone, email.
USER_DATA = {
    "name": "Juan Miguel Dela Cruz",
    "phone": "09171234567",
    "email": "juan.delacruz@example.com",
    "city": "Makati",
    "legal_name": "Juan Miguel Dela Cruz",
    "birthday": "2000-04-20",  # Example: 2000-01-01
    "id_no": "S2023456",
    "expiry": "2026-12-31",     # Example: 2030-12-31
    # Student-specific fields
    "school": "University of Example",
    "course": "BS Computer Science"
}

# PHOTOS: list school ID (front/back) and registration image paths.
# Leave a photo value empty ("") if not applicable.
PHOTOS = {
    "school_id_front": r"C:\path\to\your\image.jpg",
    "school_id_back": "",
    "registration_1": r"C:\path\to\your\image.jpg",
    "registration_2": ""
}

CATEGORY = "student"

# --- Browser setup -------------------------------------------------------
edge_options = Options()
edge_options.add_experimental_option("detach", True)

# Selenium Manager (v4.6+) handles the Edge Driver automatically
driver = webdriver.Edge(options=edge_options)
actions = ActionChains(driver)

try:
    print("🚀 Initializing Move It Auto-Fill (Student Version)...")
    driver.get("https://help.moveit.com.ph/passenger/en-ph/18675585189529")
    wait = WebDriverWait(driver, 20)

    # --- Step 1: fill contact info
    print("✍️ Filling contact info...")
    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys(USER_DATA["name"])
    driver.find_element(By.ID, "phone").send_keys(USER_DATA["phone"])
    
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys(USER_DATA["email"])
    time.sleep(0.5)
    
    # --- Step 2: select Student category
    print(f"⌨️ Selecting Category: {CATEGORY.upper()}...")
    email_field.send_keys(Keys.TAB)
    time.sleep(0.5)

    # Open the dropdown and move to the Student option (requires two downs)
    actions.send_keys(Keys.ENTER).pause(0.8).send_keys(Keys.ARROW_DOWN).pause(0.1).send_keys(Keys.ARROW_DOWN).pause(0.5).send_keys(Keys.ENTER).perform()
    time.sleep(1.5)

    # --- Step 3: select request type
    print("⌨️ Selecting Request Type...")
    actions.send_keys(Keys.TAB).pause(0.5).send_keys(Keys.ENTER).pause(0.8).send_keys(Keys.ENTER).perform()
    time.sleep(2)

    # --- Step 4: fill student sub-form
    print("✍️ Filling student sub-form fields...")

    def fill_by_placeholder(placeholder, value):
        try:
            el = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"input[placeholder='{placeholder}']")
            ))
            el.clear()
            el.send_keys(value)
        except Exception as e:
            print(f"   ⚠️ Could not fill '{placeholder}': {e}")

    def fill_date_by_placeholder(placeholder, yyyy_mm_dd):
        """Enter a date (YYYY-MM-DD) and tab out."""
        try:
            el = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"input[placeholder='{placeholder}']")
            ))
            el.clear()
            el.send_keys(yyyy_mm_dd)
            time.sleep(0.3)
            el.send_keys(Keys.ENTER)
            time.sleep(0.3)
            el.send_keys(Keys.TAB)
        except Exception as e:
            print(f"   ⚠️ Could not fill date '{placeholder}': {e}")

    fill_by_placeholder("Registered city", USER_DATA["city"])
    fill_by_placeholder("Name of school", USER_DATA["school"])
    fill_by_placeholder("Course", USER_DATA["course"])
    fill_by_placeholder("Legal name", USER_DATA["legal_name"])
    # Tab out of Legal name before entering the date picker
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='Legal name']").send_keys(Keys.TAB)
    time.sleep(0.3)
    fill_date_by_placeholder("Birthday", USER_DATA["birthday"])
    fill_by_placeholder("ID number", USER_DATA["id_no"])
    # Tab out of ID number before entering the expiry date picker
    driver.find_element(By.CSS_SELECTOR, "input[placeholder='ID number']").send_keys(Keys.TAB)
    time.sleep(0.3)
    fill_date_by_placeholder("ID expiration date", USER_DATA["expiry"])
    time.sleep(0.5)

    # --- Step 5: attach files
    # Collect file inputs in DOM order.
    file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")

    

    # Build lists: school ID files and registration files
    school_id_files = []
    if PHOTOS.get("school_id_front") and os.path.isfile(PHOTOS.get("school_id_front")):
        school_id_files.append(PHOTOS.get("school_id_front"))
    if PHOTOS.get("school_id_back") and os.path.isfile(PHOTOS.get("school_id_back")):
        if PHOTOS.get("school_id_back") != PHOTOS.get("school_id_front"):
            school_id_files.append(PHOTOS.get("school_id_back"))

    registration_files = []
    if PHOTOS.get("registration_1") and os.path.isfile(PHOTOS.get("registration_1")):
        registration_files.append(PHOTOS.get("registration_1"))
    if PHOTOS.get("registration_2") and os.path.isfile(PHOTOS.get("registration_2")):
        if PHOTOS.get("registration_2") != PHOTOS.get("registration_1"):
            registration_files.append(PHOTOS.get("registration_2"))

    # Deduplicate lists while preserving order
    seen = set()
    def dedupe_list(lst):
        out = []
        for p in lst:
            if p and p not in seen:
                out.append(p)
                seen.add(p)
        return out

    school_id_files = dedupe_list(school_id_files)
    registration_files = dedupe_list(registration_files)

    all_files = school_id_files + registration_files

    # Summary before attachments
    print(f"   ℹ️ Found {len(school_id_files)} school ID file(s): {[os.path.basename(p) for p in school_id_files]}")
    print(f"   ℹ️ Found {len(registration_files)} registration file(s): {[os.path.basename(p) for p in registration_files]}")
    print(f"   ℹ️ Detected {len(file_inputs)} file input element(s) on page")

    # Hard-coded input index hints (may need adjustment per page)
    INDEX_MAP = {
        'school_id_index': 8,
        'registration_index': 10,
        'combined_index': 2,
    }

    def fresh_input(idx):
        """Re-query file inputs to avoid stale references."""
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        if 0 <= idx < len(inputs):
            return inputs[idx]
        raise IndexError(f"File input index {idx} out of range (found {len(inputs)} inputs)")

    def try_attach(file_path, role_name, candidates):
        """Try to attach a file using mapped index, then fallbacks."""
        idx = INDEX_MAP.get(role_name)
        if idx is not None:
            try:
                fresh_input(idx).send_keys(file_path)
                print(f"   ✅ Attached {os.path.basename(file_path)} to {role_name} input #{idx+1}")
                return True
            except Exception as e:
                print(f"   ⚠️ Error attaching to {role_name} index #{idx+1}: {e}")

        tried = set()
        for idx in candidates + [i for i in range(len(file_inputs)) if i not in candidates]:
            if idx in tried:
                continue
            tried.add(idx)
            if not (0 <= idx < len(file_inputs)):
                continue
            try:
                fresh_input(idx).send_keys(file_path)
                print(f"   ✅ Attached {os.path.basename(file_path)} to input #{idx+1}")
                return True
            except Exception as e:
                print(f"   ⚠️ Could not attach to input #{idx+1}: {e}")
        return False

    

    # Build candidate lists from DOM ids
    try:
        mapping = driver.execute_script('''
            const inputs = Array.from(document.querySelectorAll("input[type='file']"));
            return inputs.map((input) => {
                let el = input;
                while (el && el !== document.body) {
                    if (el.id) return el.id;
                    el = el.parentElement;
                }
                const sibling = input.parentElement;
                if (sibling) {
                    const found = sibling.querySelector('[id]');
                    if (found) return found.id;
                }
                return null;
            });
        ''')
    except Exception:
        mapping = [None] * len(file_inputs)

    candidates_school = []
    candidates_registration = []
    for i, mid in enumerate(mapping):
        if mid == 'student_id_extra' or (isinstance(mid, str) and 'student' in mid):
            candidates_school.append(i)
        if mid == 'student_school_registration_extra' or (isinstance(mid, str) and 'registration' in mid):
            candidates_registration.append(i)

    if not candidates_school and len(file_inputs) >= 3:
        candidates_school = [2]
    if not candidates_registration and len(file_inputs) >= 4:
        candidates_registration = [3]

    # Handle explicit mappings and attach files accordingly
    combined_attached = False
    school_attached = False
    reg_attached = False

    # Build combined list (school ID files then registration files), deduped
    combined_files = []
    combined_files.extend(school_id_files)
    combined_files.extend(registration_files)
    seen_attach = set()
    dedup_combined = [p for p in combined_files if p and not (p in seen_attach or seen_attach.add(p))]

    # Attach to combined index if provided
    mapped_combined_idx = INDEX_MAP.get('combined_index')
    if mapped_combined_idx is not None and 0 <= mapped_combined_idx < len(file_inputs) and dedup_combined:
        try:
            # Re-query input each time to avoid stale references
            attached_count = 0
            for p in dedup_combined:
                try:
                    fresh_input(mapped_combined_idx).send_keys(p)
                    attached_count += 1
                    time.sleep(0.5)
                except Exception as e:
                    print(f"   ⚠️ Failed to attach {os.path.basename(p)} to combined input #{mapped_combined_idx+1}: {e}")
            if attached_count:
                print(f"   ✅ Attached {attached_count} file(s) to mapped combined input #{mapped_combined_idx+1} (one-by-one).")
                combined_attached = True
        except Exception as e:
            print(f"   ⚠️ Failed to attach combined files to mapped input #{mapped_combined_idx+1}: {e}")

    # Attach school ID files to explicit school_id_index if provided
    mapped_school_idx = INDEX_MAP.get('school_id_index')
    # read registration mapping early for fallback use
    mapped_reg_idx = INDEX_MAP.get('registration_index')
    if mapped_school_idx is not None and 0 <= mapped_school_idx < len(file_inputs) and school_id_files:
        try:
            # dedupe school id files
            seen_s = set()
            s_list = [p for p in school_id_files if p and not (p in seen_s or seen_s.add(p))]
            # Attach each school ID file one-by-one (safer than multi-file send)
            attached_count = 0
            remaining = []
            for p in s_list:
                try:
                    fresh_input(mapped_school_idx).send_keys(p)
                    attached_count += 1
                    time.sleep(0.5)
                except Exception as e:
                    print(f"   ⚠️ Failed to attach {os.path.basename(p)} to mapped school input #{mapped_school_idx+1}: {e}")
                    remaining.append(p)

            if attached_count:
                print(f"   ✅ Attached {attached_count} school ID file(s) to mapped school input #{mapped_school_idx+1} (one-by-one).")
                school_attached = True

            # If any files remain (or input likely doesn't support multiple), try fallback attachments
            if remaining:
                print(f"   ℹ️ Attaching remaining {len(remaining)} school ID file(s) to fallback inputs.")
                fb_attached = False
                if mapped_reg_idx is not None and 0 <= mapped_reg_idx < len(file_inputs):
                    try:
                        for p in remaining:
                            fresh_input(mapped_reg_idx).send_keys(p)
                            time.sleep(0.5)
                        print(f"   ✅ Attached {len(remaining)} file(s) to mapped registration input #{mapped_reg_idx+1} as fallback.")
                        fb_attached = True
                        reg_attached = True
                    except Exception:
                        fb_attached = False
                if not fb_attached:
                    for rem in remaining:
                        placed = try_attach(rem, 'school_id_index_fallback', [i for i in range(len(file_inputs))])
                        if placed:
                            print(f"   ✅ Placed fallback file {os.path.basename(rem)}")
                        else:
                            print(f"   ⚠️ Could not place fallback file {os.path.basename(rem)} automatically.")
        except Exception as e:
            print(f"   ⚠️ Failed to attach school ID files to mapped input #{mapped_school_idx+1}: {e}")

    # Attach registration files to explicit registration_index if provided
    mapped_reg_idx = INDEX_MAP.get('registration_index')
    if mapped_reg_idx is not None and 0 <= mapped_reg_idx < len(file_inputs) and registration_files:
        try:
            # dedupe registration files
            seen_reg = set()
            reg_to_attach = [p for p in registration_files if p and not (p in seen_reg or seen_reg.add(p))]
            attached_count = 0
            for p in reg_to_attach:
                try:
                    fresh_input(mapped_reg_idx).send_keys(p)
                    attached_count += 1
                    time.sleep(0.5)
                except Exception as e:
                    print(f"   ⚠️ Failed to attach {os.path.basename(p)} to mapped registration input #{mapped_reg_idx+1}: {e}")
            if attached_count:
                print(f"   ✅ Attached {attached_count} registration file(s) to mapped registration input #{mapped_reg_idx+1} (one-by-one).")
                reg_attached = True
        except Exception as e:
            print(f"   ⚠️ Failed to attach registration files to mapped input #{mapped_reg_idx+1}: {e}")

    # Fallback: try candidate-based attachment if explicit mapping failed
    if not school_attached:
        if school_id_files:
            attached = False
            for sf in school_id_files:
                print(f"   Trying to attach School ID file: {os.path.basename(sf)}")
                if try_attach(sf, 'school_id_index', candidates_school):
                    attached = True
                    break
            if not attached:
                print("   ⚠️ Could not automatically map School ID files. Please attach manually in the browser.")

    if not reg_attached:
        if registration_files:
            attached = False
            for rf in registration_files:
                print(f"   Trying to attach Registration file: {os.path.basename(rf)}")
                if try_attach(rf, 'registration_index', candidates_registration):
                    attached = True
                    break
            if not attached:
                print("   ⚠️ Could not automatically map Registration files. Please attach manually in the browser.")

    # --- Step 6: check agreement
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
