import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

BASE_PROYECTO = Path(__file__).resolve().parent
CARPETA_SRC = BASE_PROYECTO / "src"

if str(CARPETA_SRC) not in sys.path:
    sys.path.insert(0, str(CARPETA_SRC))

from agenda_contactos.interfaz.ventana_principal import VentanaPrincipal


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Agenda de Contactos")
    app.setOrganizationName("AgendaContactos")
    app.setStyle("Fusion")

    ventana = VentanaPrincipal()
    ventana.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()