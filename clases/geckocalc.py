# geckocalc.py
# ╭──────────────────────────────────────────────────────────────╮
# │ 🦎 GeckoMP4Creator - Estudio Geckoniano Audiovisual Libre    │
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
# │ 🎛️ Libertad en cada click.                                    │
# ╰──────────────────────────────────────────────────────────────╯
'''
Somos Geckoístas Autónomos del Sur Digital.
Una mezcla de Perón, Foucault, Stallman y un mono en calzoncillos programando en el balcón de la Matrix.

EJEMPLO DE USO:
from geckocalc import calcular_parametros_animacion

duracion, zoom_speed, pan_speed = calcular_parametros_animacion(
    mp3_path,
    zoom_limit=1.15,
    pan_distancia=720
)
'''
import subprocess
import re

def obtener_duracion_mp3(path_mp3):
    """
    Devuelve la duración del archivo MP3 en segundos (float).
    """
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                path_mp3
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        duracion = float(result.stdout.strip())
        return duracion
    except Exception as e:
        print(f"[geckocalc] Error al obtener duración: {e}")
        return 0.0

def obtener_duracion_mp3ffmpeg(path_mp3):
    """
    Usa ffmpeg para analizar el archivo de audio completo y obtener una duración precisa.
    Devuelve la duración en segundos (float).
    """
    try:
        # Este comando lee todo el archivo sin escribir nada, forzando un análisis completo.
        result = subprocess.run(
            ["ffmpeg", "-i", path_mp3, "-f", "null", "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # La duración está en la salida de error (stderr)
        output = result.stderr
        # Usamos una expresión regular para encontrar la línea "Duration: HH:MM:SS.ss"
        match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})", output)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            milliseconds = int(match.group(4))
            
            total_seconds = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 100.0)
            return total_seconds
        else:
            print(f"[geckocalc] No se pudo encontrar la duración en la salida de ffmpeg.")
            return 0.0
    except Exception as e:
        print(f"[geckocalc] Error al obtener duración confiable: {e}")
        return 0.0

def obtener_duracion_video(video_path):
    """
    Usa ffprobe para obtener la duración del video en segundos (float).
    """
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        duration = float(result.stdout.strip())
        return duration if duration > 0 else 0.0
    except Exception as e:
        print(f"[geckocalc] Error al obtener duración del video: {e}")
        return 0.0

def calcular_zoom_speed(duracion, zoom_limit=1.1):
    """
    Calcula la velocidad de zoom necesaria para alcanzar zoom_limit
    al final de la duración del audio.
    """
    if duracion <= 0:
        return 0.0
    incremento = zoom_limit - 1.0
    return round(incremento / duracion, 6)

def calcular_pan_speed(duracion, distancia_pixels=1280):
    """
    Calcula la velocidad de paneo (en píxeles por segundo) para
    recorrer distancia_pixels a lo largo de la duración.
    """
    if duracion <= 0:
        return 0.0
    return round(distancia_pixels / duracion, 4)

def calcular_parametros_animacion(path_mp3, zoom_limit=1.68, pan_distancia=1280):
    """
    Función unificadora. Devuelve duración, velocidad de zoom y paneo.
    """
    duracion = obtener_duracion_mp3(path_mp3)
    zoom_speed = calcular_zoom_speed(duracion, zoom_limit)
    pan_speed = calcular_pan_speed(duracion, pan_distancia)
    return duracion, zoom_speed, pan_speed