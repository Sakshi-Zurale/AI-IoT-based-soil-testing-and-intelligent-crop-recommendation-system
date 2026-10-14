# KrushiAI Module 1 Architecture

## Flow

Farmer Details
→ Soil Test
→ Soil Analysis
→ Location
→ Weather
→ Random Forest
→ RAG
→ AI Explanation
→ Recommendation
→ PDF Report
→ History

## Data ownership

- React: presentation and user interaction
- FastAPI: validation, orchestration and APIs
- SQLAlchemy: database persistence
- Random Forest: structured crop prediction
- RAG: agricultural context retrieval
- Local AI explanation layer: evidence-based wording
- ESP32: sensor gateway
- ReportLab: PDF generation

## Production note

The bundled ML dataset is only for local software demonstration. It must be replaced and scientifically evaluated before real agricultural deployment.
