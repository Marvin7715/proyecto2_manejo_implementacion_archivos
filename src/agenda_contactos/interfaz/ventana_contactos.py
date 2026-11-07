from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView
)

from agenda_contactos.contactos.modelo import Contacto
from agenda_contactos.contactos.servicio import ServicioContactos


class VentanaContactos(QWidget):

    def __init__(self):
        super().__init__()

        self.servicio = ServicioContactos()
        self.contacto_seleccionado = None

        self.construir_interfaz()
        self.cargar_contactos()

    def construir_interfaz(self):
        layout_principal = QVBoxLayout(self)

        titulo = QLabel("Gestión de contactos")
        titulo.setObjectName("titulo")

        descripcion = QLabel(
            "Agrega, consulta y modifica los contactos registrados."
        )
        descripcion.setObjectName("subtitulo")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descripcion)

        formulario = QFormLayout()

        self.campo_id = QLineEdit()
        self.campo_nombre = QLineEdit()
        self.campo_telefono = QLineEdit()
        self.campo_correo = QLineEdit()
        self.campo_ciudad = QLineEdit()

        self.campo_id.setPlaceholderText("Ej. 1001")
        self.campo_nombre.setPlaceholderText("Nombre completo")
        self.campo_telefono.setPlaceholderText("Número telefónico")
        self.campo_correo.setPlaceholderText("Correo electrónico")
        self.campo_ciudad.setPlaceholderText("Ciudad")

        formulario.addRow("ID:", self.campo_id)
        formulario.addRow("Nombre:", self.campo_nombre)
        formulario.addRow("Teléfono:", self.campo_telefono)
        formulario.addRow("Correo:", self.campo_correo)
        formulario.addRow("Ciudad:", self.campo_ciudad)

        layout_principal.addLayout(formulario)

        botones = QHBoxLayout()

        self.boton_agregar = QPushButton("Agregar")
        self.boton_buscar = QPushButton("Buscar por ID")
        self.boton_modificar = QPushButton("Modificar")
        self.boton_limpiar = QPushButton("Limpiar")

        botones.addWidget(self.boton_agregar)
        botones.addWidget(self.boton_buscar)
        botones.addWidget(self.boton_modificar)
        botones.addWidget(self.boton_limpiar)

        layout_principal.addLayout(botones)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Teléfono", "Correo", "Ciudad"
        ])

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout_principal.addWidget(self.tabla)

        self.boton_agregar.clicked.connect(self.agregar_contacto)
        self.boton_buscar.clicked.connect(self.buscar_contacto)
        self.boton_modificar.clicked.connect(self.modificar_contacto)
        self.boton_limpiar.clicked.connect(self.limpiar_formulario)
        self.tabla.cellClicked.connect(self.seleccionar_contacto)

    def obtener_datos_formulario(self):
        try:
            identificador = int(self.campo_id.text().strip())
        except ValueError:
            raise ValueError("El ID debe ser un número entero.")

        return Contacto(
            id=identificador,
            nombre=self.campo_nombre.text().strip(),
            telefono=self.campo_telefono.text().strip(),
            correo=self.campo_correo.text().strip(),
            ciudad=self.campo_ciudad.text().strip()
        )

    def agregar_contacto(self):
        try:
            contacto = self.obtener_datos_formulario()
            numero, inicio, final = self.servicio.agregar(contacto)

            QMessageBox.information(
                self,
                "Contacto agregado",
                f"Contacto guardado correctamente.\n"
                f"Registro: {numero}\n"
                f"Posición inicial: {inicio}\n"
                f"Posición final: {final}"
            )

            self.cargar_contactos()
            self.limpiar_formulario()

        except (ValueError, OSError) as error:
            QMessageBox.warning(self, "No se pudo agregar", str(error))

    def buscar_contacto(self):
        try:
            identificador = self.campo_id.text().strip()

            if not identificador:
                raise ValueError("Ingresa el ID que deseas buscar.")

            contacto, numero, posicion = self.servicio.buscar(
                identificador
            )

            self.mostrar_en_formulario(contacto)
            self.contacto_seleccionado = contacto.id

            QMessageBox.information(
                self,
                "Contacto encontrado",
                f"Contacto encontrado.\n"
                f"Número de registro: {numero}\n"
                f"Posición en el archivo: {posicion}"
            )

        except (ValueError, OSError) as error:
            QMessageBox.warning(self, "Búsqueda", str(error))

    def modificar_contacto(self):
        try:
            if self.contacto_seleccionado is None:
                raise ValueError(
                    "Primero busca un contacto o selecciónalo en la tabla."
                )

            contacto = self.obtener_datos_formulario()

            if contacto.id != self.contacto_seleccionado:
                raise ValueError("No puedes cambiar el ID del contacto.")

            numero, inicio, final = self.servicio.modificar(
                self.contacto_seleccionado,
                contacto
            )

            QMessageBox.information(
                self,
                "Contacto modificado",
                f"Contacto actualizado correctamente.\n"
                f"Registro: {numero}\n"
                f"Posición inicial: {inicio}\n"
                f"Posición final: {final}"
            )

            self.cargar_contactos()
            self.limpiar_formulario()

        except (ValueError, OSError) as error:
            QMessageBox.warning(self, "No se pudo modificar", str(error))

    def cargar_contactos(self):
        try:
            contactos = self.servicio.listar_contactos()
            self.tabla.setRowCount(len(contactos))

            for fila, contacto in enumerate(contactos):
                valores = [
                    contacto.id,
                    contacto.nombre,
                    contacto.telefono,
                    contacto.correo,
                    contacto.ciudad
                ]

                for columna, valor in enumerate(valores):
                    self.tabla.setItem(
                        fila,
                        columna,
                        QTableWidgetItem(str(valor))
                    )

        except (ValueError, OSError) as error:
            QMessageBox.warning(
                self,
                "Error al cargar contactos",
                str(error)
            )

    def seleccionar_contacto(self, fila, columna):
        elemento = self.tabla.item(fila, 0)

        if elemento is None:
            return

        try:
            contacto, numero, posicion = self.servicio.buscar(
                elemento.text()
            )
            self.mostrar_en_formulario(contacto)
            self.contacto_seleccionado = contacto.id

        except (ValueError, OSError) as error:
            QMessageBox.warning(self, "Error", str(error))

    def mostrar_en_formulario(self, contacto):
        self.campo_id.setText(str(contacto.id))
        self.campo_nombre.setText(contacto.nombre)
        self.campo_telefono.setText(contacto.telefono)
        self.campo_correo.setText(contacto.correo)
        self.campo_ciudad.setText(contacto.ciudad)

    def limpiar_formulario(self):
        self.campo_id.clear()
        self.campo_nombre.clear()
        self.campo_telefono.clear()
        self.campo_correo.clear()
        self.campo_ciudad.clear()
        self.contacto_seleccionado = None
        self.tabla.clearSelection()