from pathlib import Path

from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QGridLayout,
    QMessageBox,
)

from agenda_contactos.interfaz.estilos import obtener_estilo
from agenda_contactos.interfaz.ventana_contactos import VentanaContactos
from agenda_contactos.interfaz.ventana_exportar import VentanaExportar
from agenda_contactos.interfaz.ventana_herramientas import VentanaHerramientas
from agenda_contactos.almacenamiento.integridad import verificar_integridad
from agenda_contactos.contactos.servicio import ServicioContactos


RUTA_PROYECTO = Path(__file__).resolve().parents[3]


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.configuracion = QSettings("AgendaContactos", "AgendaContactos")
        self.tema = self.configuracion.value("tema", "claro", type=str)

        if self.tema not in ("claro", "oscuro"):
            self.tema = "claro"

        self.servicio = ServicioContactos()
        self.botones_menu = []
        self.tarjetas_inicio = {}

        self.setWindowTitle("Agenda de Contactos")
        self.setMinimumSize(1100, 700)

        contenedor = QWidget()
        contenedor.setObjectName("contenido_principal")

        layout_principal = QHBoxLayout(contenedor)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        self.crear_sidebar(layout_principal)
        self.crear_contenido(layout_principal)

        self.setCentralWidget(contenedor)
        self.aplicar_tema()

        self.ventana_contactos.contactos_actualizados.connect(
            self.actualizar_inicio
        )

        self.cambiar_seccion(0)
        self.verificar_archivo_integridad()

    def crear_sidebar(self, layout_principal):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(245)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 25, 18, 20)
        layout.setSpacing(10)

        logo = QLabel("AGENDA")
        logo.setObjectName("logo")

        logo_subtitulo = QLabel("GESTIÓN DE CONTACTOS")
        logo_subtitulo.setObjectName("logo_subtitulo")

        layout.addWidget(logo)
        layout.addWidget(logo_subtitulo)
        layout.addSpacing(28)

        opciones = [
            ("Inicio", 0),
            ("Contactos", 1),
            ("Exportar", 2),
            ("Herramientas", 3),
            ("Ayuda", 4),
        ]

        for nombre, indice in opciones:
            boton = QPushButton(nombre)
            boton.setObjectName("menu_boton")
            boton.setProperty("activo", False)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            boton.setMinimumHeight(42)
            boton.clicked.connect(
                lambda checked=False, i=indice: self.cambiar_seccion(i)
            )
            layout.addWidget(boton)
            self.botones_menu.append(boton)

        layout.addStretch()

        self.boton_tema = QPushButton()
        self.boton_tema.setObjectName("boton_tema")
        self.boton_tema.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_tema.clicked.connect(self.alternar_tema)
        layout.addWidget(self.boton_tema)

        version = QLabel("Agenda de Contactos\nVersión 1.0")
        version.setObjectName("logo_subtitulo")
        layout.addSpacing(12)
        layout.addWidget(version)

        layout_principal.addWidget(sidebar)

    def crear_contenido(self, layout_principal):
        contenedor = QWidget()
        contenedor.setObjectName("contenido_principal")

        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(30, 25, 30, 24)
        layout.setSpacing(16)

        encabezado_layout = QVBoxLayout()
        encabezado_layout.setSpacing(5)

        self.encabezado = QLabel()
        self.encabezado.setObjectName("titulo")

        self.descripcion = QLabel()
        self.descripcion.setObjectName("subtitulo")

        encabezado_layout.addWidget(self.encabezado)
        encabezado_layout.addWidget(self.descripcion)
        layout.addLayout(encabezado_layout)

        self.paginas = QStackedWidget()

        self.ventana_inicio = self.crear_inicio()
        self.ventana_contactos = VentanaContactos()
        self.ventana_exportar = VentanaExportar()
        self.ventana_herramientas = VentanaHerramientas()
        self.ventana_ayuda = self.crear_ayuda()

        self.paginas.addWidget(self.ventana_inicio)
        self.paginas.addWidget(self.ventana_contactos)
        self.paginas.addWidget(self.ventana_exportar)
        self.paginas.addWidget(self.ventana_herramientas)
        self.paginas.addWidget(self.ventana_ayuda)

        layout.addWidget(self.paginas, 1)
        layout_principal.addWidget(contenedor, 1)

    def crear_inicio(self):
        pagina = QWidget()
        pagina.setObjectName("pagina")

        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(18)

        titulo = QLabel("Resumen general")
        titulo.setObjectName("seccion_titulo")

        descripcion = QLabel(
            "Consulta el estado actual de tus contactos y archivos."
        )
        descripcion.setObjectName("seccion_descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        tarjetas = QGridLayout()
        tarjetas.setSpacing(14)

        datos = [
            ("Contactos registrados", "contactos"),
            ("Archivo de datos", "archivo"),
            ("Índice principal", "indice"),
            ("Integridad SHA-256", "integridad"),
        ]

        for columna, (nombre, clave) in enumerate(datos):
            tarjeta, valor = self.crear_tarjeta_inicio(nombre)
            self.tarjetas_inicio[clave] = valor
            tarjetas.addWidget(tarjeta, 0, columna)

        layout.addLayout(tarjetas)

        panel = QFrame()
        panel.setObjectName("panel_contenido")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 22, 24, 22)
        panel_layout.setSpacing(12)

        bienvenida = QLabel("Bienvenido a Agenda de Contactos")
        bienvenida.setObjectName("seccion_titulo")

        texto = QLabel(
            "Administra tu información mediante registros de tamaño fijo, "
            "acceso aleatorio e índice primario. Desde este sistema puedes "
            "registrar contactos, exportar reportes y proteger tus archivos."
        )
        texto.setObjectName("seccion_descripcion")
        texto.setWordWrap(True)

        panel_layout.addWidget(bienvenida)
        panel_layout.addWidget(texto)

        acciones = QHBoxLayout()
        acciones.setSpacing(10)

        boton_contactos = QPushButton("Administrar contactos")
        boton_contactos.setObjectName("boton_primario")
        boton_contactos.clicked.connect(
            lambda: self.cambiar_seccion(1)
        )

        boton_exportar = QPushButton("Exportar información")
        boton_exportar.clicked.connect(
            lambda: self.cambiar_seccion(2)
        )

        boton_herramientas = QPushButton("Herramientas")
        boton_herramientas.clicked.connect(
            lambda: self.cambiar_seccion(3)
        )

        acciones.addWidget(boton_contactos)
        acciones.addWidget(boton_exportar)
        acciones.addWidget(boton_herramientas)
        acciones.addStretch()

        panel_layout.addSpacing(5)
        panel_layout.addLayout(acciones)

        layout.addWidget(panel)
        layout.addStretch()

        return pagina

    def crear_tarjeta_inicio(self, titulo):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta_resumen")
        tarjeta.setMinimumHeight(125)

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(17, 15, 17, 15)
        layout.setSpacing(8)

        etiqueta = QLabel(titulo)
        etiqueta.setObjectName("tarjeta_titulo")
        etiqueta.setWordWrap(True)

        valor = QLabel("Consultando...")
        valor.setObjectName("tarjeta_valor")
        valor.setWordWrap(True)

        layout.addWidget(etiqueta)
        layout.addStretch()
        layout.addWidget(valor)

        return tarjeta, valor

    def crear_ayuda(self):
        pagina = QWidget()
        pagina.setObjectName("pagina")

        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(14)

        panel = QFrame()
        panel.setObjectName("panel_contenido")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 22, 24, 22)
        panel_layout.setSpacing(12)

        titulo = QLabel("Centro de ayuda")
        titulo.setObjectName("seccion_titulo")

        descripcion = QLabel(
            "Guía rápida para utilizar Agenda de Contactos."
        )
        descripcion.setObjectName("seccion_descripcion")

        instrucciones = [
            ("Contactos", "Registra nuevos contactos, busca por ID y modifica los datos existentes. Selecciona una fila para cargar sus datos en el formulario."),
            ("Exportar", "Genera el archivo contactos.json y el reporte PDF. El PDF se construye a partir del JSON actualizado."),
            ("Herramientas", "Verifica la integridad SHA-256, crea respaldos ZIP y consulta tamaño, fecha y permisos de los archivos."),
            ("Modo de visualización", "Utiliza el botón inferior del menú lateral para alternar entre el modo claro y el modo oscuro."),
        ]

        panel_layout.addWidget(titulo)
        panel_layout.addWidget(descripcion)

        for nombre, texto in instrucciones:
            encabezado = QLabel(nombre)
            encabezado.setStyleSheet("font-weight: 700;")
            detalle = QLabel(texto)
            detalle.setObjectName("seccion_descripcion")
            detalle.setWordWrap(True)
            panel_layout.addWidget(encabezado)
            panel_layout.addWidget(detalle)

        layout.addWidget(panel)
        layout.addStretch()
        return pagina

    def cambiar_seccion(self, indice):
        titulos = [
            ("Inicio", "Resumen general del sistema"),
            ("Contactos", "Administración de la información personal"),
            ("Exportar", "Generación de archivos y reportes"),
            ("Herramientas", "Administración y mantenimiento de archivos"),
            ("Ayuda", "Información y orientación del sistema"),
        ]

        titulo, descripcion = titulos[indice]
        self.encabezado.setText(titulo)
        self.descripcion.setText(descripcion)
        self.paginas.setCurrentIndex(indice)

        if indice == 0:
            self.actualizar_inicio()
        elif indice == 1:
            self.ventana_contactos.cargar_contactos()
        elif indice == 3:
            self.ventana_herramientas.actualizar_metadatos()

        for posicion, boton in enumerate(self.botones_menu):
            boton.setProperty("activo", posicion == indice)
            boton.style().unpolish(boton)
            boton.style().polish(boton)

    def actualizar_inicio(self):
        try:
            contactos = self.servicio.listar_contactos()
            self.tarjetas_inicio["contactos"].setText(str(len(contactos)))
        except (OSError, ValueError):
            self.tarjetas_inicio["contactos"].setText("No disponible")

        ruta_contactos = RUTA_PROYECTO / "data" / "contactos.dat"
        ruta_indice = RUTA_PROYECTO / "data" / "indice.json"

        self.tarjetas_inicio["archivo"].setText(
            f"{ruta_contactos.stat().st_size:,} bytes"
            if ruta_contactos.exists() else "No creado"
        )

        self.tarjetas_inicio["indice"].setText(
            "Disponible" if ruta_indice.exists() else "No creado"
        )

        try:
            estado, mensaje = verificar_integridad()
            estados = {
                "correcto": "Correcta",
                "alterado": "Alterada",
                "nuevo": "Inicializada",
                "sin_archivo": "Pendiente",
            }
            self.tarjetas_inicio["integridad"].setText(
                estados.get(estado, "No disponible")
            )
        except (OSError, ValueError):
            self.tarjetas_inicio["integridad"].setText("No disponible")

    def aplicar_tema(self):
        self.setStyleSheet(obtener_estilo(self.tema))
        if self.tema == "claro":
            self.boton_tema.setText("Cambiar a modo oscuro")
        else:
            self.boton_tema.setText("Cambiar a modo claro")

    def alternar_tema(self):
        self.tema = "oscuro" if self.tema == "claro" else "claro"
        self.configuracion.setValue("tema", self.tema)
        self.aplicar_tema()

    def verificar_archivo_integridad(self):
        try:
            estado, mensaje = verificar_integridad()

            if estado == "alterado":
                QMessageBox.warning(
                    self,
                    "Advertencia de integridad",
                    mensaje
                )

        except (OSError, ValueError) as error:
            QMessageBox.warning(
                self,
                "Error de integridad",
                str(error)
            )