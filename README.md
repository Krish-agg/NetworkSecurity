# 🛡️ Phishing Websites Predictions

This project aims to classify websites as **phishing** or **legitimate** using a dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/). Phishing websites attempt to trick users into revealing sensitive information, and this model helps in identifying such malicious sites based on their attributes.

---

## 📊 Dataset Overview

- **Source**: UCI Machine Learning Repository  
- **Total Observations**: 11055 
- **TrainTestRatio**: 0.2  
- **Features**: 30  
- **Target Variable**: `result`  
  - `1` → Legitimate website  
  - `-1` → Phishing website

---

## 🧾 Feature Description (Codebook)

| Feature Description            | Values       | Column Name          |
|-------------------------------|--------------|-----------------------|
| Having IP Address             | `{1, 0}`     | `has_ip`              |
| Having long URL               | `{1, 0, -1}` | `long_url`            |
| Uses Shortening Service       | `{1, 0}`     | `short_service`       |
| Having '@' Symbol             | `{1, 0}`     | `has_at`              |
| Double Slash Redirecting      | `{1, 0}`     | `double_slash_redirect` |
| Having Prefix-Suffix          | `{-1, 0, 1}` | `pref_suf`            |
| Having Sub Domain             | `{-1, 0, 1}` | `has_sub_domain`      |
| SSL Final State               | `{-1, 0, 1}` | `ssl_state`           |
| Domain Registration Length    | `{-1, 0, 1}` | `long_domain`         |
| Favicon                       | `{1, 0}`     | `favicon`             |
| Is Standard Port              | `{1, 0}`     | `port`                |
| Uses HTTPS Token              | `{1, 0}`     | `https_token`         |
| Request URL                   | `{1, -1}`    | `req_url`             |
| Abnormal URL Anchor           | `{-1, 0, 1}` | `url_of_anchor`       |
| Links in Tags                 | `{1, -1, 0}` | `tag_links`           |
| SFH (Server Form Handler)     | `{-1, 1}`    | `SFH`                 |
| Submitting to Email           | `{1, 0}`     | `submit_to_email`     |
| Abnormal URL                  | `{1, 0}`     | `abnormal_url`        |
| Redirect                      | `{1, 0}`     | `redirect`            |
| On Mouse Over                 | `{1, 0}`     | `mouseover`           |
| Right Click Disabled          | `{1, 0}`     | `right_click`         |
| Pop-up Window                 | `{1, 0}`     | `popup`               |
| Iframe Usage                  | `{1, 0}`     | `iframe`              |
| Age of Domain                 | `{-1, 0, 1}` | `domain_age`          |
| DNS Record                    | `{1, 0}`     | `dns_record`          |
| Web Traffic                   | `{-1, 0, 1}` | `traffic`             |
| Page Rank                     | `{-1, 0, 1}` | `page_rank`           |
| Google Index                  | `{1, 0}`     | `google_index`        |
| Links Pointing to Page        | `{1, 0, -1}` | `links_to_page`       |
| Statistical Report            | `{1, 0}`     | `stats_report`        |
| **Target (Label)**            | `{1, -1}`    | `result`              |

> ℹ️ Binary values denote presence (1) or absence (0). Three-class values usually reflect the strength or severity of the feature (e.g., low, medium, high).

---

## 🛠️ Technologies Used

- Python
- Scikit-learn
- Pandas / NumPy
- MongoDB Atlas
- MLFlow
- FastAPI

---

## 🚀 How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/NetworkSecurity.git
cd NetworkSecurity


### 2. Install Dependencies
```bash
pip install -r requirements.txt

### 3. Run the Script
```bash
python app.py


