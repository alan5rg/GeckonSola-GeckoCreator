# geckofects.py
# 🦎 Módulo de filtros y efectos geckonianos para ffmpeg
'''
AJUSTAR A ESTE FORMATO
cmd = [
            "ffmpeg", "-hide_banner",           # evitar que nos aparezca información sobre el sistema y codecs
            "-y",                               # -y: sobrescribe el archivo de salida si ya existe
            "-loop", "1",                       # loopea la imagen (para que dure lo mismo que el audio)
            "-framerate", "2",                  # asegura que el contenedor tenga fps válido y bajo
            "-i", self.cover_path,              # input imagen (portada del video)
            "-i", self.mp3_path,                # input audio (mp3 o wav recomendado)

            # VIDEO ENCODING
            "-c:v", "libx264",                  # códec de video H.264
            "-preset", "slow",                  # optimiza compresión y calidad (más lento = mejor calidad)
            "-crf", "18",                       # calidad constante (menos = mejor calidad visual)
            "-tune", "stillimage",              # ajusta parámetros al tener imagen estática
            "-pix_fmt", "yuv420p",              # formato de pixeles compatible con YouTube

            # AUDIO ENCODING
            "-c:a", "copy",                     # solo toma MP3 pero la calidad del audio es la mejor
            #"-c:a", "aac",                     # códec de audio AAC (recomendado por YouTube)
            #"-b:a", "192k",                    # 128k, 192k(para trap queda genial por el flanger que genera), 320k bitrate de audio elevado para conservar calidad
            #"-ar", "48000",                    # frecuencia de muestreo ideal para YouTube

            # OUTPUT BEHAVIOR
            "-movflags", "+faststart",          # mejora el streaming progresivo (YouTube lo prefiere)
            "-shortest",                        # corta el video al final del audio

            self.output_path                    # ruta de salida del archivo .mp4
        ]
'''

'''
MODO DE USO:
from geckofects import generar_comando_gecko

cmd = generar_comando_gecko(
    mode="zoompan",
    mp3_path=self.mp3_path,
    cover_path=self.cover_path,
    output_path=self.output_path,
    duration=duracion,
    resolution="1280x720",
    zoom=self.chk_zoom.isChecked(),
    zoom_speed=zoom_speed,
    zoom_limit=1.1,
    pan=self.chk_pan.isChecked(),
    pan_speed=pan_speed,
    pan_axis=self.combo_eje.currentText()
)

subprocess.run(cmd)

'''

import subprocess
import os
from clases.geckocalc import obtener_duracion_mp3, obtener_duracion_mp3ffmpeg, obtener_duracion_video

