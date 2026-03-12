# 🦎 GeckoScope con selector de salida (HDMI / Analog / etc)
import sys, subprocess, numpy as np, sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

import sounddevice as sd

def list_monitors():
    """
    Devuelve una lista de nombres de dispositivos de entrada para el QComboBox.
    Mantiene una lista paralela de índices para usar en sd.InputStream.
    """
    #print(sd.query_devices())
    try:
        devices = sd.query_devices()
        # Filtrar dispositivos con entrada (> 0 canales) o el dispositivo por defecto
        input_devices = [
            (i, device['name'])
            for i, device in enumerate(devices)
            if device['max_input_channels'] > 0 or device['name'] == 'default'
        ]
        # Separar nombres para el QComboBox y mantener índices para el stream
        names = [name for _, name in input_devices]
        indices = [index for index, _ in input_devices]
        for salidas in input_devices:
            print(salidas)
        return names, indices
    except Exception as e:
        print("⚠️ No se pudieron listar dispositivos:", e)
        return ["default"], [0]
    
    
class GeckoScope(QWidget):
#class GeckoScope(QMainWindow):
    def __init__(self, samplerate=44100, blocksize=1024):
        super().__init__()
        self.setWindowTitle("🦎 GeckoScope Selector v0.3")
        self.resize(900, 700)

        # Parámetros de audio
        self.samplerate = samplerate
        self.blocksize = blocksize

        # Layout principal
        #central = QWidget()
        #self.setCentralWidget(central)
        layout = QVBoxLayout(self)

        # ----- Selector de salida -----
        self.label = QLabel("🎧 Seleccioná salida de audio:")
        layout.addWidget(self.label)
        self.selector = QComboBox()
        #self.monitors = list_monitors()
        self.monitors, self.monitor_indices = list_monitors()  # Obtener nombres e índices
        self.selector.addItems(self.monitors) 
        layout.addWidget(self.selector)
        self.selector.currentIndexChanged.connect(self.change_device)

        # ----- Osciloscopio -----
        self.osc_plot = pg.PlotWidget(title="Osciloscopio Geckoniano")
        self.osc_plot.showGrid(x=True, y=True, alpha=0.5)
        self.osc_curve = self.osc_plot.plot(pen=pg.mkPen("lime", width=1.5))
        layout.addWidget(self.osc_plot)

        # ----- Espectro -----
        self.fft_plot = pg.PlotWidget(title="Espectro Geckoniano")
        self.fft_plot.showGrid(x=True, y=True, alpha=0.5)
        self.fft_curve = self.fft_plot.plot(pen=pg.mkPen("yellow", width=2))
        layout.addWidget(self.fft_plot)

        # Buffer inicial
        self.data = np.zeros(self.blocksize)

        # Iniciar con el primer monitor
        self.current_device = self.monitors[0]
        self.current_device_index = 9
        self.start_stream()

        # Timer para actualizar gráficos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(20)  # ~50 FPS

    def start_stream(self):
        try:
            if hasattr(self, "stream"):
                self.stream.stop()
                self.stream.close()
            #print(f"🎧 Capturando desde: {self.current_device}")
            print(f"🎧 Capturando desde: {self.monitors[self.monitor_indices.index(self.current_device_index)]} (índice: {self.current_device_index})")
            self.stream = sd.InputStream(
                #device=self.current_device,
                device=self.current_device_index,  # Usa índice en lugar de nombre
                channels=1,
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                callback=self.audio_callback
            )
            self.stream.start()
        except Exception as e:
            print("⚠️ Error al iniciar stream:", e)

    def change_device(self, idx):
        #self.current_device = self.monitors[idx]
        self.current_device_index = self.monitor_indices[idx]  # Usa índice en lugar de nombre
        self.start_stream()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        self.data = indata[:, 0]

    def update_plots(self):
        # Osciloscopio
        self.osc_curve.setData(self.data)

        # FFT
        fft = np.abs(np.fft.rfft(self.data)) / self.blocksize
        freqs = np.fft.rfftfreq(self.blocksize, 1.0 / self.samplerate)
        self.fft_curve.setData(freqs, fft)

    # Agregar al final de la clase para cerrar el stream:
    def closeEvent(self, event):
        if hasattr(self, "stream"):
            self.stream.stop()
            self.stream.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeckoScope()
    ventana.show()
    sys.exit(app.exec_())
