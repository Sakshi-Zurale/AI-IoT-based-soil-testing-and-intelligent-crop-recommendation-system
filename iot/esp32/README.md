# ESP32 IoT Setup

Hardware:
- ESP32
- RS485/MAX485
- NPK Modbus sensor
- DHT11 or DHT22
- Soil moisture sensor

IMPORTANT:
The exact NPK sensor model and Modbus register map must be confirmed from the sensor datasheet before enabling real N/P/K register reads. The firmware below keeps the Modbus register section clearly isolated and does not claim unknown addresses.

Configure:
- WIFI_SSID
- WIFI_PASSWORD
- BACKEND_URL
- DEVICE_ID
- FARMER_ID

For first software testing, use the dashboard's Developer Sensor Simulator instead of pretending simulator values are real sensor values.
