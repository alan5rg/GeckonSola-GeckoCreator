# ╭──────────────────────────────────────────────────────────────╮
# │ 🧠 classaveconf.py - Módulo de Configuración Persistente    │
# │                                                              │
# │ Guarda y carga preferencias de usuario en GeckoMP4Creator   │
# │ con estructura dict + serialización pickle.                  │
# │                                                              │
# │ Porque Gecko también recuerda lo que amás.                   │
# ╰──────────────────────────────────────────────────────────────╯
'''
MODO DE USO:
# Importar
from classaveconf import ConfiguradorGecko

# Instanciar
self.configurador = ConfiguradorGecko()
config = self.configurador.cargar_configuracion()

# Aplicás el tema cargado
self.aplicar_tema(*config["tema"])

# Cargás listas si querés...
# self.playlist_mp3.addItems(config["playlistMP3"])  ← si ya los tenés en widgets

'''
import os
import pickle

class ConfiguradorGecko:
    def __init__(self, parent, archivo_config="geckonfigv2.pkl"):
        self.parent = parent
        self.archivo = archivo_config
        self.config = {
            "tema": ("Azul Servidor Cuántico", "#001122", "#0084ff", "#ffffff"),
            "playlistMP3": [],
            "playlistMP4": [],
            "playlistCover": []  # 🦎 Lista para imágenes cargadas
        }

    def guardar_configuracion(self, tema=None, mp3_list=None, mp4_list=None, cover_list=None):
        """
        Guarda los datos actuales (tema, listas de reproducción) en disco.
        🦎 Incluye playlistCover para persistencia geckoniana.
        """
        if tema:
            self.config["tema"] = tema
        if mp3_list is not None:
            self.config["playlistMP3"] = mp3_list
        if mp4_list is not None:
            self.config["playlistMP4"] = mp4_list
        if cover_list is not None:
            self.config["playlistCover"] = cover_list

        try:
            with open(self.archivo, "wb") as f:
                pickle.dump(self.config, f)
            #print("💾 Configuración guardada con éxito.")
            self.parent.status_label.setText("💾 Configuración guardada con éxito.")
        except Exception as e:
            #print(f"⚠️ Error al guardar configuración: {e}")
            self.parent.status_label.setText(f"⚠️ Error al guardar configuración: {e}")

    def cargar_configuracion(self):
        """
        Carga la configuración desde disco. Si no existe, devuelve los valores por defecto.
        """
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "rb") as f:
                    self.config = pickle.load(f)
                print("📦 Configuración cargada correctamente.")
                #self.parent.status_label.setText("📦 Configuración cargada correctamente.")
            except Exception as e:
                print(f"⚠️ Error al cargar configuración: {e}")
                #self.parent.status_label.setText(f"⚠️ Error al cargar configuración: {e}")
        else:
            print("📁 No se encontró configuración. Usando valores por defecto.")

        return self.config
