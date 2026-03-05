# Move It Philippines: Special Discount Form Automator

> [!IMPORTANT]
> **CURRENT VERSION: PWD CATEGORY ONLY**  
> This script is specifically tuned for the **PWD (Persons with Disability)** discount application workflow. 
> 
> 🚧 **IN DEVELOPMENT:**  
> - 🎓 Student Discount Version  
> - 🏅 Athlete Discount Version  
> 
> *Please do not use this script for Student or Athlete applications yet, as the dynamic form fields and document requirements differ significantly.*

---

## 🚀 Overview

Applying for transport discounts can be a repetitive and time-consuming process involving multiple file uploads and specific data entry. This Python-based Selenium tool automates the entire data-entry phase for the **Move It Philippines Special Discount** form.

### Why this exists?
The Move It Help Centre is built using the **Ant Design (AntD)** framework. AntD uses custom UI components that hide standard HTML inputs, making the site difficult to automate with traditional "click and type" methods. This script uses advanced simulation techniques to bypass these hurdles.

## 🛠 Technical Hurdles & Solutions

This project serves as a case study in automating modern, dynamic React frameworks:

*   **Ant Design Dropdowns:** Standard Selenium clicks often fail to trigger the option lists. This script uses **Accessibility-based Keyboard Navigation** (`TAB` -> `ENTER` -> `ARROW_KEYS`) to interact with elements more reliably.
*   **Read-Only Date Pickers:** The Birthday and Expiry fields block direct text input. We solve this using `ActionChains` to focus the field and simulate actual keystrokes, which updates the internal React state correctly.
*   **Dynamic File Uploads:** Upload slots on this form share identical class names and labels. The script solves this by identifying unique IDs in the "Help Text" (e.g., `pwd_id_front_extra`) and traversing the DOM tree to find the correct hidden `<input type='file'>`.
*   **Zero-Config Driver:** Uses **Selenium Manager** (built into Selenium 4.6+) to automatically detect and manage the Microsoft Edge driver binary.

## 📋 Prerequisites

- **Python 3.x**
- **Microsoft Edge** browser
- **Selenium 4.6+**

```bash
pip install selenium
```

## ⚙️ Configuration

1. **Clone the repository.**
2. **Setup your data:** Open `moveit_pwd_automation.py` and update the `USER_DATA` dictionary with your information.
3. **Setup your files:** Update the `PHOTOS` dictionary with the **absolute paths** to your ID images.

> [!WARNING]
> **Privacy Note:** Never commit your script to a public repository if it contains your real phone number, email, or home address. Use placeholders if you plan to fork or share this code.

```python
USER_DATA = {
    "name": "Juan Dela Cruz",
    "birthday": "2000-01-01",
    # ...
}
```

## 🏃 Usage

Run the script from your terminal or VS Code:

```bash
python moveit_pwd_automation.py
```

1. The script will launch Microsoft Edge and navigate to the Move It Help Centre.
2. It will auto-fill every text box, dropdown, and calendar field in approximately 10–15 seconds.
3. **Manual Handover:** The script will stop before submission. You must:
   - Review the pre-filled data.
   - Solve the **reCAPTCHA** manually.
   - Click the **Submit** button yourself.

## 🛡️ Disclaimer

- **Accuracy:** The user is responsible for ensuring all data pre-filled by the script is accurate before clicking submit.
- **Bot Detection:** This script is intended for personal productivity. It includes built-in delays to mimic human pacing and does not attempt to bypass security features like reCAPTCHA.
- **Affiliation:** This project is not affiliated with, maintained, or endorsed by Move It Philippines.

---
*Developed as a technical solution for modern web framework automation.*