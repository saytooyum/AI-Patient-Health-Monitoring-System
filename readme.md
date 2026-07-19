# 🏥 Intelligent Patient Health Monitoring System

An IoT-based Patient Health Monitoring System that enables real-time monitoring of patients using ESP32 and biomedical sensors. The system provides a web-based dashboard for healthcare professionals to monitor vital signs, manage patient records, receive alerts for abnormal conditions, and generate patient reports.

---

## 📌 Overview

The Intelligent Patient Health Monitoring System is designed to assist healthcare professionals by continuously monitoring patient vital signs and presenting them through an intuitive web dashboard.

The project combines **IoT**, **Embedded Systems**, **Web Development**, and **Database Management** to create an efficient patient monitoring platform.

---

## ✨ Features

- 👨‍⚕️ Secure Doctor Login System
- 📊 Interactive Dashboard
- 👤 Patient Management
- ❤️ Heart Rate Monitoring
- 🌡️ Body Temperature Monitoring
- 📈 Real-Time Vital Sign Charts
- 🚨 Critical Patient Alerts
- ⚠️ Patient Priority Queue
- 📋 AI-Based Health Summary (Upcoming)
- 📄 Patient Report Generation (Upcoming)
- 💾 MySQL Database Integration
- 📡 ESP32 Sensor Integration
- 🔒 Secure Authentication

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js

### Database
- MySQL

### Hardware
- ESP32
- MAX30100 Pulse Oximeter Sensor
- LM35 Temperature Sensor
- AD8232 ECG Sensor

---

## 📂 Project Structure

```text
AI-Patient-Health-Monitoring-System/
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── monitoring.py
│   ├── patients.py
│   ├── reports.py
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── esp32/
```

---

## 🏗️ System Architecture

```text
Biomedical Sensors
        │
        ▼
      ESP32
        │
        ▼
 Flask Application
        │
        ▼
   MySQL Database
        │
        ▼
Interactive Dashboard
        │
        ▼
 Healthcare Professional
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/saytooyum/AI-Patient-Health-Monitoring-System.git
```

### 2. Navigate to the Project Folder

```bash
cd AI-Patient-Health-Monitoring-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

### 6. Configure the Database

Create a MySQL database and update your database credentials inside `config.py`.

### 7. Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 📷 Screenshots

### Login Page

*Coming Soon*

### Dashboard

*Coming Soon*

### Patient Management

*Coming Soon*

### Live Monitoring

*Coming Soon*

### Critical Alerts

*Coming Soon*

---

## 🔮 Future Enhancements

- AI-Based Patient Risk Prediction
- PDF Report Generation
- Email Notifications
- SMS Alerts
- Cloud Deployment
- Mobile Application
- Machine Learning-Based Health Analysis

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests to improve the project.

---

## 👨‍💻 Author

**Satyam Raina**

B.Tech Computer Science & Engineering

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

---

## 📄 License

This project is licensed under the MIT License.