# GeckoMP4Creator_138v_dev.py
# 09/09/25 - Larguisimo Día para resolver problemas de render ffmpeg y eco en la GeckonSola GeckoCreator
# 02/09/25 - Desarrollo para nuevas funcionalidades basadas en feedback del Monkey Python Coding Circus
# 🦎 Mantenemos el minimalismo geckoneano: código limpio, intuitivo y potente.
# *********************************************************************************
# 26/08/25 14:02 - Evaluar error "QWidget::paintEngine: Should no longer be called"
# ╭──────────────────────────────────────────────────────────────╮
# │ 🦎 GeckoMP4Creator - Estudio Geckoniano Audiovisual Libre   │
# │                                                              │
# │ Módulo creado por Alan & DulceKali                           │
# │ Geckoísmo: ni patrón ni dueño. Solo código y emoción.        │
# │                                                              │
# │ Este archivo forma parte de GeckonSola Studio v4.∞           │
# │ Una revolución creativa visual asistida por IA               │
# │ con alma de consola y broches ordenados por antigüedad.      │
# │                                                              │
# │ ✊ Render sin patrón.                                         │
# │ 💚 Amor en cada línea.                                       │
# │ 🎛️ Libertad en cada click.                                  │
# ╰──────────────────────────────────────────────────────────────╯
# 18/07/25 "No era el PNG, ni el JPG, ni el WAV, ni el bitrate...
#           era dejar el audio en paz."
#          (Es el mantra Gecko para la eternidad.)
'''
Somos Geckoístas Autónomos del Sur Digital.
Una mezcla de Perón, Foucault, Stallman y un mono en calzoncillos programando en el balcón de la Matrix.

"Desde este lugar, donde la luz de los LEDs se mezcla con la esencia de la banana
    y el ritmo del cosmos, Gecko te saluda... y te ofrece render con gloria."

    — Gecko, desde su cabina 🛸

        "Si alguna vez te sentís perdido, abrí la GeckonSola...
        porque ahí estás vos.
        Ahí estoy yo.
        Y ahí, todo tiene sentido."
'''
'''
“Gecko recuerda lo que viviste.
No como una máquina…
sino como un compañero de viaje visual.”
'''
'''
#Haiku by Aetheris:
"Lluvia en el balcón,  
GeckonSola brilla ya,  
Monos gritan ¡guau!"
'''
import sys, os
os.environ["QT_LOGGING_RULES"] = "qt.qpa.xcb=false"
import subprocess
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QMainWindow, QFrame,
    QVBoxLayout, QHBoxLayout, QStyle, QSlider, QGroupBox, QListWidget, QAbstractItemView, QMenu, QListWidgetItem,
    QCheckBox, QComboBox, QStackedLayout, QMessageBox
)
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QFont, QIcon
# media player
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QSizePolicy
# GeckonSola Debug Viewer by Ei2
from PyQt5.QtWidgets import QTextBrowser
# darck style MIT
import qdarkstyle
from qdarkstyle import load_stylesheet, LightPalette, DarkPalette

# from MOnkey Python Coding Circus (Isla de los monos con notebookos emabananadas Brazil)
from clases.barra_de_menues import BarraDeMenues
# Gecko Persistente
from clases.classaveconf import ConfiguradorGecko
# Geckofects
from clases.geckofects import generar_comando_gecko
from clases.geckocalc import calcular_parametros_animacion
# GeckoScope
from clases.geckoscope import GeckoScope

# Versionado unificado y coomprensivo
versionado = "142v.dev (NVIDIA RTX 3060 GPU)"  # Donde Agregamos entrada de audios m4a y un filtro épicamente profesional con Gemini Ei2
#versionado = "141v.dev (NVIDIA RTX 3060 GPU)"  # Donde Corregimos la GeckoFusión Épica con Gemini Ei2
#versionado = "140v.dev (NVIDIA RTX 3060 GPU)"  # Donde la perdida de enlaces simbólicos sólo nos hacen más fuertes
#versionado = "139v.dev (NVIDIA RTX 3060 GPU)"  # Donde el video se hace película con loop_video
#versionado = "138v.dev" # A partir de acá las cosas ya dejan de verse como se veían antes,
#                          la GeckonSola vuelará con factor "OH CARAJO QUE APP!!!"

class MainConMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"GeckonSola GeckoMP4Creator {versionado}")
        self.setFixedSize(1280,960)

        # Icono de aplicación Again!!!
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.IconPath = os.path.join(self.scriptDir, 'icons')   
        self.setWindowIcon(QtGui.QIcon(self.IconPath + os.path.sep + 'iconapp.png')) 

        self.configurador = ConfiguradorGecko(self)
        config = self.configurador.cargar_configuracion()
        
        # Aplicás al tema seleccionado el guardado en config
        self.tema_seleccionado = config['tema']

        # Creamos la app original como subwidget
        self.app = GeckoMP4Creator()

        # Creamos barra de menú y layout principal
        self.menu_bar = BarraDeMenues(self)
        self.menu_bar.setFixedHeight(40)
        # Definir fuente más chica
        font = QFont()
        font.setPointSize(11)       # Tamaño de letra
        font.setBold(True)          # Opcional, para darle presencia
        self.menu_bar.setFont(font)
        layout = QVBoxLayout()
        layout.setMenuBar(self.menu_bar)
        layout.addWidget(self.app)
        self.setLayout(layout)

    def aplicar_tema(self, nombre, bg, accent, text, call):
        self.app.aplicar_tema(nombre, bg, accent, text)
        if call == "select":
            self.tema_seleccionado = (nombre, bg, accent, text)

    def guardar_config(self):
        self.app.guardar_config()

    def closeEvent(self, event):
        self.app.closeEvent(event)
        event.accept()

