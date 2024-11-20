
import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QWidget
)
from PyQt6.QtCore import QTimer

# Dirección del servidor Flask en la Raspberry Pi
RASPBERRY_PI_URL = "http://<raspberry_ip>:5000"  # Cambia <raspberry_ip> por la IP de tu Raspberry Pi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Sensores y Focos")

        # Crear el diseño principal
        self.main_layout = QVBoxLayout()

        # Sección de sensores
        self.sensor_layout = QVBoxLayout()
        self.sensor_label = QLabel("Lectura de Sensores:")
        self.temperature_label = QLabel("Temperatura: --- °C")
        self.humidity_label = QLabel("Humedad: --- %")
        self.ph_label = QLabel("pH: ---")
        self.sensor_layout.addWidget(self.sensor_label)
        self.sensor_layout.addWidget(self.temperature_label)
        self.sensor_layout.addWidget(self.humidity_label)
        self.sensor_layout.addWidget(self.ph_label)
        self.main_layout.addLayout(self.sensor_layout)

        # Sección de control de focos
        self.foco_layout = QVBoxLayout()
        self.foco_label = QLabel("Control de Focos:")
        self.foco_layout.addWidget(self.foco_label)

        self.buttons = []
        for i in range(4):
            h_layout = QHBoxLayout()
            btn_on = QPushButton(f"Encender Foco {i + 1}")
            btn_off = QPushButton(f"Apagar Foco {i + 1}")
            btn_on.clicked.connect(lambda _, r=i: self.control_foco(r, "on"))
            btn_off.clicked.connect(lambda _, r=i: self.control_foco(r, "off"))
            h_layout.addWidget(btn_on)
            h_layout.addWidget(btn_off)
            self.foco_layout.addLayout(h_layout)
            self.buttons.append((btn_on, btn_off))
        self.main_layout.addLayout(self.foco_layout)

        # Configurar el temporizador para actualizar sensores
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sensors)
        self.timer.start(2000)  # Actualizar cada 2 segundos

        # Configurar el contenedor principal
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def control_foco(self, relay, action):
        """Envía una solicitud al servidor para encender o apagar un foco."""
        try:
            response = requests.post(f"{RASPBERRY_PI_URL}/control", data={"relay": relay, "action": action})
            if response.status_code == 200:
                print(f"Foco {relay + 1} {'encendido' if action == 'on' else 'apagado'} correctamente.")
            else:
                print(f"Error al controlar el foco {relay + 1}: {response.text}")
        except Exception as e:
            print(f"Error de conexión al servidor: {e}")

    def update_sensors(self):
        """Obtiene los datos de los sensores desde la Raspberry Pi."""
        try:
            response = requests.get(RASPBERRY_PI_URL)
            if response.status_code == 200:
                data = response.json()  # Suponiendo que el servidor devuelve JSON
                self.temperature_label.setText(f"Temperatura: {data['temperature']} °C")
                self.humidity_label.setText(f"Humedad: {data['humidity']} %")
                self.ph_label.setText(f"pH: {data['ph_value']}")
            else:
                print(f"Error al obtener los datos de sensores: {response.text}")
        except Exception as e:
            print(f"Error de conexión al servidor: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
