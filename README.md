
## AI-IoT Based Soil Testing and Crop Recommendation
### 🚜 Smart Farming • Intelligent Soil • Better Crop Decisions

<p align="center">
  <strong>🌾 From Soil Testing to AI-Powered Crop Recommendations 🌾</strong>
</p>

<p align="center">
  An AI + IoT-based smart agriculture system that helps farmers understand soil conditions and make informed crop decisions.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI-Machine%20Learning-2E7D32?style=for-the-badge" alt="AI and Machine Learning">
  <img src="https://img.shields.io/badge/IoT-ESP32-1565C0?style=for-the-badge" alt="IoT ESP32">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge" alt="FastAPI">
  <img src="https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge" alt="React">
  <img src="https://img.shields.io/badge/Domain-Smart%20Agriculture-8BC34A?style=for-the-badge" alt="Smart Agriculture">
</p>

---

## 🌾 About the Project

**KrushiAI** combines soil sensing, machine learning, and intelligent analysis to support data-driven farming.

Farmers can enter soil values manually or use a developer sensor simulator to explore soil analysis and crop recommendations.

### 🌿 Key Features

- 🧪 **Soil Testing:** Capture Nitrogen (N), Phosphorus (P), Potassium (K), moisture, temperature, and humidity.
- 📡 **IoT Integration:** Designed for ESP32 and RS485/MAX485-based soil sensor integration.
- 🤖 **AI Crop Recommendation:** Random Forest model for crop prediction.
- 🌦️ **Weather & Location:** Supports weather data retrieval and location-aware analysis.
- 🧠 **Agricultural Knowledge:** Local TF-IDF-based retrieval and AI-assisted explanations.
- 📄 **PDF Reports:** Generate downloadable soil analysis and crop recommendation reports.
- 👨‍🌾 **Farmer Management:** Maintain farmer profiles and soil-test history.
- 🖥️ **Sensor Simulation:** Test the workflow without physical hardware.

---

## 🧪 Soil Intelligence — NPK

| Nutrient | Full Form | Why It Matters |
|---|---|---|
| 🟢 **N** | Nitrogen | Supports leafy and vegetative growth |
| 🟠 **P** | Phosphorus | Supports root development and energy transfer |
| 🔵 **K** | Potassium | Supports plant health and stress tolerance |

Additional readings include 🌡️ temperature, 💧 soil moisture, and 💨 humidity.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| 🎨 Frontend | React, Vite, Tailwind CSS, Axios, Recharts |
| ⚙️ Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| 🧠 Machine Learning | scikit-learn, Random Forest |
| 🔎 Knowledge Retrieval | TF-IDF |
| 🗄️ Database | SQLite by default; MySQL supported through configuration |
| 📡 Hardware | ESP32, RS485/MAX485, NPK sensor, DHT sensor, soil moisture sensor |
| 📑 Reports | ReportLab PDF |

---

## 🏗️ System Architecture

```text
👨‍🌾 Farmer
    │
    ▼
🖥️ React Frontend
    │
    ▼
⚙️ FastAPI Backend
    │
    ├── 🧪 Soil Analysis (NPK + Environmental Data)
    ├── 🌦️ Weather & Location
    ├── 🤖 Random Forest Crop Prediction
    ├── 🧠 Agricultural Knowledge Retrieval
    ├── 📄 PDF Report Generation
    └── 🗄️ Farmer & Soil-Test Records

📡 ESP32 + Soil Sensors ──► FastAPI
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 recommended
- Node.js and npm
- Git

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/KrushiAI-Module1.git
cd KrushiAI-Module1
```

### 2️⃣ Start the Backend

Open PowerShell in the project directory:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.ml.train
uvicorn app.main:app --reload
```

Backend API: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### 3️⃣ Start the Frontend

Open a second terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the application at `http://localhost:5173`.

### 4️⃣ Configure Environment Variables

Use the example files as templates:

- Root: `.env.example`
- Frontend: `frontend/.env.example`

Configure local settings as needed. **Never commit real API keys, passwords, or private credentials.**

### 5️⃣ Explore the Workflow

1. 👨‍🌾 Create a farmer profile.
2. 🧪 Enter soil values or use the sensor simulator.
3. 📊 Analyze soil conditions.
4. 🌦️ Provide or confirm location details.
5. 🤖 Generate a crop recommendation.
6. 📄 Download the soil-test report.
7. 📚 Review soil-test history.

---

## 📁 Project Structure

```text
KrushiAI-Module1/
├── backend/       # FastAPI, ML, database, reports
├── frontend/      # React + Vite application
├── iot/           # ESP32 and sensor integration
├── docs/          # Project documentation
├── .env.example   # Backend configuration template
├── .gitignore
├── README.md
├── run_backend.ps1
└── run_frontend.ps1
```

---

## ⚠️ Important Disclaimer

- 🌱 The bundled ML dataset is for demonstration and training.
- 🤖 Crop recommendations are decision-support suggestions, not guaranteed agricultural advice.
- 🧪 Validate the model using reliable, region-specific agricultural data before real-world use.
- 📡 Real hardware readings depend on compatible sensors, calibration, and integration.
- 🔐 Do not publish real farmer records, local databases, API keys, or personal information.

---

## 🔮 Project Vision

**From Soil Data to Smarter Farming. 🌱**

KrushiAI aims to make agricultural technology more accessible by combining IoT sensing, machine learning, and farmer-friendly decision support.

<p align="center">
  🌾 🧪 🤖 📡 🌱
  <br>
  <strong>KrushiAI — Growing Intelligence for Agriculture</strong>
</p>

