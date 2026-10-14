from pathlib import Path
import re

KNOWLEDGE = [
    ("General crop requirements", "Crop suitability depends on soil nutrients, moisture, temperature, humidity, local climate and crop-specific agronomic requirements."),
    ("Rice", "Rice generally requires adequate moisture and warm growing conditions. Suitability should be confirmed against local agronomic guidance."),
    ("Wheat", "Wheat is generally associated with cooler growing conditions than warm-season crops. Soil and seasonal conditions should be considered."),
    ("Maize", "Maize performance depends on adequate nutrients, moisture and suitable temperature during growth."),
    ("Cotton", "Cotton is sensitive to temperature, moisture and soil conditions; local recommendations should be consulted before planting."),
    ("Sugarcane", "Sugarcane has a long crop duration and substantial water requirements. Local water availability is important."),
    ("Groundnut", "Groundnut requires suitable drainage and moisture conditions. Soil texture and nutrient status should be evaluated."),
    ("Soybean", "Soybean requires suitable moisture, temperature and nutrient conditions and should be evaluated against the local season."),
    ("Chickpea", "Chickpea is commonly grown in cooler seasons and should be evaluated using local soil and seasonal conditions."),
    ("Tomato", "Tomato performance depends on nutrient availability, temperature, moisture and disease-management practices."),
    ("Onion", "Onion suitability depends on soil condition, moisture management and seasonal temperature."),
]

def retrieve(crops, query, k=4):
    q = set(re.findall(r"[a-z]+", query.lower()))
    scored = []
    for title, text in KNOWLEDGE:
        words = set(re.findall(r"[a-z]+", (title + " " + text).lower()))
        score = len(q & words)
        for crop in crops:
            if crop.lower() in text.lower() or crop.lower() in title.lower():
                score += 2
        scored.append((score, title, text))
    scored.sort(reverse=True)
    return [{"title": x[1], "text": x[2]} for x in scored[:k]]
