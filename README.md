<h1 align="center">MoveIt Discount Automator</h1>

<p align="center">
  <img src="https://github.com/user-attachments/assets/03f68471-81f4-436e-908b-d20effa890fe" width="600" alt="Project Dashboard">
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="https://www.selenium.dev/"><img src="https://img.shields.io/badge/Selenium-4.6%2B-green?logo=selenium&logoColor=white" alt="Selenium 4.6+"></a>
  <a href="https://www.microsoft.com/edge"><img src="https://img.shields.io/badge/Browser-Edge-blue?logo=microsoftedge&logoColor=white" alt="Edge Support"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white" alt="MIT License"></a>
</p>

<p align="center">
  <strong>Enterprise-grade form automation for Move It Philippines Discount Applications</strong>
</p>

---

## Table of Contents
- [Executive Summary](#executive-summary)
- [Current Release Status](#current-release-status)
- [Core Engine Capabilities](#core-engine-capabilities)
- [Installation & Requirements](#installation--requirements)
- [Configuration & Deployment](#configuration--deployment)
- [Compliance & Safety](#compliance--safety)
- [Disclaimer & Legal](#disclaimer--legal)

---

## Executive Summary

The **MoveIt Automation Suite** is a Python-based Selenium framework designed to streamline the data-entry process for the **Move It Philippines Special Discount** portal. 

By automating repetitive form interactions, this tool reduces manual entry time and minimizes human error during the application process. The engine is specifically architected to handle the **Ant Design (AntD)** framework, utilizing advanced DOM interaction techniques to ensure stability where traditional automation scripts fail.

## Current Release Status

> **Stable Release:** v1  
> **Supported Workflows:** PWD & Student Categories

| Module | Status | Version | Documentation |
| :--- | :---: | :---: | :--- |
| **PWD Automation** | ✅ Stable | 1.0.0 | [View Config](#option-a-pwd-application-module) |
| **Student Automation** | ✅ Stable | 1.0.0 | [View Config](#option-b-student-application-module) |
| **Athlete Automation** | 🚧 Dev | 0.9.0-Beta | Coming Soon |

---

## Core Engine Capabilities

This project serves as a reference implementation for automating dynamic React/AntD frameworks. The underlying engine addresses common instability points in web automation:

*   **Accessibility-Based Navigation:**  
    Bypasses standard click handlers that fail on Ant Design dropdowns. The engine utilizes keyboard simulation (`TAB` → `ENTER` → `ARROW_KEYS`) for 99.9% interaction reliability.
*   **State-Aware Input Handling:**  
    Resolves read-only date picker restrictions by focusing fields and simulating native keystrokes, ensuring the internal React state updates correctly.
*   **Dynamic DOM Traversal:**  
    Identifies file upload inputs via unique Help Text IDs (e.g., `pwd_id_front_extra`) rather than volatile class names, ensuring script resilience against UI updates.
*   **Zero-Config Driver Management:**  
    Leverages **Selenium Manager** (v4.6+) to automatically provision the correct Microsoft Edge WebDriver binary without user intervention.

### Workflow Logic Optimizations (Student Module)

The Student Application module includes specific logic patches to handle aggressive DOM re-rendering:

1.  **Stale Element Mitigation:** Implements a `fresh_input(idx)` helper to re-query the DOM before every interaction, preventing `StaleElementReferenceException`.
2.  **Sequential Payload Injection:** Enforces a `0.5s` delay between file uploads to prevent race conditions during multi-file attachments.
3.  **Deterministic Index Mapping:** Utilizes a hard-coded `INDEX_MAP` for file slots to maximize execution speed and reliability.

---

## Installation & Requirements

### System Prerequisites
- **Runtime:** Python 3.8 or higher
- **Browser:** Microsoft Edge (Latest Stable Version)
- **Package Manager:** pip

### Dependencies
Install the required Selenium package via terminal:

```bash
pip install selenium
```

---

## Configuration & Deployment

### Option A: PWD Application Module
**Entry Point:** `moveit_pwd_automation.py`

1.  **Initialize Configuration:** Open the script and populate the `USER_DATA` dictionary with accurate applicant information.
2.  **Asset Mapping:** Update the `PHOTOS` dictionary with absolute file paths to valid PWD identification documents.
3.  **Execute:**
    ```bash
    python moveit_pwd_automation.py
    ```

### Option B: Student Application Module
**Entry Point:** `moveit_student_automation.py`

1.  **Initialize Configuration:** Populate `USER_DATA`. Ensure student-specific fields are included:
    ```python
    USER_DATA = {
        "school": "University of Example",
        "course": "BS Computer Science",
        # ... standard fields
    }
    ```
2.  **Asset Mapping:** Provide paths for `school_id_front`, `school_id_back`, and `registration_1`.
3.  **Execution:**
    ```bash
    python moveit_student_automation.py
    ```

---

## Compliance & Safety

> **Manual Verification Required**  
> For security and compliance reasons, the automation sequence **terminates prior to final submission**.

The operator must perform the following steps manually:
1.  **Data Audit:** Verify all pre-filled fields for accuracy.
2.  **Security Challenge:** Complete the **reCAPTCHA** verification.
3.  **Final Submission:** Manually click the **Submit** button.

---

## Disclaimer & Legal

*   **Data Integrity:** The end-user assumes full responsibility for the accuracy of data entered by the script. The developers are not liable for application rejections due to data errors.
*   **Terms of Service:** This tool is intended for personal productivity assistance. It does not bypass security protocols (e.g., reCAPTCHA) and operates within standard browser automation limits.
*   **Affiliation:** This software is an open-source community project. It is **not** affiliated with, endorsed by, or maintained by Move It Philippines.

---

<p align="center">
  <sub>© 2026 MoveIt Discount Automator. Released under the <a href="LICENSE">MIT License</a>.</sub>
</p>

