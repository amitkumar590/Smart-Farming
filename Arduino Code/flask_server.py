from flask import Flask, jsonify, request
import logging

app = Flask(__name__)

# Configure logging to a file
logging.basicConfig(filename='flask_server.log', level=logging.DEBUG)

latest_data = {'temperature': None, 'humidity': None}

@app.route('/data', methods=['POST'])
def receive_data():
    global latest_data
    data = request.json
    logging.debug("Received data: %s", data)
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    logging.debug("Temperature: %s, Humidity: %s", temperature, humidity)
    
    # Update latest data
    latest_data['temperature'] = temperature
    latest_data['humidity'] = humidity
    
    return "Data received successfully", 200

@app.route('/')
def index():
    global latest_data
    return jsonify(latest_data)

if __name__ == '__main__':
    logging.debug("Starting Flask server")
    app.run(host='0.0.0.0', port=5010, debug=True)