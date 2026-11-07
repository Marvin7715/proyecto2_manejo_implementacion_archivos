from pathlib import Path

from agenda_contactos.contactos.modelo import Contacto


RUTA_PROYECTO = Path(__file__).resolve().parents[3]
CARPETA_DATOS = RUTA_PROYECTO / "data"
RUTA_CONTACTOS = CARPETA_DATOS / "contactos.dat"

LONGITUDES = {
    "id": 6,
    "nombre": 40,
    "telefono": 15,
    "correo": 45,
    "ciudad": 30
}

TAMANO_REGISTRO = sum(LONGITUDES.values())


def ajustar_campo(valor, longitud):
    resultado = ""

    for caracter in str(valor):
        candidato = resultado + caracter

        if len(candidato.encode("utf-8")) > longitud:
            break

        resultado = candidato

    contenido = resultado.encode("utf-8")
    return contenido.ljust(longitud, b" ")


def crear_registro(contacto):

    identificador = str(contacto.id).zfill(6)

    campos = [
        ajustar_campo(identificador, LONGITUDES["id"]),
        ajustar_campo(contacto.nombre, LONGITUDES["nombre"]),
        ajustar_campo(contacto.telefono, LONGITUDES["telefono"]),
        ajustar_campo(contacto.correo, LONGITUDES["correo"]),
        ajustar_campo(contacto.ciudad, LONGITUDES["ciudad"])
    ]

    return b"".join(campos)


def decodificar_registro(datos):

    if len(datos) != TAMANO_REGISTRO:
        raise ValueError("El registro está incompleto o dañado.")

    posiciones = {}
    inicio = 0

    for campo, longitud in LONGITUDES.items():
        fin = inicio + longitud
        posiciones[campo] = datos[inicio:fin].decode("utf-8").strip()
        inicio = fin

    return Contacto(
        id=int(posiciones["id"]),
        nombre=posiciones["nombre"],
        telefono=posiciones["telefono"],
        correo=posiciones["correo"],
        ciudad=posiciones["ciudad"]
    )


def agregar_registro(contacto):

    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)

    with open(RUTA_CONTACTOS, "a+b") as archivo:
        archivo.seek(0, 2)

        posicion = archivo.tell()

        if posicion % TAMANO_REGISTRO != 0:
            raise ValueError("El archivo contiene registros incompletos.")

        numero_registro = posicion // TAMANO_REGISTRO

        archivo.write(crear_registro(contacto))
        archivo.flush()

        posicion_final = archivo.tell()

    return numero_registro, posicion, posicion_final


def leer_registro(numero_registro):

    if not RUTA_CONTACTOS.exists():
        raise FileNotFoundError("Todavía no existe el archivo de contactos.")

    if numero_registro < 0:
        raise ValueError("El número de registro no es válido.")

    with open(RUTA_CONTACTOS, "rb") as archivo:

        posicion = numero_registro * TAMANO_REGISTRO

        archivo.seek(posicion)
        posicion_actual = archivo.tell()

        datos = archivo.read(TAMANO_REGISTRO)

        if len(datos) != TAMANO_REGISTRO:
            raise ValueError("No se encontró un registro completo.")

        contacto = decodificar_registro(datos)

    return contacto, posicion_actual


def modificar_registro(numero_registro, contacto):

    if not RUTA_CONTACTOS.exists():
        raise FileNotFoundError("No existe el archivo de contactos.")

    if numero_registro < 0:
        raise ValueError("El número de registro no es válido.")

    with open(RUTA_CONTACTOS, "r+b") as archivo:

        posicion = numero_registro * TAMANO_REGISTRO

        archivo.seek(posicion)

        if archivo.tell() != posicion:
            raise ValueError("No se pudo ubicar el registro.")

        archivo.write(crear_registro(contacto))
        archivo.flush()

        posicion_final = archivo.tell()

    return posicion, posicion_final