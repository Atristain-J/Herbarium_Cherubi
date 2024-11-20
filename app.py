
from flask import Flask, request, jsonify
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep

# Configurar el sensor de temperatura y humedad
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # Pin GPIO donde está conectado el sensor DHT22

# Configurar pines GPIO para los relés
RELAY_PINS = [17, 27, 22, 5]  # Pines GPIO para los 4 relés
GPIO.setmode(GPIO.BCM)
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Inicializar Flask
app = Flask(__name__)

def read_adc(channel):
    """Simula la lectura de un sensor analógico (como pH)."""
    # Implementación real dependería del ADC que estés usando
    # Aquí simplemente se retorna un valor ficticio para demostración
    return 512

@app.route('/')
def index():
    """Devuelve los datos de los sensores en formato JSON."""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    ph_value = read_adc(0)

    return jsonify({
        "temperature": round(temperature, 2) if temperature else "Error",
        "humidity": round(humidity, 2) if humidity else "Error",
        "ph_value": round((ph_value / 1023) * 14, 2)  # Convertir a escala de pH
    })

@app.route('/control', methods=['POST'])
def control_relay():
    """Controla los relés para encender o apagar los focos."""
    try:
        relay = int(request.form.get("relay"))
        action = request.form.get("action")

        if relay < 0 or relay >= len(RELAY_PINS):
            return "Relé inválido", 400

        if action == "on":
            GPIO.output(RELAY_PINS[relay], GPIO.HIGH)
        elif action == "off":
            GPIO.output(RELAY_PINS[relay], GPIO.LOW)
        else:
            return "Acción inválida", 400

        return "OK", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
