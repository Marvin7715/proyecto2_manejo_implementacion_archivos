from agenda_contactos.contactos.modelo import Contacto
from agenda_contactos.almacenamiento.integridad import guardar_hash
from agenda_contactos.almacenamiento.registros import (
    LONGITUDES,
    agregar_registro,
    leer_registro,
    modificar_registro
)
from agenda_contactos.almacenamiento.indice import (
    cargar_indice,
    buscar_posicion,
    agregar_al_indice,
    guardar_indice
)


class ServicioContactos:

    def validar_contacto(self, contacto):

        if contacto.id <= 0 or contacto.id > 999999:
            raise ValueError("El ID debe estar entre 1 y 999999.")

        campos = {
            "nombre": contacto.nombre,
            "telefono": contacto.telefono,
            "correo": contacto.correo,
            "ciudad": contacto.ciudad
        }

        for campo, valor in campos.items():

            if not valor.strip():
                raise ValueError(f"El campo {campo} es obligatorio.")

            longitud = len(valor.encode("utf-8"))

            if longitud > LONGITUDES[campo]:
                raise ValueError(
                    f"El campo {campo} supera su límite de "
                    f"{LONGITUDES[campo]} bytes."
                )

    def agregar(self, contacto):

        self.validar_contacto(contacto)

        if buscar_posicion(contacto.id) is not None:
            raise ValueError("Ya existe un contacto con ese ID.")

        numero, posicion, posicion_final = agregar_registro(contacto)

        agregar_al_indice(contacto.id, numero)
        guardar_hash()
        return numero, posicion, posicion_final

    def buscar(self, identificador):

        numero_registro = buscar_posicion(identificador)

        if numero_registro is None:
            raise ValueError("No existe un contacto con ese ID.")

        contacto, posicion = leer_registro(numero_registro)

        if contacto.id != int(identificador):
            raise ValueError(
                "El índice no coincide con el registro almacenado."
            )

        return contacto, numero_registro, posicion

    def modificar(self, identificador, nuevos_datos):

        self.validar_contacto(nuevos_datos)

        if int(identificador) != nuevos_datos.id:
            raise ValueError("No se permite cambiar el ID del contacto.")

        numero_registro = buscar_posicion(identificador)

        if numero_registro is None:
            raise ValueError("No existe el contacto que desea modificar.")

        posicion, posicion_final = modificar_registro(
            numero_registro, nuevos_datos
        )
        guardar_hash()
        return numero_registro, posicion, posicion_final

    def listar_contactos(self):
        indice = cargar_indice()
        contactos = []

        for identificador, numero_registro in indice.items():
            contacto, posicion = leer_registro(numero_registro)

            if contacto.id != int(identificador):
                raise ValueError(
                    "El índice no coincide con el registro almacenado."
                )

            contactos.append(contacto)

        return sorted(contactos, key=lambda contacto: contacto.id)