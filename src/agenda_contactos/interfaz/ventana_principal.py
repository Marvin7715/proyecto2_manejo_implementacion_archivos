from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QGridLayout
)
from PySide6.QtCore import Qt

from agenda_contactos.interfaz.estilos import (
    COLORES,
    ESTILO_GENERAL
)


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agenda de Contactos")
        self.setMinimumSize(1100, 700)
        self.resize(1250, 780)

        self.botones_menu = []

        contenedor = QWidget()
        layout_principal = QHBoxLayout(contenedor)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        self.crear_sidebar(layout_principal)
        self.crear_contenido(layout_principal)

        self.setCentralWidget(contenedor)
        self.setStyleSheet(ESTILO_GENERAL)

        self.cambiar_seccion(0)

    def crear_sidebar(self, layout_principal):

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(245)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 25, 18, 20)
        layout.setSpacing(12)

        logo = QLabel("AGENDA")
        logo.setObjectName("logo")

        logo_subtitulo = QLabel("GESTIÓN DE CONTACTOS")
        logo_subtitulo.setObjectName("logo_subtitulo")

        layout.addWidget(logo)
        layout.addWidget(logo_subtitulo)
        layout.addSpacing(35)

        opciones = [
            ("Inicio", 0),
            ("Contactos", 1),
            ("Exportar", 2),
            ("Herramientas", 3),
            ("Ayuda", 4)
        ]

        for nombre, indice in opciones:
            boton = QPushButton(nombre)
            boton.setObjectName("menu_boton")
            boton.setProperty("activo", False)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            boton.clicked.connect(
                lambda checked=False, i=indice: self.cambiar_seccion(i)
            )

            layout.addWidget(boton)
            self.botones_menu.append(boton)

        layout.addStretch()

        version = QLabel("Agenda de Contactos\nVersión 1.0")
        version.setObjectName("logo_subtitulo")
        layout.addWidget(version)

        layout_principal.addWidget(sidebar)

    def crear_contenido(self, layout_principal):

        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(30, 27, 30, 25)
        layout.setSpacing(20)

        self.encabezado = QLabel()
        self.encabezado.setObjectName("titulo")

        self.descripcion = QLabel()
        self.descripcion.setObjectName("subtitulo")

        layout.addWidget(self.encabezado)
        layout.addWidget(self.descripcion)

        self.paginas = QStackedWidget()

        self.paginas.addWidget(self.crear_inicio())
        self.paginas.addWidget(self.crear_pagina(
            "Gestión de contactos",
            "Aquí podremos agregar, buscar y modificar contactos."
        ))
        self.paginas.addWidget(self.crear_pagina(
            "Exportación de información",
            "Aquí generaremos los archivos JSON y los reportes PDF."
        ))
        self.paginas.addWidget(self.crear_pagina(
            "Herramientas del sistema",
            "Aquí verificaremos la integridad, crearemos respaldos "
            "y consultaremos la información de los archivos."
        ))
        self.paginas.addWidget(self.crear_pagina(
            "Centro de ayuda",
            "Información general sobre el funcionamiento del sistema."
        ))

        layout.addWidget(self.paginas)
        layout_principal.addWidget(contenedor)

    def crear_inicio(self):

        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(22)

        titulo = QLabel("Resumen de la agenda")
        titulo.setObjectName("seccion_titulo")

        descripcion = QLabel(
            "Consulta general del estado de tus contactos."
        )
        descripcion.setObjectName("seccion_descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        tarjetas = QGridLayout()
        tarjetas.setSpacing(15)

        datos = [
            ("Contactos registrados", "0"),
            ("Archivo de datos", "No creado"),
            ("Índice principal", "No creado")
        ]

        for columna, (nombre, valor) in enumerate(datos):
            tarjeta = self.crear_tarjeta(nombre, valor)
            tarjetas.addWidget(tarjeta, 0, columna)

        layout.addLayout(tarjetas)

        panel = QFrame()
        panel.setObjectName("panel_contenido")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(25, 25, 25, 25)
        panel_layout.setSpacing(12)

        panel_titulo = QLabel("Bienvenido a Agenda de Contactos")
        panel_titulo.setObjectName("seccion_titulo")

        panel_texto = QLabel(
            "Administra tu información de manera organizada mediante "
            "registros de tamaño fijo y acceso aleatorio."
        )
        panel_texto.setWordWrap(True)
        panel_texto.setObjectName("seccion_descripcion")

        panel_layout.addWidget(panel_titulo)
        panel_layout.addWidget(panel_texto)

        layout.addWidget(panel)
        layout.addStretch()

        return pagina

    def crear_tarjeta(self, titulo, valor):

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        tarjeta.setMinimumHeight(125)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(20, 18, 20, 18)

        etiqueta = QLabel(titulo)
        etiqueta.setObjectName("tarjeta_titulo")

        dato = QLabel(valor)
        dato.setObjectName("tarjeta_valor")

        layout.addWidget(etiqueta)
        layout.addStretch()
        layout.addWidget(dato)

        return tarjeta

    def crear_pagina(self, titulo, descripcion):

        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(0, 15, 0, 0)

        panel = QFrame()
        panel.setObjectName("panel_contenido")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(25, 25, 25, 25)

        etiqueta_titulo = QLabel(titulo)
        etiqueta_titulo.setObjectName("seccion_titulo")

        etiqueta_descripcion = QLabel(descripcion)
        etiqueta_descripcion.setObjectName("seccion_descripcion")
        etiqueta_descripcion.setWordWrap(True)

        panel_layout.addWidget(etiqueta_titulo)
        panel_layout.addWidget(etiqueta_descripcion)
        panel_layout.addStretch()

        layout.addWidget(panel)
        layout.addStretch()

        return pagina

    def cambiar_seccion(self, indice):

        titulos = [
            ("Inicio", "Resumen general del sistema"),
            ("Contactos", "Administración de la información personal"),
            ("Exportar", "Generación de archivos y reportes"),
            ("Herramientas", "Administración y mantenimiento de archivos"),
            ("Ayuda", "Información y orientación del sistema")
        ]

        titulo, descripcion = titulos[indice]

        self.encabezado.setText(titulo)
        self.descripcion.setText(descripcion)
        self.paginas.setCurrentIndex(indice)

        for posicion, boton in enumerate(self.botones_menu):
            boton.setProperty("activo", posicion == indice)
            boton.style().unpolish(boton)
            boton.style().polish(boton)