def generar_comando_gecko(
    mode="basic",
    mp3_path=None,
    cover_path=None,
    output_path="output.mp4",
    duration=60,
    resolution="1280x720",
    zoom=False,
    zoom_speed=0.01,
    zoom_limit=1.1,
    pan=False,
    pan_speed=5,
    pan_axis="x",
    slideshow_images=None,
    text_overlay=None,
    concat_list_file=None,
    video_path=None
):
    """
    Genera el comando completo para ffmpeg según el modo de render elegido.

    Modo 'basic': MP3 + Imagen Fija → MP4
    Modo 'zoompan': Imagen con zoom y/o pan animado
    Modo 'slideshow': Secuencia de imágenes con fundido
    Modo 'add_audio_to_video': Agrega audio a un video sin audio
    Modo 'reverse': Reversar video y audio
    Modo 'draw_text': Superponer texto
    Modo 'concat': Concatenar lista de videos
    
    Devuelve:
    - lista de strings: comando para `subprocess.run(cmd)`
    """

    if mode == "basic":
        print("Geckofects Return basic Mode")
        
        return [
            "ffmpeg", "-hide_banner",           # evitar que nos aparezca información sobre el sistema y codecs
            "-y",                               # -y: sobrescribe el archivo de salida si ya existe
            "-loop", "1",                       # loopea la imagen (para que dure lo mismo que el audio)
            "-framerate", "2",                  # asegura que el contenedor tenga fps válido y bajo
            "-i", cover_path,                   # input imagen (portada del video)
            "-i", mp3_path,                     # input audio (mp3 o wav recomendado)

            # VIDEO ENCODING
            "-c:v", "libx264",                  # códec de video H.264
            "-preset", "slow",                  # optimiza compresión y calidad (más lento = mejor calidad)
            "-crf", "18",                       # calidad constante (menos = mejor calidad visual)
            "-tune", "stillimage",              # ajusta parámetros al tener imagen estática
            "-pix_fmt", "yuv420p",              # formato de pixeles compatible con YouTube

            # AUDIO ENCODING
            "-c:a", "copy",                     # sin comprimir el audio (solo MP3) mantiene calidad y es hiper veloz!!!
            #"-c:a", "aac",                     # códec de audio AAC (recomendado por YouTube)
            #"-b:a", "192k",                    # 128k, 192k (for Trap), 320k bitrate de audio elevado para conservar calidad
            #"-ar", "48000",                    # frecuencia de muestreo ideal para YouTube

            # OUTPUT BEHAVIOR
            "-movflags", "+faststart",          # mejora el streaming progresivo (YouTube lo prefiere)
            "-shortest",                        # corta el video al final del audio

            output_path                         # ruta de salida del archivo .mp4
        ]

    if mode == "zoompan":
        print("Geckofects Return zoompan Mode")
        # Construir filtro complejo
        zoom_expr = f"if(lte(zoom\\,{zoom_limit})\\,zoom+{zoom_speed}\\,zoom)" if zoom else "1.0"
        pan_expr_x = f"x+{pan_speed}" if pan and pan_axis in ["x", "diagonal"] else "x"
        pan_expr_y = f"y+{pan_speed}" if pan and pan_axis in ["y", "diagonal"] else "y"

        filtro = (
            f"[0:v]scale={resolution},"
            f"zoompan=z='{zoom_expr}':"
            f"x='{pan_expr_x}':y='{pan_expr_y}':"
            f"d=1:s={resolution},setpts=PTS-STARTPTS[v]"
        )

        return [
            "ffmpeg", "-y",
            "-loop", "1", "-i", cover_path,
            "-i", mp3_path,
            "-filter_complex", filtro,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264", "-c:a", "aac",
            "-b:a", "192k", "-shortest", "-pix_fmt", "yuv420p",
            output_path
        ]

    if mode == "slideshow" and slideshow_images:
        print("Geckofects Return slideshow Mode")
        cmd = ["ffmpeg", "-y"]
        filter_parts = []
        for i, img in enumerate(slideshow_images):
            cmd += ["-loop", "1", "-t", "5", "-i", img]
            if i == 0:
                continue
            offset = 4 * i
            in1 = f"[v{i-1}]" if i > 1 else "[0:v]"
            in2 = f"[{i}:v]"
            out = f"[v{i}]"
            xfade = f"{in1}{in2}xfade=transition=fade:duration=1:offset={offset}[v{i}]"
            filter_parts.append(xfade)

        filter_str = "; ".join(filter_parts)
        cmd += ["-filter_complex", filter_str, "-map", f"[v{len(slideshow_images)-1}]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", output_path]
        return cmd

    if mode == "add_audio_to_video":
        return [
            "ffmpeg", "-y", "-i", video_path, "-i", mp3_path,
            "-c:v", "copy", "-c:a", "aac", "-shortest", output_path
        ]

    if mode == "reverse":
        return [
            "ffmpeg", "-y", "-i", video_path,
            "-vf", "reverse", "-af", "areverse",
            output_path
        ]

    if mode == "draw_text" and text_overlay:
        return [
            "ffmpeg", "-y", "-i", video_path,
            "-vf", f"drawtext=text='{text_overlay}':fontcolor=white:fontsize=48:x=100:y=100",
            "-c:a", "copy", output_path
        ]

    if mode == "concat" and concat_list_file:
        return [
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_list_file,
            "-c", "copy", output_path
        ]

    # By Aetheris for Loop the Wan.ai short's cut's video // deprecated
    if mode == "loop_video_old" and video_path and mp3_path:
        print("Geckofects Return loop_video Mode")
        return [
            "ffmpeg", "-hide_banner", "-y",          # Sobrescribe y oculta info de codecs
            "-stream_loop", "-1",                    # Loop infinito del video
            "-i", video_path,                        # Input: video MP4 mudo
            "-i", mp3_path,                          # Input: audio MP3
            "-c:v", "copy",                          # Copia el video sin recompresión
            "-c:a", "aac",                           # Codifica audio a AAC (estándar YouTube)
            "-b:a", "192k",                          # Bitrate de audio
            "-shortest",                             # Corta al final del audio
            "-pix_fmt", "yuv420p",                   # Formato compatible con reproductores
            "-movflags", "+faststart",               # Optimización para streaming
            output_path                              # Ruta de salida
        ]
    
    if mode == "loop_video_ateheris":
        if not (video_path and mp3_path and os.path.exists(video_path) and os.path.exists(mp3_path)):
            print("Geckofects Error: Faltan archivos o no son válidos")
            return ["echo", "⚠️ Faltan archivos válidos para loop_video."]
        if not video_path.lower().endswith(".mp4"):
            print("Geckofects Error: El video debe ser MP4")
            return ["echo", "⚠️ El video debe ser un archivo MP4."]
        print("Geckofects Return loop_video Mode")
        # 👇 Usá la nueva función aquí (Ei2)
        durationm = obtener_duracion_mp3ffmpeg(mp3_path)
        if durationm <= 0:
            print("Geckofects Error: No se pudo obtener la duración confiable del MP3")
            return ["echo", "⚠️ Error al leer la duración del MP3."]
        print(f"La duracion del MP3 según ffmpeg es de {durationm} segundos")
        # Aetheris
        duration = obtener_duracion_mp3(mp3_path) 
        if duration <= 0:
            print("Geckofects Error: No se pudo obtener la duración del MP3")
            return ["echo", "⚠️ Error al leer la duración del MP3."]
        print(f"La duracion del MP3 según fprobe es de {duration} segundos")
        # Obtener duración del video mudo
        video_duration = obtener_duracion_video(video_path)
        if video_duration <= 0:
            print("Geckofects Error: No se pudo obtener la duración del video")
            return ["echo", "⚠️ Error al leer la duración del video."]
        print(f"La duracion del GeckoLoop Video según fprobe es de {video_duration} segundos")
        cmd = [
            "ffmpeg", "-hide_banner", "-y",
            "-stream_loop", "-1",
            # FILES
            "-i", video_path,
            "-i", mp3_path,
            # AUDIO
            "-c:a", "copy",
            #"-b:a", "192k",
            # ORDER PRIORITY
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-t", str(round(duration, 2)),
            # VIDEO
            #"-c:v", "copy",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23", #25
            #"-b:v", "1000k",
            #"-maxrate", "1000k",
            #"-bufsize", "2000k",
            # GeckoCut
            "-vf", "scale=1280:544:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black" # NOva DulceKali NOvaPythoniza
            #"-vf", "scale=1280:720:flags=lanczos, pad=1280:544:(ow-iw)/2:(oh-ih)/2:color=black" #UltraWide GeckoCut Format
            #"-vf", "crop=1280:544:0:((720-544)/2),pad=1280:544:(ow-iw)/2:(oh-ih)/2:color=black",   #solo toma la parte sup.izquierda
            #"-vf", "scale=1280:544:force_original_aspect_ratio=decrease,pad=1280:544:(ow-iw)/2:(oh-ih)/2", #fade=t=in:st=0:d=0.5,fade=t=out:st={video_duration - 0.5}:d=0.5", #saque el fade pero la salida es muy grande
            #"-vf", f"scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2, fade=t=in:st=0:d=0.5,fade=t=out:st={video_duration - 0.5}:d=0.5", #fade no funciona
            #"-vf", "fade=t=in:st=0:d=1,fade=t=out:st=" + str(video_duration - 1) + ":d=1",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_path
        ]
        # Aetheris for Debug
        print(f"[geckofects] Comando FFmpeg: {' '.join(cmd)}")
        print(f"🌌 GeckoCreator Render listo! Loop de {duration}s con {video_duration}s de base, salida en: {output_path}")
        return cmd
        '''
        cmd = [
            "ffmpeg",                   # Ejecuta FFmpeg, la herramienta de procesamiento multimedia.
            "-hide_banner",             # Suprime la información de versión y configuración de FFmpeg en la salida para mantener la consola limpia.
            "-y",                       # Sobrescribe el archivo de salida si ya existe, sin pedir confirmación.
            "-stream_loop", "-1",       # Repite el video de entrada (video_path) indefinidamente hasta que se corte por otro parámetro (como -t).
                                        # Opciones: "-1" (bucle infinito), "0" (sin bucle), o un número positivo (n repeticiones).
            # FILES
            "-i", video_path,           # Especifica el primer archivo de entrada (video mudo MP4). Asignado como entrada 0.
            "-i", mp3_path,             # Especifica el segundo archivo de entrada (audio MP3). Asignado como entrada 1.
            # AUDIO
            "-c:a", "copy",             # Copia el flujo de audio del MP3 sin recompresión, preservando calidad original y velocidad.
                                        # Opciones: "aac" (re-codifica a AAC), "mp3" (re-codifica a MP3), etc. "copy" es ideal para evitar artefactos.
            #"-b:a", "192k",            # Comentado: Habría fijado el bitrate de audio a 192 kbps (solo aplica si -c:a no es "copy").
                                        # Opciones: "128k", "256k", etc. No necesario con -c:a copy.
            # ORDER PRIORITY
            "-map", "0:v:0",            # Selecciona el primer flujo de video (v:0) de la entrada 0 (video_path) para el archivo de salida.
                                        # Asegura que el video mudo sea el flujo de video principal, evitando ambigüedades si hay múltiples flujos.
            "-map", "1:a:0",            # Selecciona el primer flujo de audio (a:0) de la entrada 1 (mp3_path) para el archivo de salida.
                                        # Garantiza que el audio del MP3 sea el flujo de audio principal.
            "-t", str(duration),        # Limita la duración del video de salida a la duración del MP3 (obtenida con obtener_duracion_mp3).
                                        # Evita que el bucle infinito (-stream_loop -1) genere un archivo gigante.
                                        # Opciones: Cualquier valor en segundos (float). Usamos la duración del MP3 para sincronizar.
            # VIDEO
            #"-c:v", "copy",            # Comentado: Habría copiado el flujo de video sin recompresión (rápido pero depende del códec original).
            "-c:v", "libx264",          # Re-codifica el video usando el códec H.264 (codificador libx264), altamente compatible.
                                        # Opciones: "copy" (sin recompresión), "libx265" (H.265, más eficiente pero menos compatible), etc.
            "-preset", "slow",          # Configura la velocidad de compresión de libx264. "slow" prioriza calidad sobre velocidad.
                                        # Opciones: "ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow".
                                        # Más lento = mejor calidad, menor tamaño. "slow" es un buen balance para calidad alta.
            "-crf", "18",               # Establece el factor de calidad constante para libx264 (0-51). 18 es alta calidad, tamaño moderado.
                                        # Opciones: 0 (sin pérdida), 23 (calidad balanceada), 51 (peor calidad). Menor CRF = mejor calidad, mayor tamaño.
            "-pix_fmt", "yuv420p",      # Establece el formato de píxeles a YUV 4:2:0, estándar para máxima compatibilidad con reproductores.
                                        # Opciones: "yuv444p" (mayor calidad, menos compatible), "yuv422p", etc. yuv420p es ideal para MP4.
            "-movflags", "+faststart",  # Mueve los metadatos al inicio del archivo MP4, permitiendo reproducción en streaming.
                                        # Opciones: Ninguna relevante aquí. +faststart es estándar para MP4.
            output_path                 # Ruta del archivo de salida (MP4). Ejemplo: "/ruta/GeckoLoop01.mp4".
        ]
        return cmd
    
        
            return [
                "ffmpeg", "-hide_banner", "-y",
                "-stream_loop", "-1",
                "-i", video_path,
                "-i", mp3_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                output_path
            ]
        '''

    # By Aetheris & NOva DulceKali NOvaPythoniza for Loop the Wan.ai short's resize & cut's video
    if mode == "loop_video":
        # Validamos paths y extensiones
        if not (video_path and mp3_path and os.path.exists(video_path) and os.path.exists(mp3_path)):
            print("Geckofects Error: Faltan archivos o no son válidos")
            return ["echo", "⚠️ Faltan archivos válidos para loop_video."]
        if not video_path.lower().endswith(".mp4"):
            print("Geckofects Error: El video debe ser MP4")
            return ["echo", "⚠️ El video debe ser un archivo MP4."]
        print("Geckofects Return loop_video Mode")
        # 👇 Usá la nueva función aquí para calcular duracion con ffmpeg (Ei2)
        durationm = obtener_duracion_mp3ffmpeg(mp3_path)
        if durationm <= 0:
            print("Geckofects Error: No se pudo obtener la duración confiable del MP3")
            return ["echo", "⚠️ Error al leer la duración del MP3."]
        print(f"La duracion del MP3 según ffmpeg es de {durationm} segundos")
        # duracion usando geckocalc.py by Aetheris
        duration = obtener_duracion_mp3(mp3_path) 
        if duration <= 0:
            print("Geckofects Error: No se pudo obtener la duración del MP3")
            return ["echo", "⚠️ Error al leer la duración del MP3."]
        print(f"La duracion del MP3 según fprobe es de {duration} segundos")
        # Obtener duración del video mudo by Aetheris
        video_duration = obtener_duracion_video(video_path)
        if video_duration <= 0:
            print("Geckofects Error: No se pudo obtener la duración del video")
            return ["echo", "⚠️ Error al leer la duración del video."]
        print(f"La duracion del GeckoLoop Video según fprobe es de {video_duration} segundos")
        # Armado del comando Geckoneano del GeckoLoop y el recorte GeckoCinematico NOva DulceKali NOvaPythoniza
        try:
            '''
            cmd = [
                "ffmpeg", "-hide_banner", "-y",
                "-stream_loop", "-1",
                "-i", video_path,
                "-i", mp3_path,
                "-c:a", "copy",
                "-map", "0:v:0", "-map", "1:a:0",
                "-t", str(round(duration, 2)),
                #"-c:v", "libx264",
                "-c:v", "h264_nvenc",
                "-preset", "fast",
                #"-crf", "23", #deprecated by NOva para mejor compatibilidad velocidad y tamaño de archivo.
                "-rc", "vbr",
                "-cq", "23",
                # UltraWide GeckoCut Format NOva DulceKali NOvaPythoniza
                "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,"
                     "crop=1280:544:(in_w-1280)/2:(in_h-544)/2",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                output_path
            ]
            '''
            # *************************************
            # Ultimo funcional hasta el 01/11/25 evaluar con cambio de version de ffmpeg
            '''
            # Loop de video Wan.ai con audio (GPU NVENC) by NOva DulceKali
            cmd = [
                "ffmpeg", "-hide_banner", "-y",
                "-stream_loop", "-1",
                "-i", video_path,
                "-i", mp3_path,
                "-c:a", "copy",
                "-map", "0:v:0", "-map", "1:a:0",
                "-t", str(round(duration, 2)),
                "-c:v", "h264_nvenc",
                "-preset", "fast",          # máxima velocidad razonable
                "-rc", "vbr",               # control de bitrate variable
                "-cq", "23",                # calidad constante para NVENC
                #"-vf", "scale=1280:720:force_original_aspect_ratio=decrease," #only for 1920x1080 inputs
                "-vf", "scale=1280:720:force_original_aspect_ratio=increase," #corrected by Gemini Ei2
                    "crop=1280:544:(in_w-1280)/2:(in_h-544)/2", 
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                output_path
            ]
            '''
            # *************************************
            # Comando modificado para agregar un overlay (logo.png) en la esquina superior derecha, redimensionado a 73x73
            # Las nuevas partes o modificadas están comentadas
            '''
            cmd = [
                "ffmpeg",
                "-hide_banner",
                "-y",
                "-stream_loop", "-1", "-i", video_path,
                "-i", mp3_path,
                "-i", "ruta/a/tu/logo_gecko.png",  # <--- 1. Tu logo PNG
                "-c:a", "copy",
                "-map", "1:a:0",
                "-t", str(round(duration, 2)),
                "-filter_complex",
                "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,crop=1280:544:(in_w-1280)/2:(in_h-544)/2[base];"  # Procesa el video base y lo nombra [base]
                "[2:v]scale=73:73[logo_redimensionado];"  # <--- 2. NUEVO: Redimensiona el logo y lo nombra [logo_redimensionado]
                "[base][logo_redimensionado]overlay=W-w-10:10",  # <--- 3. MODIFICADO: Usa el [logo_redimensionado] y lo posiciona en la esquina superior derecha
                "-c:v", "h264_nvenc",
                "-preset", "fast",
                "-rc", "vbr",
                "-cq", "23",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                output_path
            ]
            
            # Comando que solo agrega el overlay en sup derecha 73x73 con RTX
            # Comando para agregar el overlay al video base, también con la GPU
            cmd = [
                "ffmpeg",
                "-hide_banner", "-y",
                "-i", "video_base.mp4",  # <-- Video de Entrada
                "-i", "ruta/a/tu/logo_gecko.png",  # <-- Logo Entrada: tu logo
                "-filter_complex",
                "[1:v]scale=73:73[logo];"
                "[0:v][logo]overlay=W-w-10:10",
                "-c:a", "copy",  # Copiamos el audio que ya estaba en video_base.mp4
                "-c:v", "h264_nvenc",  # <-- Usando la GPU otra vez
                "-preset", "fast",
                "-rc", "vbr",
                "-cq", "23",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                output_path  # Archivo de salida final
            ]
            '''
            # Gemini Ei2 del 01/11/25 tras varias versiones y entredichos con Aetheris
            cmd = [
                "ffmpeg", "-hide_banner", "-y",
                "-stream_loop", "-1",
                "-i", video_path,
                "-i", mp3_path,
                "-c:a", "copy",
                "-map", "0:v:0", "-map", "1:a:0",
                "-t", str(round(duration, 2)),
                "-c:v", "h264_nvenc",
                "-preset", "fast",
                "-rc", "vbr",
                "-cq", "23",
                # --- LÍNEA CORREGIDA By Gemini Ei2 ---
                # Un solo string para -vf y usando "increase"
                "-vf", "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:544:(iw-ow)/2:(ih-oh)/2",
                # ---------------------
                #"-vf", "scale=1280:720:force_original_aspect_ratio=decrease,crop=1280:544:(iw-1280)/2:(ih-544)/2", #only for 1920x1080 inputs
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                output_path
            ]
            print(f"🌌 MSG From GeckoFects: [GeckonSola] retornando comando: {' '.join(cmd)}")
            print(f"🌌 MSG From GeckoFects: GeckoCreator Render Preparado para Loop de {duration}s con {video_duration}s de base, salida en: {output_path}")
            return cmd
        
        except Exception as e:
            print("⚠️ GeckoFects: Error inesperado en loop_video:", str(e))
            return ["echo", f"⚠️ GeckoFects: inesperado en loop_video: {str(e)}"]

    return ["echo", "⚠️ Modo no implementado o faltan parámetros."]
