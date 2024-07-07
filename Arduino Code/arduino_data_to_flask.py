import serial
import requests
import re

# Connect to Arduino
ser = serial.Serial('/dev/cu.usbmodem101', 9600)  # Adjust serial port as needed

# Flask server URL
FLASK_SERVER_URL = 'http://localhost:5010/data'  # Adjust URL as needed

# Initialize temperature and humidity variables
temperature = None
humidity = None

while True:
    # Read data from Arduino
    data = ser.readline().decode().strip()
    print("Data from Arduino:", data)
    
    # Use regular expressions to extract temperature and humidity
    temperature_match = re.match(r'Temperature\s*=\s*([\d.]+)', data)
    humidity_match = re.match(r'Humidity\s*=\s*([\d.]+)', data)

    if temperature_match:
        temperature = temperature_match.group(1)
    elif humidity_match:
        humidity = humidity_match.group(1)
    
    # If both temperature and humidity are received, send data to Flask server
    if temperature is not None and humidity is not None:
        payload = {'temperature': temperature, 'humidity': humidity}
        try:
            response = requests.post(FLASK_SERVER_URL, json=payload)
            print("Response from Flask server:", response.text)
            # Reset temperature and humidity variables
            temperature = None
            humidity = None
        except Exception as e:
            print("Error sending data to Flask server:", e)