# KrushiAI — Module 1
## AI-IoT Based Soil Testing and Crop Recommendation

A complete local full-stack implementation for:
**Intelligent Soil Analysis and AI-Assisted Crop Recommendation**

### Stack
- Frontend: React + Vite + Tailwind CSS + Axios + Recharts
- Backend: FastAPI + SQLAlchemy + Pydantic
- Database: SQLite by default; MySQL supported through `DATABASE_URL`
- ML: scikit-learn Random Forest
- RAG: local TF-IDF retrieval over agricultural knowledge documents
- AI explanation: local deterministic explanation engine; optional LLM hook can be added later
- Reports: ReportLab PDF
- IoT: ESP32 + RS485/MAX485 + NPK + DHT + soil moisture
- Developer sensor simulator included

### Important data policy
The application does not invent farmer, sensor, GPS, weather, or test-history values.
When real values are unavailable it displays an empty/waiting state.
The bundled ML dataset is explicitly a **demo/training dataset** so the project can run offline. Replace it with a validated agricultural dataset before making real agronomic decisions.

---

# Windows quick start

## 1. Backend

Open PowerShell in this folder:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.ml.train
pytest
uvicorn app.main:app --reload
```

Backend:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

Keep this terminal open.

## 2. Frontend

Open a second PowerShell:

```powershell
cd frontend
npm install
npm run dev
```

Open:
http://localhost:5173

## 3. Database

No MySQL installation is required for the first run.
The project defaults to:

```text
backend/krushiai.db
```

To use MySQL later, set:

```env
DATABASE_URL=mysql+pymysql://USER:PASSWORD@localhost:3306/krushiai
```

## 4. Demo sensor

The dashboard contains a developer-only sensor simulator.
It sends clearly labelled simulated readings to the backend.

For actual hardware, see:
`iot/esp32/README.md`

---

# End-to-end demo flow

1. Create farmer profile.
2. Start a manual soil test OR use the developer sensor simulator.
3. Save soil test.
4. Run soil analysis.
5. Enter/confirm location.
6. Fetch weather if internet is available; otherwise continue without weather.
7. Run crop recommendation.
8. Review preferred crop comparison.
9. Generate PDF report.
10. Open Test History.

---

# API highlights

- GET `/api/health`
- GET `/api/system/status`
- POST `/api/farmers`
- GET `/api/farmers/{farmer_id}`
- POST `/api/soil/manual`
- POST `/api/soil/read`
- POST `/api/soil/analyze`
- POST `/api/weather/fetch`
- POST `/api/crop/recommend`
- POST `/api/soil-tests/{test_id}/report`
- GET `/api/soil-tests`
- GET `/api/soil-tests/{test_id}`
- POST `/api/dev/simulate-soil-reading`

Swagger:
http://localhost:8000/docs

---

# Architecture

```text
                 ┌─────────────────────┐
                 │     React UI        │
                 └──────────┬──────────┘
                            │ REST
                 ┌──────────▼──────────┐
                 │     FastAPI         │
                 ├─────────────────────┤
                 │ Farmer / Soil APIs  │
                 │ Weather / Reports   │
                 │ ML / RAG / AI       │
                 └───────┬─────┬───────┘
                         │     │
                ┌────────▼─┐ ┌─▼─────────────┐
                │ Database │ │ Random Forest │
                └──────────┘ └──────┬────────┘
                                    │
                               ┌────▼────┐
                               │   RAG   │
                               └────┬────┘
                                    │
                               AI Explanation

ESP32 → RS485/MAX485 → Wi-Fi → FastAPI
```
