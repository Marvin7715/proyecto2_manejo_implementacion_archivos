from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QSizePolicy,
    QFrame
)

from agenda_contactos.contactos.modelo import Contacto
from agenda_contactos.contactos.servicio import ServicioContactos


class VentanaContactos(QWidget):
    contactos_actualizados = Signal()

    def __init__(self):
        super().__init__()

        self.servicio = ServicioContactos()
        self.contacto_seleccionado = None

        self.construir_interfaz()
        self.cargar_contactos()

    def construir_interfaz(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 5, 0, 0)
        layout_principal.setSpacing(14)

        panel_formulario = QFrame()
        panel_formulario.setObjectName("panel_contenido")

        layout_formulario = QVBoxLayout(panel_formulario)
        layout_formulario.setContentsMargins(20, 17, 20, 17)
        layout_formulario.setSpacing(12)

        titulo_formulario = QLabel("Información del contacto")
        titulo_formulario.setObjectName("seccion_titulo")

        descripcion = QLabel(
            "Completa los campos para registrar, buscar o actualizar un contacto."
        )
        descripcion.setObjectName("seccion_descripcion")

        layout_formulario.addWidget(titulo_formulario)
        layout_formulario.addWidget(descripcion)

        campos = QGridLayout()
        campos.setHorizontalSpacing(16)
        campos.setVerticalSpacing(9)
        campos.setColumnStretch(1, 1)
        campos.setColumnStretch(3, 2)

        self.campo_id = self.crear_campo("Ej. 1001")
        self.campo_nombre = self.crear_campo("Nombre completo")
        self.campo_telefono = self.crear_campo("Número telefónico")
        self.campo_correo = self.crear_campo("Correo electrónico")
        self.campo_ciudad = self.crear_campo("Ciudad")

        self.campo_id.setValidator(QIntValidator(1, 999999, self))

        self.agregar_campo(campos, 0, 0, "ID", self.campo_id)
        self.agregar_campo(campos, 0, 2, "Nombre", self.campo_nombre)
        self.agregar_campo(campos, 1, 0, "Teléfono", self.campo_telefono)
        self.agregar_campo(campos, 1, 2, "Correo", self.campo_correo)
        self.agregar_campo(campos, 2, 0, "Ciudad", self.campo_ciudad, ancho_completo=True)

        layout_formulario.addLayout(campos)

        botones = QHBoxLayout()
        botones.setSpacing(9)

        self.boton_agregar = QPushButton("Registrar contacto")
        self.boton_agregar.setObjectName("boton_primario")

        self.boton_buscar = QPushButton("Buscar por ID")
        self.boton_buscar.setObjectName("boton_secundario")

        self.boton_modificar = QPushButton("Guardar cambios")
        self.boton_modificar.setObjectName("boton_exito")

        self.boton_limpiar = QPushButton("Limpiar formulario")

        botones.addWidget(self.boton_agregar)
        botones.addWidget(self.boton_buscar)
        botones.addWidget(self.boton_modificar)
        botones.addWidget(self.boton_limpiar)
        botones.addStretch()

        layout_formulario.addLayout(botones)

        self.estado = QLabel("Selecciona una acción para comenzar.")
        self.estado.setObjectName("estado")
        self.estado.setWordWrap(True)
        layout_formulario.addWidget(self.estado)

        panel_tabla = QFrame()
        panel_tabla.setObjectName("panel_contenido")

        layout_tabla = QVBoxLayout(panel_tabla)
        layout_tabla.setContentsMargins(18, 15, 18, 15)
        layout_tabla.setSpacing(10)

        encabezado_tabla = QHBoxLayout()

        titulo_tabla = QLabel("Contactos registrados")
        titulo_tabla.setObjectName("seccion_titulo")

        self.total_contactos = QLabel("0 contactos")
        self.total_contactos.setObjectName("texto_secundario")

        encabezado_tabla.addWidget(titulo_tabla)
        encabezado_tabla.addStretch()
        encabezado_tabla.addWidget(self.total_contactos)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Teléfono", "Correo electrónico", "Ciudad"
        ])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setShowGrid(True)
        self.tabla.setWordWrap(False)
        self.tabla.setMinimumHeight(220)
        self.tabla.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.verticalHeader().setDefaultSectionSize(38)
        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.tabla.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout_tabla.addLayout(encabezado_tabla)
        layout_tabla.addWidget(self.tabla)

        layout_principal.addWidget(panel_formulario)
        layout_principal.addWidget(panel_tabla, 1)

        self.boton_agregar.clicked.connect(self.agregar_contacto)
        self.boton_buscar.clicked.connect(self.buscar_contacto)
        self.boton_modificar.clicked.connect(self.modificar_contacto)
        self.boton_limpiar.clicked.connect(self.limpiar_formulario)
        self.tabla.cellClicked.connect(self.seleccionar_contacto)

    def crear_campo(self, placeholder):
        campo = QLineEdit()
        campo.setPlaceholderText(placeholder)
        campo.setMinimumHeight(38)
        return campo

    def agregar_campo(self, layout, fila, columna, nombre, campo, ancho_completo=False):
        etiqueta = QLabel(nombre)
        etiqueta.setObjectName("etiqueta_campo")

        layout.addWidget(etiqueta, fila, columna)

        if ancho_completo:
            layout.addWidget(campo, fila, columna + 1, 1, 3)
        else:
            layout.addWidget(campo, fila, columna + 1)

    def obtener_datos_formulario(self):
        try:
            identificador = int(self.campo_id.text().strip())
        except ValueError:
            raise ValueError("El ID debe ser un número entero entre 1 y 999999.")

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

            self.cargar_contactos()
            self.limpiar_formulario()
            self.estado.setText(
                f"Contacto registrado. Registro: {numero} | "
                f"Posición inicial: {inicio} bytes | "
                f"Posición final: {final} bytes."
            )
            self.contactos_actualizados.emit()

        except (ValueError, OSError) as error:
            QMessageBox.warning(self, "No se pudo registrar", str(error))

    def buscar_contacto(self):
        try:
            identificador = self.campo_id.text().strip()

            if not identificador:
                raise ValueError("Ingresa el ID del contacto que deseas buscar.")

            contacto, numero, posicion = self.servicio.buscar(identificador)

            self.mostrar_en_formulario(contacto)
            self.contacto_seleccionado = contacto.id
            self.estado.setText(
                f"Contacto encontrado en el registro {numero}, "
                f"posición {posicion} del archivo."
            )

        except (ValueError, OSError) as error:
            QMessageBox.warning(self, "Búsqueda de contacto", str(error))

    def modificar_contacto(self):
        try:
            if self.contacto_seleccionado is None:
                raise ValueError(
                    "Busca un contacto o selecciónalo en la tabla antes de modificarlo."
                )

            contacto = self.obtener_datos_formulario()

            if contacto.id != self.contacto_seleccionado:
                raise ValueError("El ID de un contacto existente no se puede cambiar.")

            numero, inicio, final = self.servicio.modificar(
                self.contacto_seleccionado,
                contacto
            )

            self.cargar_contactos()
            self.limpiar_formulario()
            self.estado.setText(
                f"Contacto actualizado en el registro {numero}. "
                f"Posición inicial: {inicio} bytes | "
                f"Posición final: {final} bytes."
            )
            self.contactos_actualizados.emit()

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
                    contacto.ciudad,
                ]

                for columna, valor in enumerate(valores):
                    elemento = QTableWidgetItem(str(valor))
                    if columna == 0:
                        elemento.setTextAlignment(
                            Qt.AlignmentFlag.AlignCenter
                        )
                    self.tabla.setItem(fila, columna, elemento)

            cantidad = len(contactos)
            self.total_contactos.setText(
                f"{cantidad} contacto" if cantidad == 1
                else f"{cantidad} contactos"
            )

        except (ValueError, OSError) as error:
            self.tabla.setRowCount(0)
            self.total_contactos.setText("No disponible")
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
            contacto, numero, posicion = self.servicio.buscar(elemento.text())
            self.mostrar_en_formulario(contacto)
            self.contacto_seleccionado = contacto.id
            self.estado.setText(
                f"Contacto seleccionado: {contacto.nombre}. "
                "Puedes modificar sus datos y guardar los cambios."
            )

        except (ValueError, OSError) as error:
            QMessageBox.warning(self, "Error de selección", str(error))

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
        self.estado.setText("Formulario limpio. Puedes ingresar otro contacto.")