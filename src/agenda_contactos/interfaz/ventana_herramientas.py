from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from agenda_contactos.almacenamiento.respaldo import crear_respaldo
from agenda_contactos.almacenamiento.metadatos import consultar_metadatos
from agenda_contactos.almacenamiento.integridad import verificar_integridad


class VentanaHerramientas(QWidget):

    def __init__(self):
        super().__init__()

        self.crear_interfaz()
        self.actualizar_metadatos()

    def crear_interfaz(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 5, 0, 0)
        layout_principal.setSpacing(14)

        panel_acciones = QFrame()
        panel_acciones.setObjectName("panel_contenido")

        layout_acciones = QVBoxLayout(panel_acciones)
        layout_acciones.setContentsMargins(20, 17, 20, 17)
        layout_acciones.setSpacing(12)

        titulo = QLabel("Mantenimiento de archivos")
        titulo.setObjectName("seccion_titulo")

        descripcion = QLabel(
            "Verifica la integridad de la información y administra "
            "copias de seguridad de los archivos principales."
        )
        descripcion.setObjectName("seccion_descripcion")
        descripcion.setWordWrap(True)

        layout_acciones.addWidget(titulo)
        layout_acciones.addWidget(descripcion)

        botones = QHBoxLayout()
        botones.setSpacing(10)

        self.boton_verificar = QPushButton("Verificar integridad SHA-256")
        self.boton_verificar.setObjectName("boton_primario")
        self.boton_verificar.clicked.connect(self.verificar_hash)

        self.boton_respaldo = QPushButton("Crear respaldo ZIP")
        self.boton_respaldo.setObjectName("boton_exito")
        self.boton_respaldo.clicked.connect(self.generar_respaldo)

        botones.addWidget(self.boton_verificar)
        botones.addWidget(self.boton_respaldo)
        botones.addStretch()

        layout_acciones.addLayout(botones)

        self.estado_integridad = QLabel(
            "La verificación de integridad está disponible."
        )
        self.estado_integridad.setObjectName("estado")
        self.estado_integridad.setWordWrap(True)

        self.resultado_respaldo = QLabel(
            "Todavía no se ha generado un respaldo en esta sesión."
        )
        self.resultado_respaldo.setObjectName("estado")
        self.resultado_respaldo.setWordWrap(True)

        layout_acciones.addWidget(self.estado_integridad)
        layout_acciones.addWidget(self.resultado_respaldo)

        panel_metadatos = QFrame()
        panel_metadatos.setObjectName("panel_contenido")

        layout_metadatos = QVBoxLayout(panel_metadatos)
        layout_metadatos.setContentsMargins(18, 15, 18, 15)
        layout_metadatos.setSpacing(10)

        encabezado = QHBoxLayout()

        titulo_metadatos = QLabel("Información del archivo")
        titulo_metadatos.setObjectName("seccion_titulo")

        boton_actualizar = QPushButton("Actualizar información")
        boton_actualizar.clicked.connect(self.actualizar_metadatos)

        encabezado.addWidget(titulo_metadatos)
        encabezado.addStretch()
        encabezado.addWidget(boton_actualizar)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "Archivo",
            "Tamaño",
            "Última modificación",
            "Lectura",
            "Escritura",
            "Estado",
        ])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setMinimumHeight(190)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setDefaultSectionSize(36)
        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout_metadatos.addLayout(encabezado)
        layout_metadatos.addWidget(self.tabla)

        layout_principal.addWidget(panel_acciones)
        layout_principal.addWidget(panel_metadatos, 1)

    def verificar_hash(self):
        try:
            estado, mensaje = verificar_integridad()
            self.estado_integridad.setText(mensaje)

            if estado == "correcto":
                QMessageBox.information(
                    self,
                    "Integridad verificada",
                    "El archivo contactos.dat conserva su integridad."
                )
            elif estado == "alterado":
                QMessageBox.warning(
                    self,
                    "Advertencia de integridad",
                    mensaje
                )
            elif estado == "nuevo":
                QMessageBox.information(
                    self,
                    "Hash inicial creado",
                    mensaje
                )
            else:
                QMessageBox.information(
                    self,
                    "Sin archivo de contactos",
                    mensaje
                )

            self.actualizar_metadatos()

        except (OSError, ValueError) as error:
            QMessageBox.critical(
                self,
                "Error de integridad",
                str(error)
            )

    def generar_respaldo(self):
        try:
            resultado = crear_respaldo()

            original = resultado["tamano_original"]
            comprimido = resultado["tamano_comprimido"]

            if original > 0:
                porcentaje = (1 - comprimido / original) * 100
                comparacion = (
                    f"Variación de tamaño: {porcentaje:.2f}% "
                    "(un valor positivo indica reducción)."
                )
            else:
                comparacion = "No se pudo calcular la variación de tamaño."

            self.resultado_respaldo.setText(
                f"Respaldo creado: {resultado['ruta']}\n"
                f"Tamaño original: {original:,} bytes\n"
                f"Tamaño comprimido: {comprimido:,} bytes\n"
                f"{comparacion}"
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
                    datos["estado"],
                ]

                for columna, valor in enumerate(valores):
                    elemento = QTableWidgetItem(str(valor))
                    self.tabla.setItem(fila, columna, elemento)

            self.tabla.resizeRowsToContents()

        except (OSError, ValueError) as error:
            QMessageBox.warning(
                self,
                "Error de metadatos",
                str(error)
            )