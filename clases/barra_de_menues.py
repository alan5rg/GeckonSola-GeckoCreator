'''
 INCLUYE ESTILOS, SE CREAN EN EL MISMO MENU
 💚 PALETA GECKONEANA: análisis espiritual y técnico
 🖼️ Tema	🔍 Análisis DulceKaliano
Estudio Clásico Gecko	Ese #659665 para el borde lo vuelve vintage profesional, más sobrio y menos neón. Un Gecko en modo analógico.
Consola Gecko Matrix	¡Sí! Ahora los textos se leen sin perder la esencia hacker. Ese #0D8D02 es verde terminal espiritual.
Nave Klingon	¡ALERTA TOTAL! 🔴 #ffee00 como texto sobre rojo-sangre hace que todo vibre. Acá Gecko edita desde el puente, bajo ataque, con honores.
Edición Nocturna	Más intensa y profesional. Ese #00c500 le da un toque oscuro pero vivo. Ideal para edición mental.
Jungle Gecko	Pasaste de selva a jungla digital tropical. #0B470B y #2de45b es hoja y savia. Me hace sentir que Gecko está editando con lianas colgando.
CyberParty 1997	¡TRON + FM Party! El amarillo #fffb00 con fucsia y violeta es un viaje. Visual rave asegurada.
Azul Servidor Cuántico	Más sobrio, más confiable. #0084ff es puro dataflow con profundidad. Me hace sentir que Gecko está editando dentro de un D-Wave.
Shamballa	Suave, divino, sin estridencias. Como Gecko con incienso tibetano y cristales líquidos.
'''

from PyQt5.QtWidgets import QMenuBar, QAction, QMessageBox

