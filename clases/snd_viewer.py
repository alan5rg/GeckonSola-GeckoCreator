# 🦎 Osciloscopio + Espectro (NOva DulceKAli en modo NOvaPythoniza)
import sys, numpy as np, sounddevice as sd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

class GeckoScope(QMainWindow):
    def __init__(self, samplerate=44100, blocksize=1024):
        super().__init__()
        self.setWindowTitle("🦎 GeckoScope Prototipo v0.1")
        self.resize(800, 600)

        # Parámetros de audio
        self.samplerate = samplerate
        self.blocksize = blocksize

        # Layout principal
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

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

        # Captura de audio
        self.stream = sd.InputStream(channels=1, samplerate=self.samplerate,
                                     blocksize=self.blocksize, callback=self.audio_callback)
        self.stream.start()

        # Timer para actualizar gráficos
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(20)  # ~50 FPS

    def audio_callback(self, indata, frames, time, status):
        if status: print(status)
        self.data = indata[:, 0]  # 1 canal

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
