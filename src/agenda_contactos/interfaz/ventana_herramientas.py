from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from agenda_contactos.almacenamiento.respaldo import crear_respaldo
from agenda_contactos.almacenamiento.metadatos import consultar_metadatos


class VentanaHerramientas(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Herramientas del sistema")

        self.crear_interfaz()
        self.actualizar_metadatos()

    def crear_interfaz(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 15, 20, 15)
        layout_principal.setSpacing(15)

        titulo = QLabel("Herramientas del sistema")
        titulo.setObjectName("seccion_titulo")

        descripcion = QLabel(
            "Administra los respaldos y consulta la información "
            "de los archivos del sistema."
        )
        descripcion.setWordWrap(True)

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(18, 15, 18, 15)
        layout_tarjeta.setSpacing(10)

        subtitulo = QLabel("Respaldo de archivos")
        subtitulo.setObjectName("subtitulo")

        detalle = QLabel(
            "Genera una copia comprimida de contactos.dat "
            "e indice.json."
        )
        detalle.setWordWrap(True)

        boton_respaldo = QPushButton("Crear respaldo ZIP")
        boton_respaldo.clicked.connect(self.generar_respaldo)

        self.resultado = QLabel(
            "Todavía no se ha generado un respaldo."
        )
        self.resultado.setWordWrap(True)

        layout_tarjeta.addWidget(subtitulo)
        layout_tarjeta.addWidget(detalle)
        layout_tarjeta.addWidget(boton_respaldo)
        layout_tarjeta.addWidget(self.resultado)

        subtitulo_metadatos = QLabel("Metadatos y permisos")
        subtitulo_metadatos.setObjectName("subtitulo")

        boton_actualizar = QPushButton("Actualizar información")
        boton_actualizar.clicked.connect(self.actualizar_metadatos)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Archivo",
            "Tamaño",
            "Modificación",
            "Lectura",
            "Escritura",
            "Estado"
        ])

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.tabla.horizontalHeader().setStretchLastSection(True)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descripcion)
        layout_principal.addWidget(tarjeta)
        layout_principal.addWidget(subtitulo_metadatos)
        layout_principal.addWidget(boton_actualizar)
        layout_principal.addWidget(self.tabla, 1)

    def generar_respaldo(self):
        try:
            resultado = crear_respaldo()

            self.resultado.setText(
                f"Respaldo creado correctamente.\n"
                f"Ubicación: {resultado['ruta']}\n"
                f"Tamaño original: "
                f"{resultado['tamano_original']} bytes\n"
                f"Tamaño comprimido: "
                f"{resultado['tamano_comprimido']} bytes"
            )

            self.actualizar_metadatos()

            QMessageBox.information(
                self,
                "Respaldo creado",
                "El respaldo ZIP se generó correctamente."
            )

        except (OSError, ValueError) as error:
            QMessageBox.critical(
                self,
                "Error al crear respaldo",
                str(error)
            )

    def actualizar_metadatos(self):
        try:
            resultados = consultar_metadatos()

            self.tabla.setRowCount(len(resultados))

            for fila, datos in enumerate(resultados):
                valores = [
                    datos["nombre"],
                    datos["tamano"],
                    datos["modificacion"],
                    datos["lectura"],
                    datos["escritura"],
                    datos["estado"]
                ]

                for columna, valor in enumerate(valores):
                    elemento = QTableWidgetItem(str(valor))
                    self.tabla.setItem(fila, columna, elemento)

        except OSError as error:
            QMessageBox.warning(
                self,
                "Error de metadatos",
                str(error)
            )