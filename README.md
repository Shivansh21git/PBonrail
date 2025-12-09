# 🌾 Plant Buddy

**Plant Buddy** is a smart IoT-based soil monitoring system that helps users track essential parameters like **NPK levels** and **moisture** via a user-friendly web dashboard. Built for farmers, researchers, and agri-tech enthusiasts, it empowers you with real-time insights into soil and plant health.

---

## 🚀 Features

- 🔐 User registration, login, and logout system
- 📋 Dashboard with user-specific device listings
- 📡 MQTT-based real-time data ingestion
- 🧠 InfluxDB time-series database for sensor data
- 📊 View latest NPK and moisture values per device
- 🌐 Local development ready, cloud scalable
- ♻️ Modular and maintainable architecture

---

## 🛠️ Tech Stack

| Layer        | Technology             |
|--------------|------------------------|
| Backend      | Django (Python)        |
| Database     | InfluxDB               |
| Messaging    | MQTT (paho-mqtt)       |
| Frontend     | HTML, CSS              |
| Dev Tools    | Git, MQTTBox, VS Code  |

---

## 📁 Project Structure

Plant-Buddy/
├── backend/ # Django project configuration
├── core/ # App logic: models, views, forms, templates
    ├── templates/core/ # HTML templates
    ├── static/core/ # Custom CSS
├── pbenv/ # Python virtual environment (ignored by Git)
├── mqtt_receiver.py # Script to subscribe to MQTT and write to InfluxDB
├── .env # Optional environment variables
├── requirements.txt
└── manage.py


## ⚙️ Getting Started

### ✅ 1. Clone the repository

bash
git clone https://github.com/your-username/Plant-Buddy.git
cd Plant-Buddy

 ## 🐍 **Set up virtual environment**

python -m venv pbenv
# Activate the environment:
# On Windows:
pbenv\Scripts\activate
# On Linux/macOS:
source pbenv/bin/activate

**Install dependencies**
pip install -r requirements.txt


📡 **MQTT Data Flow**

{
  "device_id": "ks-001",
  "moisture": 48.5,
  "N": 63.2,
  "P": 44.1,
  "K": 55.9
}

