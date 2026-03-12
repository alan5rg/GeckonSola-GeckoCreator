# 🦎 GeckoScope: Osciloscopio + Espectro sobre salida principal
import sys, subprocess, numpy as np, sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import sounddevice as sd

def get_default_monitor():
    """
    Devuelve el nombre del dispositivo monitor de la salida principal (PulseAudio/PipeWire).
    """
    try:
        # Detectar el sink por defecto
        sink = subprocess.check_output(
            ["pactl", "get-default-sink"], text=True
        ).strip()
        return sink + ".monitor"
    except Exception as e:
        print("⚠️ No se pudo detectar salida default, usando 'default'")
        return "default"

class GeckoScope(QMainWindow):
    def __init__(self, samplerate=44100, blocksize=1024):
        super().__init__()
        self.setWindowTitle("🦎 GeckoScope Prototipo v0.2")
        self.resize(800, 600)
        
        print(sd.query_devices())

        # Parámetros de audio
        self.samplerate = samplerate
        self.blocksize = blocksize

        # Layout principal
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # ----- Osciloscopio -----
        self.osc_plot = pg.PlotWidget(title="Osciloscopio Geckoniano")
        self.osc_plot.setLabel("left", "Amplitud")
        self.osc_plot.setLabel("bottom", "Muestras")
        self.osc_plot.showGrid(x=True, y=True, alpha=0.5)
        self.osc_curve = self.osc_plot.plot(pen=pg.mkPen("lime", width=1.5))
        layout.addWidget(self.osc_plot)

        # ----- Espectro -----
        self.fft_plot = pg.PlotWidget(title="Espectro Geckoniano")
        self.fft_plot.setLabel("left", "Magnitud")
        self.fft_plot.setLabel("bottom", "Frecuencia (Hz)")
        self.fft_plot.showGrid(x=True, y=True, alpha=0.5)
        self.fft_curve = self.fft_plot.plot(pen=pg.mkPen("yellow", width=2))
        layout.addWidget(self.fft_plot)

        # Buffer inicial
        self.data = np.zeros(self.blocksize)

        # Captura de audio desde monitor de salida
        self.device = get_default_monitor()
        print(f"🎧 Capturando desde: {self.device}")
        self.stream = sd.InputStream(
            #device=self.device,
            device= 10, 
            channels=1,
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            callback=self.audio_callback
        )
        self.stream.start()

        # Timer para actualizar gráficos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(20)  # ~50 FPS

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("⚠️", status)
        self.data = indata[:, 0]  # primer canal

    def update_plots(self):
        # Osciloscopio (forma de onda)
        self.osc_curve.setData(self.data)

        # FFT (espectro)
        fft = np.abs(np.fft.rfft(self.data)) / self.blocksize
        freqs = np.fft.rfftfreq(self.blocksize, 1.0 / self.samplerate)
        self.fft_curve.setData(freqs, fft)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeckoScope()
    ventana.show()
    sys.exit(app.exec_())