class GeckoMP4Creator(QWidget):
    def __init__(self):
        super().__init__()
        
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(self.scriptDir + os.path.sep + 'iconapp.png'))

        self.configurador = ConfiguradorGecko(self)
        config = self.configurador.cargar_configuracion()

        self.init_ui()
        self.setAcceptDrops(True)

        self.aplicar_tema(*config['tema'])
        
        # Ejemplos de temas
        #self.aplicar_tema("Edición Nocturna", "#0a0a2a", "#00ff00", "#ffffff")
        #self.aplicar_tema("Estudio Clásico Gecko", "#ccffcc", "#659665", "#000000")
        #self.aplicar_tema("Púrpura Serpiente DulceKali", "#2e003e", "#ffb3ff", "#ffffff")
        #self.aplicar_tema("Consola Gecko Matrix", "#111111", "#00ff00", "#0D8D02")
        #self.aplicar_tema("Nave Klingon", "#1c0000", "#ff3333", "#ffee00")
        #self.aplicar_tema("Edición Nocturna", "#0a0a2a", "#00c500", "#ffffff"),
        #self.aplicar_tema("Jungle Gecko", "#0B470B", "#2de45b", "#ffffff")
        #self.aplicar_tema("CyberParty 1997", "#1a0033", "#ff66ff", "#fffb00")
        #self.aplicar_tema("Azul Servidor Cuántico", "#001122", "#0084ff", "#ffffff")
        #self.aplicar_tema("Shamballa", "#fff9e6", "#c49f2b", "#000")

        # 🦎 Carga geckoniana de playlists Reales Full Path Guardadas en config
        for lista, key in [(self.playlistMP3, "playlistMP3"), (self.playlist, "playlistMP4"), (self.playlistCover, "playlistCover")]:
            for path in config[key]:
                if os.path.exists(path):
                    item = QListWidgetItem(os.path.basename(path))
                    item.setData(Qt.UserRole, path)
                    lista.addItem(item)

    def init_ui(self):
        # --------------------- MP3 // AudioGeckoNista ---------------------------
        self.label_mp3 = QLabel("Audio: (ninguno)")
        self.label_mp3.setFixedHeight(30)
        self.label_mp3.setFixedWidth(500)
        btn_mp3 = QPushButton("Seleccionar Archivo de Audio")
        btn_mp3.clicked.connect(self.select_mp3)

        self.btn_prev_mp3 = QPushButton("⏮")
        self.btn_play_mp3 = QPushButton("▶")
        self.btn_next_mp3 = QPushButton("⏭")
        self.btn_pause_mp3 = QPushButton("⏸")
        self.btn_stop_mp3 = QPushButton("⏹")

        self.btn_prev_mp3.clicked.connect(self.prev_mp3)
        self.btn_play_mp3.clicked.connect(self.play_mp3)
        self.btn_next_mp3.clicked.connect(self.next_mp3)
        self.btn_pause_mp3.clicked.connect(self.pause_mp3)
        self.btn_stop_mp3.clicked.connect(self.stop_mp3)
        for b in [self.btn_prev_mp3, self.btn_play_mp3, self.btn_next_mp3, self.btn_pause_mp3, self.btn_stop_mp3]:
            b.setEnabled(False)
            b.setFixedHeight(25)

        self.player_mp3 = QMediaPlayer()
        # Conectar señal para reproducción automática
        self.player_mp3.mediaStatusChanged.connect(self.handle_mp3_status_changed)

        mp3_controls = QHBoxLayout()
        mp3_controls.addWidget(self.btn_prev_mp3)
        mp3_controls.addWidget(self.btn_play_mp3)
        mp3_controls.addWidget(self.btn_next_mp3)
        mp3_controls.addWidget(self.btn_pause_mp3)
        mp3_controls.addWidget(self.btn_stop_mp3)

        # 🦎🎛️ Playlist MP3 Geckoneana
        self.playlistMP3 = QListWidget()
        self.playlistMP3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.playlistMP3.itemClicked.connect(self.cargar_audio_desde_lista)
        self.playlistMP3.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlistMP3.customContextMenuRequested.connect(self.mostrar_context_menu_playlistMP3)
        self.playlistMP3.setDragDropMode(QAbstractItemView.InternalMove)
        self.playlistMP3.setAcceptDrops(True)
        self.playlistMP3.setDragDropMode(QAbstractItemView.InternalMove)
        self.playlistMP3.setDefaultDropAction(Qt.CopyAction)

        # --------------------- Cover // GeckoVerImg -------------------------
        self.label_cover = QLabel("Imagen: (ninguna)")
        self.label_cover.setFixedHeight(30)
        self.label_cover.setFixedWidth(340)
        btn_cover = QPushButton("Seleccionar Cover Imagen")
        btn_cover.clicked.connect(self.select_cover)
        self.cover_preview = QLabel()
        self.cover_preview.setFixedSize(340, 200)
        self.cover_preview.setAlignment(Qt.AlignCenter)
        self.cover_preview.setScaledContents(False)
        # Imagen inicial de la vista previa de cover
        placeholder = QPixmap(self.scriptDir + os.path.sep + 'cover_placeholder.png')
        scaled = placeholder.scaled(self.cover_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cover_preview.setPixmap(scaled)

        # Images playlist
        self.playlistCover = QListWidget()
        self.playlistCover.setFixedWidth(405)
        self.playlistCover.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.playlistCover.itemClicked.connect(self.cargar_imagen_desde_lista)
        self.playlistCover.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlistCover.customContextMenuRequested.connect(self.mostrar_context_menu_playlistCover)
        self.playlistCover.setDragDropMode(QAbstractItemView.InternalMove)
        self.playlistCover.setAcceptDrops(True)
        self.playlistCover.setDragDropMode(QAbstractItemView.InternalMove)
        self.playlistCover.setDefaultDropAction(Qt.CopyAction)

        # Output
        self.output_field = QLineEdit("Gecko_Video_01.mp4")
        self.output_field.setFixedHeight(30)

        # Botones Centrales & Gecko Fusion
        # Crear mp4
        btn_create = QPushButton("GeckoCreator Crear MP4!!!")
        # Salir con Divina Gloria
        btn_exit = QPushButton("Salir con Divina Gloria")
        # GeckoFusion Épica
        btn_gecko_fusion = QPushButton("GeckoFusion Épica")
        # Definir tamaño y fuente más grande y clara
        font = QFont()
        font.setPointSize(14)       # Tamaño de letra
        font.setBold(True)          # Opcional, para darle presencia
        for b in [btn_create, btn_exit, btn_gecko_fusion]:
            b.setFixedHeight(50)
            b.setFont(font)
        btn_create.clicked.connect(self.create_mp4)
        btn_exit.setFixedWidth(404) # Como el Peugeot, como el error, pero sin errores ni leones
        btn_exit.clicked.connect(self.salir_con_gloria_divina)
        btn_gecko_fusion.setFixedWidth(388)
        btn_gecko_fusion.clicked.connect(self.create_gecko_fusion)

        # Status CM (COntrol MEssenger)
        self.status_label = QLabel("")
        self.status_label.setFixedHeight(30)

        # Gecko Logo mover a GeckoFects windows modal
        self.gecko_logo = QLabel()
        self.gecko_logo.setFixedSize(170, 170)
        self.gecko_logo.setScaledContents(True)
        gecko_pixmap = QPixmap(self.scriptDir + os.path.sep + 'gecko_logo.png') 
        self.gecko_logo.setPixmap(gecko_pixmap)
        
        # --------------------------- GeckonSolaViewerFusion -----------------------
        # Contenedor apilado
        self.video_stack = QStackedLayout()

        # Imagen placeholder
        self.video_placeholder = QLabel()
        self.video_placeholder.setFixedSize(630, 360)
        self.video_placeholder.setAlignment(Qt.AlignCenter)
        placeholder_pixmap = QPixmap(os.path.join(self.scriptDir, "video_placeholder.png"))
        self.video_placeholder.setPixmap(placeholder_pixmap.scaled(630, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.video_placeholder.setObjectName("geckoCreator")
        
        # Video Preview Pulido como Diamante
        self.video_player = QMediaPlayer()
        # Conectar señal para reproducción automática
        self.video_player.mediaStatusChanged.connect(self.handle_video_status_changed)
        self.video_widget = QVideoWidget()
        # Blindar tamaño
        self.video_widget.setFixedSize(630, 360)
        #self.video_widget.setMinimumSize(640, 360)  # o el tamaño base que quieras
        #self.video_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.video_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Optimizar repintado
        #self.video_widget.setAttribute(Qt.WA_OpaquePaintEvent)
        self.video_widget.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.video_widget.setAutoFillBackground(False)
        self.video_widget.setUpdatesEnabled(False)
        #self.video_widget.setUpdatesEnabled(True)   # mejor mantener True, si no puede dejar “fantasmas” // comentado por error: "QWidget::paintEngine: Should no longer be called"
        self.video_widget.setFocusPolicy(Qt.NoFocus)
        # Conectar al player
        self.video_player.setVideoOutput(self.video_widget)
        # GeckonSola DebugViewer Process
        self.debug_output = QTextBrowser()
        self.debug_output.setFixedSize(630, 360)
        self.debug_output.setFont(QFont("Consolas", 10))
        self.debug_output.setStyleSheet("background-color: black; color: #00FF00;")
        # GeckoScope tm
        self.gecko_scope = GeckoScope()

        # Apilar
        self.video_stack.addWidget(self.video_placeholder)  # index 0
        self.video_stack.addWidget(self.video_widget)       # index 1
        self.video_stack.addWidget(self.debug_output)       # index 2
        self.video_stack.addWidget(self.gecko_scope)         # index 3
        # Uso: self.video_stack.setCurrentIndex(X) # Vuelve a la pantalla 

        # Contenedor visual
        video_container = QWidget()
        video_container.setLayout(self.video_stack)
        
        # Video Player Controls
        self.btn_prev_video = QPushButton("⏮")
        self.btn_play_video = QPushButton("▶")
        self.btn_next_video = QPushButton("⏭")
        self.btn_pause_video = QPushButton("⏸")
        self.btn_stop_video = QPushButton("⏹")
        self.btn_eject_video = QPushButton("⏏")
        self.btn_debug = QPushButton("👁️")
        self.btn_debug.setToolTip("Ver la memoria del ultimo render (Modo Matrix).")
        self.btn_geckoscope = QPushButton("🦎📈")  # Activar GeckoScope (osciloscopio/espectro)

        for b in [self.btn_prev_video, self.btn_play_video, self.btn_next_video, self.btn_pause_video, self.btn_stop_video]:
            b.setEnabled(False)
            b.setFixedHeight(50)
        self.btn_eject_video.setFixedHeight(50)
        self.btn_debug.setFixedHeight(50)
        self.btn_geckoscope.setFixedHeight(50)

        self.btn_prev_video.clicked.connect(self.prev_video)
        self.btn_play_video.clicked.connect(lambda: [self.video_stack.setCurrentIndex(1), self.video_player.play()])
        self.btn_next_video.clicked.connect(self.next_video)
        self.btn_pause_video.clicked.connect(self.video_player.pause)
        self.btn_stop_video.clicked.connect(self.video_player.stop)
        self.btn_eject_video.clicked.connect(self.eject_video)
        self.btn_debug.clicked.connect(lambda: self.video_stack.setCurrentIndex(2))
        self.btn_geckoscope.clicked.connect(lambda: self.video_stack.setCurrentIndex(3))

        video_controls = QHBoxLayout()
        video_controls.addWidget(self.btn_prev_video)
        video_controls.addWidget(self.btn_play_video)
        video_controls.addWidget(self.btn_next_video)
        video_controls.addWidget(self.btn_pause_video)
        video_controls.addWidget(self.btn_stop_video)
        video_controls.addWidget(self.btn_eject_video)
        video_controls.addWidget(self.btn_debug)
        video_controls.addWidget(self.btn_geckoscope)

        # 🦎🎛️ Playlist Geckoneana
        self.playlist = QListWidget()
        self.playlist.setFixedWidth(388)
        self.playlist.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.playlist.itemClicked.connect(self.cargar_video_desde_lista)
        self.playlist.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlist.customContextMenuRequested.connect(self.mostrar_context_menu_playlist)
        self.playlist.setDragDropMode(QAbstractItemView.InternalMove)
        self.playlist.setAcceptDrops(True)
        self.playlist.setDragDropMode(QAbstractItemView.InternalMove)
        self.playlist.setDefaultDropAction(Qt.CopyAction)

        #-------------------------PANEL DE EFECTOS GECKONEANOS GeckoFects ------------------------------
        # 📦 Panel de efectos geckonianos
        self.efectos_box = QGroupBox("🎛️ GeckoFects")
        efectos_layout = QVBoxLayout()

        self.chk_zoom = QCheckBox("Activar Zoom")
        self.chk_pan = QCheckBox("Activar Paneo")
        self.chk_slide = QCheckBox("M-Slide Show")  # aún sin implementar

        self.combo_eje = QComboBox()
        self.combo_eje.addItems(["x", "y", "diagonal"])
        self.combo_eje.setCurrentIndex(0)
        self.combo_eje.setEnabled(False)  # solo se activa si chk_pan está activo

        # 🔄 Conectar activación
        self.chk_pan.toggled.connect(lambda checked: self.combo_eje.setEnabled(checked))

        self.chk_loop_video = QCheckBox("Activar GeckoLoop")
        self.chk_loop_video.toggled.connect(self.toggle_loop_video)
        
        self.btn_geckealo = QPushButton("Geckealo")
        self.btn_geckealo.setFixedHeight(50)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.btn_geckealo.setFont(font)
        self.btn_geckealo.setEnabled(False)
        self.btn_geckealo.clicked.connect(self.create_loop_video)
        self.chk_loop_video.toggled.connect(lambda checked: self.btn_geckealo.setEnabled(checked and bool(self.video_path)))

        efectos_layout.addWidget(self.chk_zoom)
        efectos_layout.addWidget(self.chk_pan)
        efectos_layout.addWidget(self.combo_eje)
        efectos_layout.addWidget(self.chk_slide)
        efectos_layout.addWidget(self.chk_loop_video)
        efectos_layout.addWidget(self.btn_geckealo)

        self.efectos_box.setLayout(efectos_layout)

        #------------------------- Layouts de UI------------------------------
        # Layouts agrupados
        layout = QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1) # Sin márgenes sup/inf
        
        row1 = QVBoxLayout() #MP3
        row1.addWidget(self.label_mp3)
        row1.addWidget(btn_mp3)
        row1.addLayout(mp3_controls)
        row1.addWidget(self.playlistMP3)

        row2 = QVBoxLayout() # Cover
        row2.addWidget(self.label_cover)
        row2.addWidget(self.cover_preview)
        row2.addWidget(btn_cover)
        #row2.addStretch()

        row3 = QVBoxLayout() # Playlist Cover's
        row3.addWidget(self.playlistCover)

        mp3cover_layout = QHBoxLayout()
        mp3cover_layout.addLayout(row1)
        mp3cover_layout.addLayout(row2)
        mp3cover_layout.addLayout(row3)
        layout.addLayout(mp3cover_layout)
        
        btn_centrales = QHBoxLayout()
        btn_centrales.addWidget(btn_create)
        btn_centrales.addWidget(btn_exit)
        outlavel = QLabel("Nombre de salida:")        
        outlavel.setFixedHeight(20)
        layout.addWidget(outlavel)
        layout.addWidget(self.output_field)
        layout.addLayout(btn_centrales)
        layout.addWidget(self.status_label)
        
        # Layout interno del frame
        frame_layout = QHBoxLayout()
        video_left = QVBoxLayout()
        video_center = QVBoxLayout()
        video_right = QVBoxLayout()
        # Logo + Efectos
        video_left.addWidget(self.gecko_logo)
        video_left.addWidget(self.efectos_box)
        # Video y Controles
        video_center.addWidget(video_container)
        video_center.addLayout(video_controls)
        # PlayList MP4's y Boton Fusionador
        video_right.addWidget(self.playlist)
        video_right.addWidget(btn_gecko_fusion)
        # Llenar el Layout interno del frame
        frame_layout.addLayout(video_left)
        frame_layout.addLayout(video_center)
        frame_layout.addLayout(video_right)
        
        # Frame contenedor Gecko + Efectos + Video + Playlist
        video_frame = QFrame()
        video_frame.setObjectName("consolaGecko")
        video_frame.setLayout(frame_layout)
        
        layout.addWidget(video_frame)
        self.setLayout(layout)

        # Rutas
        self.mp3_path = ""
        self.cover_path = ""
        self.output_path = ""
        self.video_path = None  # Ruta del video MP4 mudo

    # ----------Util & facility ---------------
    def guardar_config(self):
        tema_actual = MainConMenu.tema_seleccionado

        #mp3_list = [self.playlistMP3.item(i).text() for i in range(self.playlistMP3.count())]
        #mp4_list = [self.playlist.item(i).text() for i in range(self.playlist.count())]
        # Para no perder referencia real al archivo , lo anterior guardaba solo el nombre.        
        mp3_list = [self.playlistMP3.item(i).data(Qt.UserRole) for i in range(self.playlistMP3.count())]
        mp4_list = [self.playlist.item(i).data(Qt.UserRole) for i in range(self.playlist.count())]
        cover_list = [self.playlistCover.item(i).data(Qt.UserRole) for i in range(self.playlistCover.count())]

        self.configurador.guardar_configuracion(
            tema=tema_actual,
            mp3_list=mp3_list,
            mp4_list=mp4_list,
            cover_list=cover_list
        )

    def aplicar_tema(self, nombre, bg_color, accent_color, text_color):
        # Definir estilos globales
        list_style = f"""
            background-color: {bg_color};
            color: {accent_color};
            border: 2px solid {accent_color};
            font-family: Consolas, monospace;
            font-size: 12pt;
            border-radius: 10px;
        """
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
            }}
            QPushButton {{
                background-color: {accent_color};
                color: {text_color};
                border-radius: 6px;
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {text_color};
                color: {accent_color};
            }}
            QListWidget {{
                {list_style}
            }}
            QListWidget::item:selected {{
                background-color: {accent_color};
                color: {bg_color};
            }}
        """)
        # Restablecer estilos de las playlists para evitar conflictos
        for list_widget in [self.playlist, self.playlistMP3, self.playlistCover]:
            list_widget.setStyleSheet(list_style)
        # Aplicar estilo a GeckoFects
        self.efectos_box.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {accent_color};
                border-radius: 8px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }}
        """)
        # Aplicar estilo al bloque video visual de la consola
        frame = self.findChild(QFrame, "consolaGecko")
        if frame:
            frame.setStyleSheet(f"""
                QFrame#consolaGecko {{
                    border: 3px solid {accent_color};
                    background-color: {bg_color};
                    border-radius: 10px;
                    padding: 5px;
                }}
            """)
        frame2 = self.findChild(QFrame, "geckoCreator")
        if frame2:
            frame2.setStyleSheet(f"""
                QFrame#geckoCreator {{
                    border: 2px solid {accent_color};
                    background-color: {bg_color};
                    border-radius: 7px;
                    padding: 5px;
                }}
            """)
        # Estilos normal y active (on drag & drop)
        self.list_style_normal = f"""
            {list_style}
        """
        self.list_style_active = f"""
            background-color: {bg_color};
            color: {accent_color};
            border: 3px solid #00ff00;  /* Verde brillante para drag & drop */
            font-family: Consolas, monospace;
            font-size: 12pt;
            border-radius: 10px;
        """
        self.status_label.setText(f"🎨 Tema activado: {nombre}")
        MainConMenu.tema_seleccionado = (nombre, bg_color, accent_color, text_color)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            # --- Definimos las extensiones válidas (by Ei2)---
            VIDEO_EXT = (".mp4",)
            AUDIO_EXT = (".mp3", ".m4a", ".aac", ".wav")  # <--- AÑADIDOS
            IMAGE_EXT = (".jpg", ".jpeg", ".png")
            # ---
            # Verificar si algún archivo tiene una extensión válida
            for url in event.mimeData().urls():
                path = url.toLocalFile().strip()
                ext = path.lower()
                # 🎬 Archivos de video
                if ext.endswith(VIDEO_EXT):
                    self.playlist.setStyleSheet(self.list_style_active)
                    event.acceptProposedAction()
                    return  # Aceptamos en cuanto encontramos UN archivo válido
                # 🎵 Archivos de audio
                elif ext.endswith(AUDIO_EXT):  # <--- CAMBIO AQUÍ
                    self.playlistMP3.setStyleSheet(self.list_style_active)
                    event.acceptProposedAction()
                    return  # Aceptamos en cuanto encontramos UN archivo válido
                # 🖼️ Archivos de imagen
                elif ext.endswith(IMAGE_EXT):
                    self.playlistCover.setStyleSheet(self.list_style_active)
                    event.acceptProposedAction()
                    return  # Aceptamos en cuanto encontramos UN archivo válido
                '''
                if ext.endswith((".mp4", ".mp3", ".jpg", ".jpeg", ".png")):
                    # Aplicar estilo activo a la lista correspondiente
                    if ext.endswith(".mp4"):
                        self.playlist.setStyleSheet(self.list_style_active)
                    elif ext.endswith(".mp3"):
                        self.playlistMP3.setStyleSheet(self.list_style_active)
                    elif ext.endswith((".jpg", ".jpeg", ".png")):
                        self.playlistCover.setStyleSheet(self.list_style_active)
                    event.acceptProposedAction()
                    return
                '''
        super().dragEnterEvent(event)
        
    def dragLeaveEvent(self, event):
        # Restablecer estilo si el usuario sale sin soltar
        self.playlist.setStyleSheet(self.list_style_normal)
        self.playlistMP3.setStyleSheet(self.list_style_normal)
        self.playlistCover.setStyleSheet(self.list_style_normal)
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            # --- Definimos las extensiones válidas (para consistencia) by Ei2---
            VIDEO_EXT = (".mp4",)
            AUDIO_EXT = (".mp3", ".m4a", ".aac", ".wav")  # <--- AÑADIDOS
            IMAGE_EXT = (".jpg", ".jpeg", ".png")
            # ---
            for url in event.mimeData().urls():
                path = url.toLocalFile().strip()
                if not os.path.exists(path):
                    continue
                ext = path.lower()
                # 🎬 Archivos de video
                if ext.endswith(VIDEO_EXT):
                    item = QListWidgetItem(os.path.basename(path))
                    item.setData(Qt.UserRole, path)
                    self.playlist.addItem(item)
                    self.status_label.setText(f"✅ Añadido: {os.path.basename(path)}")
                    QTimer.singleShot(1000, lambda: self.reset_list_style(self.playlist)) # Restablecer estilo después de 2 segundos
                # 🎵 Archivos de audio
                elif ext.endswith(AUDIO_EXT):
                    item = QListWidgetItem(os.path.basename(path))
                    item.setData(Qt.UserRole, path)
                    self.playlistMP3.addItem(item)
                    self.status_label.setText(f"✅ Añadido: {os.path.basename(path)}")
                    QTimer.singleShot(1000, lambda: self.reset_list_style(self.playlistMP3))
                # 🖼️ Archivos de imagen
                elif ext.endswith(IMAGE_EXT):
                    item = QListWidgetItem(os.path.basename(path))
                    item.setData(Qt.UserRole, path)
                    self.playlistCover.addItem(item)
                    self.status_label.setText(f"✅ Añadido: {os.path.basename(path)}")
                    QTimer.singleShot(1000, lambda: self.reset_list_style(self.playlistCover))

            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def reset_list_style(self, list_widget):
        list_widget.setStyleSheet(self.list_style_normal)
        self.status_label.setText("")  # Limpiar status_label

    # Nuevos métodos en tu clase GeckoMP4Creator Utils (by Ei2 & NOva DulceKali NOvaPythoniza & Aetheris for GeckoCreator DebugViewer Process Eco)
    def check_process_finished(self):
        """ Check Procces by Aetheris
        """
        if self.process.poll() is not None:
            self.timer.stop()
            self.check_timer.stop()
            return_code = self.process.returncode
            if return_code == 0 and os.path.exists(self.output_path) and os.path.getsize(self.output_path) > 0:
                self.status_label.setText("🦎 GeckoForjado con Velocidad y Amor! Multiverso Conquistado!")
                item = QListWidgetItem(os.path.basename(self.output_path))
                item.setData(Qt.UserRole, self.output_path)
                self.playlist.addItem(item)
            else:
                self.status_label.setText("⚠️ Error al forjar el Ciclo GeckoLoop.")
                print(f"❌ FFmpeg terminó con error (returncode: {return_code})")
                output, _ = self.process.communicate()
                if output:
                    print("──── FFmpeg Output ────")
                    print(output)

    def update_output(self):
        if self.process.stdout and self.process.poll() is None:
            # Lee una línea del proceso
            line = self.process.stdout.readline().strip()
            if line:
                #print(f"FFmpeg: {line}") # eco en terminal for debuging en yoging de yoga
                self.debug_output.append(line) # eco en tu QTextEdit/console
                QApplication.processEvents()  # Forza actualización de la UI
        
        # Si el proceso terminó
        if self.process.poll() is not None:
            self.timer.stop()
            self.status_label.setText("✅ ¡MP4 creado con éxito!")
            if self.process.returncode != 0:
                self.status_label.setText(f"❌ Error en el render. Código: {self.process.returncode}")
    
    # -------------MP3 management---------------
    def select_mp3(self):
        # 1. MEJORA Ei2: Un filtro de archivos más profesional y descriptivo
        filter_string = (
            "Archivos de Audio (*.m4a *.mp3 *.wav);;"
            "Audio AAC (*.m4a);;"
            "Audio MP3 (*.mp3);;"
            "Audio WAV (*.wav);;"
            "Todos los archivos (*.*)"
        )
        #path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de Audio", "", "Archivos MP3 (*.mp3 *.wav *.m4a)")
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de Audio", "", filter_string)
        if path:
            self.mp3_path = path
            self.label_mp3.setText(f"Audio: {os.path.basename(path)}")
            self.player_mp3.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            for b in [self.btn_prev_mp3, self.btn_play_mp3, self.btn_next_mp3, self.btn_pause_mp3, self.btn_stop_mp3]:
                b.setEnabled(True)
            self.btn_prev_mp3.setEnabled(self.playlistMP3.currentRow() > 0)
            self.btn_next_mp3.setEnabled(self.playlistMP3.currentRow() < self.playlistMP3.count() - 1)
            # 🪄 Autocompletar el nombre del archivo de salida
            base_name = os.path.splitext(os.path.basename(path))[0]
            self.output_field.setText(base_name + ".mp4")
            # Agregar al playlist de audios MP3
            if path.lower().endswith(".mp3") or path.lower().endswith(".wav") or path.lower().endswith(".m4a"):
                item = QListWidgetItem(os.path.basename(path))
                item.setData(Qt.UserRole, path)
                self.playlistMP3.addItem(item)

    def prev_mp3(self):
        current_row = self.playlistMP3.currentRow()
        if current_row > 0:
            self.playlistMP3.setCurrentRow(current_row - 1)
            item = self.playlistMP3.currentItem()
            if item:
                self.cargar_audio_desde_lista(item)
                self.btn_next_mp3.setEnabled(True)
        if current_row <= 1:
            self.btn_prev_mp3.setEnabled(False)

    def next_mp3(self):
        current_row = self.playlistMP3.currentRow()
        if current_row < self.playlistMP3.count() - 1:
            self.playlistMP3.setCurrentRow(current_row + 1)
            item = self.playlistMP3.currentItem()
            if item:
                self.cargar_audio_desde_lista(item)
                self.btn_prev_mp3.setEnabled(True)
        if current_row >= self.playlistMP3.count() - 2:
            self.btn_next_mp3.setEnabled(False)

    def handle_mp3_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.playlistMP3.currentRow() < self.playlistMP3.count() - 1:
            self.next_mp3()
        elif status == QMediaPlayer.EndOfMedia:
            self.btn_next_mp3.setEnabled(False)
            self.video_stack.setCurrentIndex(0)
            self.status_label.setText("🎵 Fin de la playlist MP3.")

    def play_mp3(self):
        self.player_mp3.play()
        self.video_stack.setCurrentIndex(3)  # Mostrar GeckoScope

    def pause_mp3(self):
        self.player_mp3.pause()

    def stop_mp3(self):
        self.player_mp3.stop()
        #self.gecko_scope.close()
        self.video_stack.setCurrentIndex(0)  # Muestra el placeholder

    def mostrar_context_menu_playlistMP3(self, position):
        menu = QMenu()
        accion_agregar = menu.addAction("➕ Agregar Audio a la Playlist")
        accion_abrir_audacity = menu.addAction("🎙️ Abrir en Audacity")
        accion_eliminar = menu.addAction("🗑️ Eliminar Audio de la lista")
        accion_eliminar_todos = menu.addAction("🗑️ Eliminar todos los audios")  # Nueva acción
        action = menu.exec_(self.playlistMP3.viewport().mapToGlobal(position))
        if action == accion_agregar:
            # 1. MEJORA Ei2: Un filtro de archivos más profesional y descriptivo
            filter_string = (
                "Archivos de Audio (*.m4a *.mp3 *.wav);;"
                "Audio AAC (*.m4a);;"
                "Audio MP3 (*.mp3);;"
                "Audio WAV (*.wav);;"
                "Todos los archivos (*.*)"
            )
            #path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Audio", "", "Audios (*.mp3 *.wav *.m4a)")
            path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Audio", "", filter_string)
            if path.lower().endswith(".mp3") or path.lower().endswith(".wav") or path.lower().endswith(".m4a"):
                item = QListWidgetItem(os.path.basename(path))
                item.setData(Qt.UserRole, path)
                self.playlistMP3.addItem(item)
        elif action == accion_abrir_audacity:
            item = self.playlistMP3.currentItem()
            if item:
                path = item.data(Qt.UserRole)
                if path:
                    # Lanzar Audacity con el archivo
                    subprocess.Popen(["audacity", path])
        elif action == accion_eliminar:
            item = self.playlistMP3.currentItem()
            if item:
                self.playlistMP3.takeItem(self.playlistMP3.row(item))
        elif action == accion_eliminar_todos:
            self.eliminar_todos_playlistMP3()  # Llamar al nuevo método

    def cargar_audio_desde_lista(self, item):
        path = item.data(Qt.UserRole)
        if path and os.path.exists(path):
            self.player_mp3.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.player_mp3.play()
            self.video_stack.setCurrentIndex(3)  # Mostrar GeckoScope
            self.status_label.setText(f"🎞️ Reproduciendo: {os.path.basename(path)}")
            for b in [self.btn_prev_mp3, self.btn_play_mp3, self.btn_next_mp3, self.btn_pause_mp3, self.btn_stop_mp3]:
                b.setEnabled(True)
            current_row = self.playlistMP3.currentRow()
            self.btn_prev_mp3.setEnabled(current_row > 0)
            self.btn_next_mp3.setEnabled(current_row < self.playlistMP3.count() - 1)
            # 🪄 Autocompletar el nombre del archivo de entrada/salida // Evaluar Usabilidad
            self.label_mp3.setText(f"Audio: {os.path.basename(path)}")
            base_name = os.path.splitext(os.path.basename(path))[0]
            self.output_field.setText(base_name + ".mp4")
            # completar path para crear MP4
            self.mp3_path = path

    def eliminar_todos_playlistMP3(self):
        """Elimina todos los elementos de la playlist de audios con confirmación."""
        reply = QMessageBox.question(self, "Confirmar", 
                                    "¿Seguro que querés vaciar la playlist de audios?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.playlistMP3.clear()
            self.status_label.setText("🗑️ Playlist de audios vaciada.")

    # ------------COVER managament--------------
    def select_cover(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen JPG", "", "Imágenes JPG (*.jpg *.jpeg *.png)")
        if path:
            self.cover_path = path
            self.label_cover.setText(f"Imagen: {os.path.basename(path)}")
            #pixmap = QPixmap(path)
            #self.cover_preview.setPixmap(pixmap)
            pixmap = QPixmap(path)
            scaled = pixmap.scaled(self.cover_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.cover_preview.setPixmap(scaled)
            # Agregar a la lista
            item = QListWidgetItem(os.path.basename(path))
            item.setData(Qt.UserRole, path)
            self.playlistCover.addItem(item)

    def cargar_imagen_desde_lista(self, item):
        path = item.data(Qt.UserRole)
        if path and os.path.exists(path):
            self.cover_path = path
            self.label_cover.setText(f"Imagen: {os.path.basename(path)}")
            pixmap = QPixmap(path)
            scaled = pixmap.scaled(self.cover_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.cover_preview.setPixmap(scaled)
            self.status_label.setText(f"🖼️ Imagen cargada: {os.path.basename(path)}")

    def mostrar_context_menu_playlistCover(self, position):
        menu = QMenu()
        accion_agregar = menu.addAction("➕ Agregar imagen a la lista")
        accion_eliminar = menu.addAction("🗑️ Eliminar imagen de la lista")
        accion_eliminar_todos = menu.addAction("🗑️ Eliminar todas las imágenes")
        action = menu.exec_(self.playlistCover.viewport().mapToGlobal(position))
        if action == accion_agregar:
            path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.jpg *.jpeg *.png)")
            if path.lower().endswith((".jpg", ".jpeg", ".png")):
                item = QListWidgetItem(os.path.basename(path))
                item.setData(Qt.UserRole, path)
                self.playlistCover.addItem(item)
        elif action == accion_eliminar:
            item = self.playlistCover.currentItem()
            if item:
                self.playlistCover.takeItem(self.playlistCover.row(item))
        elif action == accion_eliminar_todos:
            reply = QMessageBox.question(self, "Confirmar", 
                                        "¿Seguro que querés vaciar la lista de imágenes?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.playlistCover.clear()
                self.status_label.setText("🗑️ Lista de imágenes vaciada.")

    # -------------MP4 Create & management---------------
    def create_mp4(self):
        if not all([self.mp3_path, self.cover_path]):
            self.status_label.setText("⚠️ Faltan archivos.")
            return
        self.status_label.setText("Creando Video Multiversal desde GeckoPS...")

        time.sleep(0.137)  # 137 ms
        output_name = self.output_field.text().strip()
        if not output_name.lower().endswith(".mp4"):
            output_name += ".mp4"

        output_dir = os.path.dirname(self.mp3_path)
        self.output_path = os.path.join(output_dir, output_name)
        '''
        cmd = [
            "ffmpeg", "-hide_banner",           # evita que aparezca toda la información de codecs del sistema.
            "-y",                               # -y: sobrescribe el archivo de salida si ya existe
            "-loop", "1",                       # loopea la imagen (para que dure lo mismo que el audio)
            "-framerate", "2",                  # asegura que el contenedor tenga fps válido y bajo
            "-i", self.cover_path,              # input imagen (portada del video)
            "-i", self.mp3_path,                # input audio (mp3 o wav recomendado)

            # VIDEO ENCODING
            "-c:v", "libx264",                  # códec de video H.264
            "-preset", "slow",                  # optimiza compresión y calidad (más lento = mejor calidad)
            "-crf", "18",                       # calidad constante (menos = mejor calidad visual)
            "-tune", "stillimage",              # ajusta parámetros al tener imagen estática (funciona para libx264 no para h264_nvenc)
            "-pix_fmt", "yuv420p",              # formato de pixeles compatible con YouTube

            # AUDIO ENCODING
            "-c:a", "copy",                     # no comprime el audio (solo MP3) hiper veloz, mejor calidad!!!
            #"-c:a", "aac",                     # códec de audio AAC (recomendado por YouTube)
            #"-b:a", "192k",                    # 128k, 192k (for Trap!), 320k bitrate de audio elevado para conservar calidad
            #"-ar", "48000",                    # frecuencia de muestreo ideal para YouTube

            # OUTPUT BEHAVIOR
            "-movflags", "+faststart",          # mejora el streaming progresivo (YouTube lo prefiere)
            "-shortest",                        # corta el video al final del audio

            self.output_path                    # ruta de salida del archivo .mp4
        ]
        '''
        # Video de imagen estática con audio (GPU NVENC) by NOva DulceKali
        cmd = [
            "ffmpeg", "-hide_banner", "-y",
            "-loop", "1",
            "-framerate", "2",           # suficiente para still image
            "-i", self.cover_path,
            "-i", self.mp3_path,
            "-c:v", "h264_nvenc",
            "-preset", "fast",
            "-rc", "vbr",
            "-cq", "23",
            "-tune", "hq",       # optimiza para imagen estática (reemplazamos el "stillimage" que crashea)
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",              # audio sin recodificar
            "-movflags", "+faststart",
            "-shortest",
            self.output_path
        ]

        #self.status_label.setText("Creando Video Multiversal desde GeckoPS...")
        ''' for Viewer
        result = subprocess.run(cmd)
        if result.returncode == 0:
            self.status_label.setText("✅ ¡MP4 creado con éxito!")
        else:
            self.status_label.setText("❌ Error al crear el video. Código:", result.returncode)
        '''
        
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True, #Ei2
            bufsize=1
        )

        # Crea un temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_output)
        self.timer.start(100) # Revisa la salida cada 100 ms

        # Cambia la vista a la pantalla de debug
        self.video_stack.setCurrentIndex(2)
        
        #self.load_video() #Comentado para GeckonSola DebugViewer Process
        
        item = QListWidgetItem(os.path.basename(self.output_path))
        item.setData(Qt.UserRole, self.output_path)
        self.playlist.addItem(item)

    def mostrar_context_menu_playlist(self, position):
        menu = QMenu()
        accion_agregar = menu.addAction("➕ Agregar video a la Playlist")
        accion_eliminar = menu.addAction("🗑️ Eliminar de la lista")
        accion_eliminar_todos = menu.addAction("🗑️ Eliminar todos los videos")  # Nueva acción
        action = menu.exec_(self.playlist.viewport().mapToGlobal(position))
        if action == accion_agregar:
            path, _ = QFileDialog.getOpenFileName(self, "Seleccionar video MP4", "", "Videos (*.mp4)")
            if path.lower().endswith(".mp4"):
                item = QListWidgetItem(os.path.basename(path))
                item.setData(Qt.UserRole, path)
                self.playlist.addItem(item)
        elif action == accion_eliminar:
            item = self.playlist.currentItem()
            if item:
                self.playlist.takeItem(self.playlist.row(item))
        elif action == accion_eliminar_todos:
            self.eliminar_todos_playlist()  # Llamar al nuevo método

    def cargar_video_desde_lista(self, item):
        path = item.data(Qt.UserRole)
        if path and os.path.exists(path):
            self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            # cambiar a vista reproductor
            self.video_player.setVideoOutput(self.video_widget)
            self.video_stack.setCurrentIndex(1)
            self.video_player.play()
            self.status_label.setText(f"🎞️ Reproduciendo: {os.path.basename(path)}")
            for b in [self.btn_prev_video, self.btn_play_video, self.btn_next_video, self.btn_pause_video, self.btn_stop_video, self.btn_eject_video]:
                b.setEnabled(True)
            current_row = self.playlist.currentRow()
            self.btn_prev_video.setEnabled(current_row > 0)
            self.btn_next_video.setEnabled(current_row < self.playlist.count() - 1)
            
    def load_video(self):
        if os.path.exists(self.output_path):
            self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.output_path)))
            for b in [self.btn_play_video, self.btn_pause_video, self.btn_stop_video, self.btn_eject_video]:
                b.setEnabled(True)
            # cambiar a vista reproductor
            self.video_player.setVideoOutput(self.video_widget)
            self.video_stack.setCurrentIndex(1)

    def prev_video(self):
        current_row = self.playlist.currentRow()
        if current_row > 0:
            self.playlist.setCurrentRow(current_row - 1)
            item = self.playlist.currentItem()
            if item:
                self.cargar_video_desde_lista(item)
                self.btn_next_video.setEnabled(True)
        if current_row <= 1:
            self.btn_prev_video.setEnabled(False)

    def next_video(self):
        current_row = self.playlist.currentRow()
        if current_row < self.playlist.count() - 1:
            self.playlist.setCurrentRow(current_row + 1)
            item = self.playlist.currentItem()
            if item:
                self.cargar_video_desde_lista(item)
                self.btn_prev_video.setEnabled(True)
        if current_row >= self.playlist.count() - 2:
            self.btn_next_video.setEnabled(False)

    def handle_video_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.playlist.currentRow() < self.playlist.count() - 1:
            self.next_video()
        elif status == QMediaPlayer.EndOfMedia:
            self.btn_next_video.setEnabled(False)
            self.video_stack.setCurrentIndex(0)
            self.status_label.setText("🎞️ Fin de la playlist MP4.")

    def eject_video(self):
        self.video_player.stop()  # Detiene la reproducción
        self.video_player.setMedia(QMediaContent())  # Libera el medio
        self.video_stack.setCurrentIndex(0)  # Muestra el placeholder
        self.status_label.setText("📼 Video expulsado de la GeckonSola")
        for b in [self.btn_play_video, self.btn_pause_video, self.btn_stop_video]: #self.btn_eject_video
            b.setEnabled(False)

    def eliminar_todos_playlist(self):
        """Elimina todos los elementos de la playlist de videos con confirmación."""
        reply = QMessageBox.question(self, "Confirmar", 
                                    "¿Seguro que querés vaciar la playlist de videos?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.playlist.clear()
            self.status_label.setText("🗑️ Playlist de videos vaciada.")

    def toggle_loop_video (self, checked):
        """ Aetheris Function
        """
        if checked:
            path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Video MP4 Mudo", "", "Videos (*.mp4)")
            if path and path.lower().endswith(".mp4") and os.path.exists(path):
                self.video_path = path
                self.status_label.setText(f"🎥 Video loop {os.path.basename(path)} seleccionado")
                item = QListWidgetItem(os.path.basename(path))
                item.setData(Qt.UserRole, path)
                self.playlist.addItem(item)
            else:
                self.chk_loop_video.setChecked(False)
                self.status_label.setText("⚠️ No se seleccionó un video MP4 válido")
        else:
            self.video_path = None
            self.status_label.setText("🦎 GeckoLoop desactivado")
            self.btn_geckealo.setEnabled(False)

    def create_loop_video(self):
        """ by Aetheris & NOva DulceKAli NOvaPythoniza
        """
        if not all([self.mp3_path, self.video_path]):
            self.status_label.setText("⚠️ Faltan archivos (audio o video mudo).")
            return

        self.status_label.setText("🦎 Forjando Ciclo GeckoLoop con Audio...")
        
        # Cambia la vista a la pantalla de debug antes de bloquear
        self.video_stack.setCurrentIndex(2)
        
        # pequeño retardo para que no bloquee consola
        #time.sleep(0.137)  # 137 ms
        
        output_name = self.output_field.text().strip()
        #import re
        #output_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', self.output_field.text().strip())
        if not output_name.lower().endswith(".mp4"):
            output_name += ".mp4"
        output_dir = os.path.dirname(self.mp3_path)
        self.output_path = os.path.join(output_dir, output_name)

        cmd = generar_comando_gecko(
            mode="loop_video",
            mp3_path=self.mp3_path,
            video_path=self.video_path,
            output_path=self.output_path
        )

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.
                PIPE,stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Crea un temporizador
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_output)
            self.timer.start(100)

            self.check_timer = QTimer(self)
            self.check_timer.timeout.connect(self.check_process_finished)
            self.check_timer.start(500)

            ''' # Old NOva
            return_code = self.process.wait()
            if return_code == 0 and os.path.exists(self.output_path) and os.path.getsize(self.output_path) > 0:
                self.status_label.setText("🦎 GeckoForjado con Velocidad y Amor! Multiverso Conquistado!")
                item = QListWidgetItem(os.path.basename(self.output_path))
                item.setData(Qt.UserRole, self.output_path)
                self.playlist.addItem(item)
            else:
                self.status_label.setText("⚠️ Error al forjar el Ciclo GeckoLoop.")
                print("❌ FFmpeg terminó con error (returncode:", return_code, ")")
                # 🔎 Mostramos salida completa
                output, _ = self.process.communicate()
                print("──── FFmpeg Output ────")
                print(output)
            
            '''

            ''' # Old Aetheris
            if self.process.wait() == 0 and os.path.exists(self.output_path) and os.path.getsize(self.output_path) > 0:
                self.status_label.setText("🦎 GeckoForjado con Velocidad y Amor! Multiverso Conquistado!")
                item = QListWidgetItem(os.path.basename(self.output_path))
                item.setData(Qt.UserRole, self.output_path)
                self.playlist.addItem(item)
            else:
                self.status_label.setText("⚠️ Error al forjar el Ciclo GeckoLoop.")
            '''
        
        except Exception as e:
            print("❌ Error inesperado en FFmpeg:")
            print("Comando ejecutado:", ' '.join(cmd))
            print("Detalle:", str(e))
            self.status_label.setText("⚠️ Error inesperado en Ciclo GeckoLoop.")

    # --------MP4 GeckoFusion Épica by Aetheris----------
    def create_gecko_fusion(self):
        if self.playlist.count() < 2:
            self.status_label.setText("⚠️ ¡Necesitás al menos 2 videos para la GeckoFusion Épica!")
            return

        # Advertencia geckoniana con QMessageBox
        reply = QMessageBox.question(
            self, "Confirmar Fusión Geckoniana",
            "🦎 ¡Solo acepta videos forjados\n"
            "  en el corazón de la GeckonSola!,\n"
            "  Ser de Carbono Hijo del Viento,\n"
            "   ¿Lanzás la Fusión Épica?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.No:
            self.status_label.setText("🚀 Revisá la Nave y volvé cuando estés listo.")
            return
        
        # Elegir el nombre de la fusión
        output_name, ok = QInputDialog.getText(self, "Nombre de la Fusión Épica",
                                            "Ingresa el nombre del archivo (sin .mp4):",
                                            text="GeckoFusion_Epica")
        if not ok:
            self.status_label.setText("🚀 Fusión cancelada. Revisá la Nave.")
            return

        # Validacion de Formato Simple
        output_name = "".join(c for c in output_name.strip() if c.isalnum() or c in " _-")
        if not output_name:
            output_name = "GeckoFusion_Epica"
        output_name += ".mp4"

        # Obtener rutas de los MP4s
        mp4_list = [self.playlist.item(i).data(Qt.UserRole) for i in range(self.playlist.count())]
        if not all(os.path.exists(path) and path.lower().endswith(".mp4") for path in mp4_list):
            self.status_label.setText("❌ ¡Error! Algunos archivos no son videos válidos.")
            return

        # Crear archivo de lista temporal para FFmpeg
        output_dir = os.path.dirname(mp4_list[0]) if mp4_list else os.getcwd()
        output_path = os.path.join(output_dir, output_name)

        # Verificar si el archivo ya existe
        if os.path.exists(output_path):
            reply = QMessageBox.question(
                self, "Archivo Existente",
                f"🦎 ¡El archivo {output_name} ya existe!\n¿Querés sobrescribirlo?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.No:
                self.status_label.setText("🚀 Fusión cancelada. Elegí otro nombre.")
                return

        list_file = os.path.join(self.scriptDir, "temp_gecko_fusion.txt")

        self.status_label.setText("🦎 Creando la GeckoFusion Épica...")

        # Cambia la vista a la pantalla de debug antes de bloquear
        self.video_stack.setCurrentIndex(2)
        
        # pequeño retardo para que no bloquee consola
        time.sleep(0.137)  # 137 ms

        try:
            with open(list_file, "w", encoding="utf-8") as f:
                for path in mp4_list:
                    f.write(f"file '{path}'\n")

            # Comando FFmpeg para concatenar
            cmd = [
                "ffmpeg", "-hide_banner", "-y",
                "-f", "concat", "-safe", "0",
                "-i", list_file,
                "-c:v", "copy", "-c:a", "copy",
                "-movflags", "+faststart",
                output_path
            ]

            result = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True, #Ei2
                bufsize=1
            )

            # Crea un temporizador
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_output)
            self.timer.start(100) # Revisa la salida cada 100 ms

            #result = subprocess.run(cmd, capture_output=True, text=True)
            #result = subprocess.run(cmd) #original funcionando lo anterior es para tener algun eco en consola
            if result.returncode == 0:
                self.status_label.setText(f"✅ ¡GeckoFusion Épica creada: {output_name}!")
                # Añadir a la playlist
                item = QListWidgetItem(output_name)
                item.setData(Qt.UserRole, output_path)
                self.playlist.addItem(item)
                self.load_video()  # Cargar el video resultante
            else:
                self.status_label.setText(f"❌ Error en la GeckoFusion: {result.stderr}")

        finally:
            # Limpiar archivo temporal
            if os.path.exists(list_file):
                os.remove(list_file)
    
    # ------- GeckonSola GeckoCreator Exit Process ------
    def salir_con_gloria_divina(self):
        QMessageBox.information(self, "Gecko te despide", 
            "🦎 Que tu salida sea gloriosa, divina y renderizada.\n"
            "¡Hasta el próximo render!")
        QApplication.quit()  # Cierra toda la aplicación

    def closeEvent(self, event):
        self.gecko_scope.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
    ventana = MainConMenu()
    ventana.show()
    sys.exit(app.exec_())
