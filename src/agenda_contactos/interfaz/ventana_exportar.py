from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFrame
)

from agenda_contactos.contactos.servicio import ServicioContactos
from agenda_contactos.exportaciones.json_exportador import (
    exportar_contactos_json
)
from agenda_contactos.exportaciones.pdf_exportador import (
    generar_reporte_pdf
)


class VentanaExportar(QWidget):

    def __init__(self):
        super().__init__()

        self.servicio = ServicioContactos()

        self.construir_interfaz()

    def construir_interfaz(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(18)

        panel = QFrame()
        panel.setObjectName("panel_contenido")

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(25, 25, 25, 25)
        panel_layout.setSpacing(15)

        titulo = QLabel("Exportación de información")
        titulo.setObjectName("seccion_titulo")

        descripcion = QLabel(
            "Genera una copia de los contactos en formato JSON "
            "y un reporte PDF con la información exportada."
        )
        descripcion.setObjectName("seccion_descripcion")
        descripcion.setWordWrap(True)

        self.boton_json = QPushButton("Exportar contactos a JSON")
        self.boton_pdf = QPushButton("Generar reporte PDF")

        self.estado = QLabel(
            "Los archivos se guardarán en la carpeta exports."
        )
        self.estado.setObjectName("seccion_descripcion")
        self.estado.setWordWrap(True)

        panel_layout.addWidget(titulo)
        panel_layout.addWidget(descripcion)
        panel_layout.addSpacing(10)
        panel_layout.addWidget(self.boton_json)
        panel_layout.addWidget(self.boton_pdf)
        panel_layout.addWidget(self.estado)

        layout.addWidget(panel)
        layout.addStretch()

        self.boton_json.clicked.connect(self.exportar_json)
        self.boton_pdf.clicked.connect(self.exportar_pdf)

    def exportar_json(self):
        try:
            contactos = self.servicio.listar_contactos()
            ruta = exportar_contactos_json(contactos)

            self.estado.setText(
                f"Archivo JSON generado correctamente:\n{ruta}"
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
            ruta = generar_reporte_pdf()

            self.estado.setText(
                f"Reporte PDF generado correctamente:\n{ruta}"
            )

            QMessageBox.information(
                self,
                "Reporte generado",
                f"El reporte PDF se creó correctamente.\n\n{ruta}"
            )

        except (ValueError, OSError) as error:
            QMessageBox.warning(
                self,
                "Error al generar PDF",
                str(error)
            )