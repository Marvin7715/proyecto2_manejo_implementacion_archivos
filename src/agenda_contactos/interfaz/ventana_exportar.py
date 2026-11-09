from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox,
)

from agenda_contactos.contactos.servicio import ServicioContactos
from agenda_contactos.exportaciones.json_exportador import exportar_contactos_json
from agenda_contactos.exportaciones.pdf_exportador import generar_reporte_pdf


class VentanaExportar(QWidget):

    def __init__(self):
        super().__init__()

        self.servicio = ServicioContactos()
        self.construir_interfaz()

    def construir_interfaz(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 0)
        layout.setSpacing(16)

        panel = QFrame()
        panel.setObjectName("panel_contenido")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 22, 24, 22)
        panel_layout.setSpacing(14)

        titulo = QLabel("Exportación de información")
        titulo.setObjectName("seccion_titulo")

        descripcion = QLabel(
            "Genera archivos externos con los contactos registrados. "
            "El reporte PDF se construye utilizando el archivo JSON actualizado."
        )
        descripcion.setObjectName("seccion_descripcion")
        descripcion.setWordWrap(True)

        panel_layout.addWidget(titulo)
        panel_layout.addWidget(descripcion)

        tarjetas = QHBoxLayout()
        tarjetas.setSpacing(14)

        tarjeta_json = self.crear_tarjeta(
            "Exportación JSON",
            "Genera contactos.json con todos los registros de la agenda.",
            "Exportar contactos a JSON",
            "boton_primario",
            self.exportar_json,
        )

        tarjeta_pdf = self.crear_tarjeta(
            "Reporte PDF",
            "Genera un documento PDF con la fecha de creación y la tabla de contactos.",
            "Generar reporte PDF",
            "boton_exito",
            self.exportar_pdf,
        )

        tarjetas.addWidget(tarjeta_json)
        tarjetas.addWidget(tarjeta_pdf)

        panel_layout.addLayout(tarjetas)

        self.estado = QLabel(
            "Los archivos generados se almacenan en la carpeta exports."
        )
        self.estado.setObjectName("estado")
        self.estado.setWordWrap(True)

        panel_layout.addWidget(self.estado)

        layout.addWidget(panel)
        layout.addStretch()

    def crear_tarjeta(self, titulo, descripcion, texto_boton, estilo_boton, accion):
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")

        contenido = QVBoxLayout(tarjeta)
        contenido.setContentsMargins(18, 18, 18, 18)
        contenido.setSpacing(12)

        etiqueta = QLabel(titulo)
        etiqueta.setObjectName("seccion_titulo")

        detalle = QLabel(descripcion)
        detalle.setObjectName("seccion_descripcion")
        detalle.setWordWrap(True)
        detalle.setMinimumHeight(55)

        boton = QPushButton(texto_boton)
        boton.setObjectName(estilo_boton)
        boton.clicked.connect(accion)

        contenido.addWidget(etiqueta)
        contenido.addWidget(detalle)
        contenido.addStretch()
        contenido.addWidget(boton)

        return tarjeta

    def exportar_json(self):
        try:
            contactos = self.servicio.listar_contactos()

            if not contactos:
                raise ValueError(
                    "No hay contactos registrados para exportar."
                )

            ruta = exportar_contactos_json(contactos)

            self.estado.setText(
                f"JSON generado correctamente: {ruta}"
            )

            QMessageBox.information(
                self,
                "Exportación completada",
                f"Se exportaron {len(contactos)} contactos.\n\n{ruta}"
            )

        except (ValueError, OSError) as error:
            QMessageBox.warning(
                self,
                "Error de exportación",
                str(error)
            )

    def exportar_pdf(self):
        try:
            contactos = self.servicio.listar_contactos()

            if not contactos:
                raise ValueError(
                    "No hay contactos registrados para generar el reporte."
                )

            ruta_json = exportar_contactos_json(contactos)
            ruta_pdf = generar_reporte_pdf()

            self.estado.setText(
                f"JSON actualizado: {ruta_json}\n"
                f"Reporte PDF generado: {ruta_pdf}"
            )

            QMessageBox.information(
                self,
                "Reporte generado",
                f"El reporte PDF se creó correctamente.\n\n{ruta_pdf}"
            )

        except (ValueError, OSError) as error:
            QMessageBox.warning(
                self,
                "Error al generar PDF",
                str(error)
            )