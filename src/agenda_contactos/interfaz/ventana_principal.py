from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout
)
from PySide6.QtCore import Qt


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agenda de Contactos")
        self.setMinimumSize(1000, 650)

        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)

        titulo = QLabel("AGENDA DE CONTACTOS")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        descripcion = QLabel(
            "Sistema de administración de contactos "
            "con acceso aleatorio"
        )
        descripcion.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        self.setCentralWidget(contenedor)