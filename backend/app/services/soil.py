REFERENCE_RANGES = {
    "nitrogen": (20, 80),
    "phosphorus": (15, 60),
    "potassium": (20, 80),
    "soil_moisture": (25, 75),
    "air_temperature": (15, 35),
    "humidity": (30, 85),
}

def classify(name, value):
    low, high = REFERENCE_RANGES[name]
    if value < low:
        status = "Low"
    elif value > high:
        status = "High"
    else:
        status = "Normal"
    interpretations = {
        "Low": "Below the configured reference range.",
        "Normal": "Within the configured reference range.",
        "High": "Above the configured reference range.",
    }
    return {"value": value, "status": status, "interpretation": interpretations[status]}

def analyze(test):
    return {
        "test_id": test.test_id,
        "parameters": {
            "nitrogen": classify("nitrogen", test.nitrogen),
            "phosphorus": classify("phosphorus", test.phosphorus),
            "potassium": classify("potassium", test.potassium),
            "soil_moisture": classify("soil_moisture", test.soil_moisture),
            "air_temperature": classify("air_temperature", test.air_temperature),
            "humidity": classify("humidity", test.humidity),
        }
    }
