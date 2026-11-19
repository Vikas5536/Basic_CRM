# CoustomerManagementRelationship - Deployment & Configuration Guide

यह प्रोजेक्ट आपकी HostGator cPanel होस्टिंग और MySQL डेटाबेस के अनुसार पूरी तरह कॉन्फ़िगर कर दिया गया है।

---

## 1. डेटाबेस कॉन्फ़िगरेशन (Database Configuration)

आपके cPanel और phpMyAdmin स्क्रीनशॉट के अनुसार सेटिंग्स:

| Setting | Value |
| :--- | :--- |
| **Database Host** | `localhost` |
| **Port** | `3306` |
| **Database Name** | `upayssmk_sidak_crm` |
| **Database User** | `upayssmk_sidak` |
| **Password** | `.env` फ़ाइल में डालें (`MYSQL_PASSWORD=...`) |

---

## 2. पासवर्ड कहाँ डालना है? (Where to set password)

प्रोजेक्ट के रूट फ़ोल्डर में `.env` फ़ाइल तैयार है:

```env
# Flask Secret Key
SECRET_KEY=sidak_crm_secret_key_production_2026

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=upayssmk_sidak
MYSQL_PASSWORD=YOUR_ACTUAL_SQL_PASSWORD
MYSQL_DATABASE=upayssmk_sidak_crm
```

> **नोट:** `YOUR_ACTUAL_SQL_PASSWORD` को हटाकर अपने MySQL यूजर `upayssmk_sidak` का सही पासवर्ड डाल दें।

---

## 3. HostGator cPanel पर कैसे लॉन्च करें (Step-by-Step Deployment)

### Step 1: फ़ाइलें अपलोड करें (Upload Files)
- cPanel में **File Manager** खोलें।
- अपने डोमेन/सब-डोमेन के फोल्डर में प्रोजेक्ट फाइल्स अपलोड करें (या Git Version Control से क्लोन करें)।

### Step 2: "Setup Python App" खोलें
- cPanel डैशबोर्ड में जाकर **Setup Python App** (CloudLinux Python Selector) पर क्लिक करें।
- **Create Application** पर क्लिक करें:
  - **Python Version**: `3.9` / `3.10` / `3.11` (जो भी उपलब्ध हो)
  - **Application root**: आपकी प्रोजेक्ट डायरेक्टरी का पाथ
  - **Application URL**: आपका डोमेन/सब-डोमेन
  - **Application startup file**: `passenger_wsgi.py`
  - **Application Entry point**: `application`
- **CREATE** बटन दबाएं।

### Step 3: Dependencies इनस्टॉल करें
- cPanel में ऊपर दी गई **virtualenv command** को कॉपी करके Terminal में चलाएं।
- इसके बाद dependencies इंस्टॉल करें:
  ```bash
  pip install -r requirements.txt
  ```

### Step 4: `.env` फ़ाइल में पासवर्ड चेक करें
- File Manager में **Settings** -> **Show Hidden Files (dotfiles)** को ऑन करें ताकि `.env` फ़ाइल दिखाई दे।
- `.env` फ़ाइल एडिट करके `MYSQL_PASSWORD` में अपना डेटाबेस पासवर्ड सेट करें और सेव करें।

### Step 5: Application Restart करें
- cPanel में Python App पेज पर जाकर **Restart** बटन पर क्लिक करें।
- आपकी CRM वेबसाइट लाइव हो जाएगी!