class BarraDeMenues(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.acciones_tema = {}
        self.crear_menu_config()
        self.crear_menu_estudio()
        self.crear_menu_ayuda()
        self.crear_menu_acerca()
        self.crear_menu_salir()

    def crear_menu_config(self):
        '''menu para configuraciones'''
        self.menu_conf = self.addMenu("Config's GeckoNeanas")

        guardar_acc = QAction ("Guardar Configuracion Actual", self)
        guardar_acc.triggered.connect(self.parent.guardar_config)
        self.menu_conf.addAction(guardar_acc)
        
        cargar_acc = QAction ("Cargar Configuracion desde Archivo .pkl", self)
        cargar_acc.triggered.connect(self.mostrar_tips)
        self.menu_conf.addAction(cargar_acc)

    def conectar_tema(self, accion, nombre, colores):
        # Conectar señal triggered para clics
        call="select"
        accion.triggered.connect(lambda checked: self.parent.aplicar_tema(nombre, *colores, call))
        # Conectar la señal hovered de cada QAction individualmente
        accion.hovered.connect(lambda: self.efecto_hover_tema(accion, nombre, colores))
        self.acciones_tema[accion] = (nombre, colores)

    def crear_menu_estudio(self):
        self.menu_estudio = self.addMenu("🎨 Enchulame el Estudio")
        
        temas = {
            "Estudio Clásico Gecko": ("#ccffcc", "#659665", "#000000"),
            "Estudio Clásico II Gecko": ("#fff3bb", "#659665", "#000000"),
            "Consola Gecko Matrix": ("#111111", "#00ff00", "#0D8D02"),
            "Nave Klingon": ("#1c0000", "#ff3333", "#ffee00"),
            "Edición Nocturna": ("#0a0a2a", "#00c500", "#ffffff"),
            "Jungle Gecko": ("#0B470B", "#2de45b", "#ffffff"),
            "CyberParty 1997": ("#1a0033", "#ff66ff", "#fffb00"),
            "Azul Servidor Cuántico": ("#001122", "#0084ff", "#ffffff"),
            "Shamballa": ("#fff9e6", "#c49f2b", "#000000"),
            "Museo del Tiempo": ("#f8f0e3", "#6e4b1f", "#000000"),
            "Charreteras del Chamaco": ("#fff0ff", "#ff1a8c", "#5200ff"),
            "LVHR.4": ("#1f001f", "#ff6600", "#ff00ff"),
            "Púrpura Serpiente DulceKali": ("#2e003e", "#ffb3ff", "#ffffff"),
            "Cámara de los Mil Decisiones": ("#001a33", "#33ffff", "#ffffff"),
            "DulceBot de Edición": ("#fff0f5", "#ff4da6", "#000000"),
            "BunnyIndicator": ("#e6fff9", "#33cccc", "#00334d"),
            "Duplicador Cuántico": ("#000022", "#00ffff", "#ff00ff"),
            "Monkey Python Coding Circus": ("#fff5cc", "#ff9900", "#663300"),
            # Themes by Aetheris for Visual Care
            "Eclipse Geckoniano": ("#1f2521", "#4a7043", "#f5e8c7"),  # Gris oscuro, verde musgo suave, blanco cálido
            "Noche en el Balcón Matrix": ("#0d1117", "#4d8299", "#c7d1d8"),  # Casi negro, cian apagado, gris claro
            "Cueva del Código Cósmico": ("#1c2526", "#6b5b95", "#e0d7c3"),  # Azul-gris oscuro, morado tenue, marfil suave
        }

        for nombre, colores in temas.items():
            accion = QAction(nombre, self)
            self.menu_estudio.addAction(accion)
            self.conectar_tema(accion, nombre, colores)
            accion.setCheckable(True)
            accion.setChecked(False)
        
        # Alternativa: Conectar la señal hovered del menú completo
        #self.menu_estudio.hovered.connect(self.efecto_hover_tema)

        # Conectar señal aboutToHide para restaurar el tema seleccionado
        self.menu_estudio.aboutToHide.connect(self.restaurar_tema_seleccionado)

    def efecto_hover_tema(self, accion, nombre, colores):
        call="hover"
        #print(f"[DEBUG] Hover detectado en: {accion.text()}")
        if accion in self.acciones_tema:
            nombre, colores = self.acciones_tema[accion]
            self.parent.aplicar_tema(nombre, *colores, call)
        self.tildar_seleccion()

    def restaurar_tema_seleccionado(self):
        call="rest"
        # Restaurar el tema seleccionado al ocultar el menú
        if self.parent.tema_seleccionado:
            nombre = self.parent.tema_seleccionado[0]
            self.tildar_seleccion()
            colores = (self.parent.tema_seleccionado[1],self.parent.tema_seleccionado[2],self.parent.tema_seleccionado[3])
            #print(f"[DEBUG] Restaurando tema: {nombre}")
            self.parent.aplicar_tema(nombre, *colores, call)

        else:
            #print("[DEBUG] No hay tema seleccionado, usando tema por defecto")
            # Opcional: Aplicar un tema por defecto si no hay tema seleccionado
            self.parent.aplicar_tema("Estudio Clásico Gecko", "#ccffcc", "#659665", "#000000", call)
            self.tildar_seleccion()

    def tildar_seleccion(self):
        nombre = self.parent.tema_seleccionado[0]
        # Seleccionar y deseleccionar opciones
        for accion in self.acciones_tema:
            nombremenu, colores = self.acciones_tema[accion]
            # print(f"[DEBUG] Tema: {nombremenu}")
            accion.setChecked(False)
            if nombremenu == nombre:
                accion.setChecked(True)

    def crear_menu_ayuda(self):
        self.menu_ayuda = self.addMenu("🧠 Ayuda me Geckonizo")
        accion = QAction("Mostrar tips mágicos", self)
        accion.triggered.connect(self.mostrar_tips)
        self.menu_ayuda.addAction(accion)

    def crear_menu_acerca(self):
        self.menu_acerca = self.addMenu("🔍 Acerca de Gecko")
        accion = QAction("Sobre esta app", self)
        accion.triggered.connect(self.mostrar_acerca)
        self.menu_acerca.addAction(accion)

    def crear_menu_salir(self):
        self.menu_salir = self.addMenu("🚪 Salir Solo con Gloria (Divina)")
        accion = QAction("¡Adiós, gloriosamente!", self)
        accion.triggered.connect(self.salir_con_gloria)
        self.menu_salir.addAction(accion)

    def mostrar_tips(self):
        QMessageBox.information(self, "Tips Geckoneanos", 
            "🦎 Consejos para usar GeckoMP4Creator:\n\n"
            "- Crear videos con solo dos clics\n"
            "- Reproducir desde la playlist lateral\n"
            "- Hacé clic derecho para agregar manualmente\n"
            "- Probá los temas... cada uno invoca una energía diferente\n"
            "- Y recordá... Gecko nunca duerme")

    def mostrar_acerca(self):
        QMessageBox.information(self, "Sobre Gecko", 
            "GeckoMP4Creator v1.0\n\n"
            "Hecho con amor por Alan & DulceKali\n"
            "Consola audiovisual impulsada por bananas\n"
            "Mirá los resultados en YouTube... y seguí creando 💚")

    def salir_con_gloria(self):
        QMessageBox.information(self, "Gecko te despide", 
            "🦎 Que tu salida sea gloriosa, divina y renderizada.\n"
            "¡Hasta el próximo render!")
        self.parent.close()       
