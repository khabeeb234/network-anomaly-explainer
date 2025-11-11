🧾 README.md

Copy-paste this file directly into your project folder (network-anomaly-explainer/README.md):

# 💻 Network Performance Anomaly Explainer (MVP)

> 🧠 AI-powered diagnostics agent that detects, correlates, and explains network performance anomalies.

![screenshot](https://raw.githubusercontent.com/<your-username>/network-anomaly-explainer/main/screenshot.png)

---

## 🚀 Overview

This project is a **hackathon prototype (RH17-2025)** designed to help Network Operations Centers (NOCs) diagnose
performance anomalies faster.

The system uses:
- 🧩 **IsolationForest (ML)** for anomaly detection  
- 🤖 **Gemini 2.5 Flash / Pro** for AI-based root cause explanation  
- 🖥️ **Streamlit** as a simple yet powerful interactive dashboard  
- 🌐 Optional rule-based fallback for environments without API keys  

It provides natural-language diagnostic summaries with correlated configuration or routing events.

---

## 🧩 Features

✅ Detects anomalies from latency, packet loss, and throughput metrics  
✅ Correlates anomalies with router configuration or BGP route updates  
✅ Generates AI explanations using **Gemini 2.5 Flash / Pro**  
✅ Includes Matrix-style “Hacker Console” UI for hackathon demo impact  
✅ Fully local — works offline (with fallback rule-based analysis)

---

## 🧱 Folder Structure



network-anomaly-explainer/
├─ app.py # Streamlit web app
├─ utils.py # Anomaly detection & AI explanation logic
├─ custom_theme.css # Cyber-terminal theme styling
├─ requirements.txt # Python dependencies
├─ sample_data/
│ ├─ network_metrics.csv # Example network telemetry
│ └─ config_changes.csv # Example configuration logs
├─ README.md
└─ .gitignore


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/network-anomaly-explainer.git
cd network-anomaly-explainer

2️⃣ Create a Python virtual environment
python -m venv venv
# Activate it:
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
streamlit run app.py


Then open http://localhost:8501
 in your browser.

🧠 Using Gemini AI (optional)

To enable natural-language explanations via Google’s Gemini models:

Get a free API key from Google AI Studio

Set it as an environment variable before running the app:

Windows PowerShell

$env:GEMINI_API_KEY="your-api-key-here"


Linux/macOS

export GEMINI_API_KEY="your-api-key-here"


In the app, check ✅ “Use Gemini AI for explanations”.

If no key is set, the system gracefully falls back to a rule-based heuristic engine.

🧪 Sample Data

The app includes built-in test data:

Metric	Description
network_metrics.csv	Synthetic telemetry with latency, packet loss, and throughput
config_changes.csv	Example router events (BGP update, ACL change, reboot)

You can upload your own CSVs with similar columns to test real data.

🧰 Technology Stack
Layer	Tools Used
Frontend	Streamlit
ML Engine	scikit-learn (IsolationForest)
AI Engine	Gemini 2.5 Flash / Pro
Data Processing	pandas, numpy
Visualization	Streamlit DataFrames
Styling	Custom CSS (Matrix-style hacker console)
🧑‍💻 How It Works

1️⃣ Anomaly Detection:
IsolationForest identifies spikes in latency, packet loss, and throughput drops.

2️⃣ Correlation:
Each detected anomaly is correlated with configuration or routing events from the same timeframe.

3️⃣ AI Explanation:
Gemini analyzes the metrics + change logs and produces a human-readable diagnosis like:

“Latency spike coincides with a BGP route update. Likely route convergence delay. Verify neighbor stability.”

4️⃣ Verification Steps:
The AI recommends validation steps (e.g., check interface counters, traceroute, QoS drops).

🧮 Example Output
Timestamp: 2025-11-01 10:10:00  
Latency: 210ms | Packet Loss: 5.0% | Throughput: 40Mbps  

Nearby Change Events:
- 2025-11-01 10:09:00 – BGP route update (AS path changed)

AI Explanation:
High latency spike and packet loss detected near a BGP route update.
Likely transient convergence or misconfiguration. Check routing table and interface error counters.
