import httpx

async def fetch_weather(latitude, longitude):
    if latitude is None or longitude is None:
        return None, "Location coordinates were not supplied."
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "hourly": "precipitation",
        "forecast_days": 1
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json()
        current = data.get("current", {})
        hourly = data.get("hourly", {})
        rain = 0.0
        if hourly.get("precipitation"):
            rain = float(hourly["precipitation"][0] or 0)
        code = current.get("weather_code")
        condition = f"Weather code {code}" if code is not None else "Unavailable"
        return {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "rainfall": rain,
            "weather_condition": condition,
            "source": "Open-Meteo"
        }, None
    except Exception as exc:
        return None, str(exc)
