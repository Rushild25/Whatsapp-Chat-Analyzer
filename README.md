# 📊 WhatsApp Chat Analyzer

A complete end-to-end **WhatsApp Chat Analysis Dashboard** built using **Python, Pandas, Matplotlib, and Streamlit**.

This application allows users to upload exported WhatsApp chat files (`.txt`) and generate interactive analytics including message trends, user activity, timelines, and heatmaps.

---

## 🚀 Features

### 📌 Core Analytics
- Total Messages
- Total Words
- Media Messages Count
- Links Shared Count

### 📈 Time-Based Analysis
- Monthly Message Timeline
- Daily Message Timeline
- Weekly Activity Distribution
- Day × Hour Activity Heatmap

### 👥 User Insights
- Most Active Users (Top N)
- User-specific filtering
- Individual vs Overall analysis

### 🛡 Robust Parsing
- Supports multiple encodings (`utf-8`, `utf-16`, `latin-1`)
- Handles multiline messages
- Handles system notifications
- Handles different date formats
- Supports both 12-hour and 24-hour timestamps

---

# Project Architecture

## Whatsapp Chat Analyzer
```
Whatsapp Chat Analyzer
│
├── app.py 
├── parser.py 
├── helper.py 
├── visualizer.py 
└── README.md
```

## Modular Flow:
```
User Upload 
    ↓
Parser Layer 
    ↓ 
Feature Engineering Layer 
    ↓
Analytics Layer
    ↓ 
Visualization Layer 
    ↓ 
Streamlit UI Rendering
```

---

## 📦 Installation

### 1️⃣ Clone the repository
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer

### 2️⃣ Create a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

### 3️⃣ Install dependencies
pip install -r requirements.txt

### ▶️ Running the Application
streamlit run app.py

---

## 📁 How to Export WhatsApp Chat

1. Open WhatsApp  
2. Open the chat you want to analyze  
3. Tap the three dots (⋮) in the top-right corner  
4. Select **More**  
5. Click **Export Chat**  
6. Choose **Without Media**  
7. Save the exported `.txt` file  
8. Upload the file into the application  

---

## 🛠 Technologies Used

- Python 3.10+
- Pandas
- Matplotlib
- Streamlit
- Regular Expressions (Regex)

---

## 📜 License


This project is open-source and available under the MIT License.

