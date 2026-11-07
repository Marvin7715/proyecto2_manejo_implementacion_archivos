import json
import os
from pathlib import Path


RUTA_PROYECTO = Path(__file__).resolve().parents[3]
CARPETA_DATOS = RUTA_PROYECTO / "data"
RUTA_INDICE = CARPETA_DATOS / "indice.json"


def cargar_indice():

    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)

    if not RUTA_INDICE.exists():
        guardar_indice({})
        return {}

    try:
        with open(RUTA_INDICE, "r", encoding="utf-8") as archivo:
            indice = json.load(archivo)

        if not isinstance(indice, dict):
            raise ValueError("La estructura del índice no es válida.")

        for identificador, registro in indice.items():
            if not identificador.isdigit():
                raise ValueError("El índice contiene un ID inválido.")

            if not isinstance(registro, int) or registro < 0:
                raise ValueError("El índice contiene una posición inválida.")

        return indice

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise ValueError(f"No se pudo cargar el índice: {error}")


def guardar_indice(indice):

    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)

    temporal = RUTA_INDICE.with_name("indice.tmp")

    try:
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(
                indice,
                archivo,
                ensure_ascii=False,
                indent=4
            )

            archivo.flush()
            os.fsync(archivo.fileno())

        os.replace(temporal, RUTA_INDICE)

    except OSError:
        if temporal.exists():
            temporal.unlink()

        raise


def buscar_posicion(identificador):

    indice = cargar_indice()

    return indice.get(str(identificador))


def agregar_al_indice(identificador, numero_registro):

    indice = cargar_indice()

    identificador = str(identificador)

    if identificador in indice:
        raise ValueError("Ya existe un contacto con ese ID.")

    indice[identificador] = numero_registro

    guardar_indice(indice)