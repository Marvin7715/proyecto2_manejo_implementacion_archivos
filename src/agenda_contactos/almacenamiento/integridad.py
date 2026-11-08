import hashlib
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parents[3]
CARPETA_DATOS = RUTA_PROYECTO / "data"
RUTA_CONTACTOS = CARPETA_DATOS / "contactos.dat"
RUTA_HASH = CARPETA_DATOS / "contactos.sha256"


def calcular_hash():
    sha256 = hashlib.sha256()

    with open(RUTA_CONTACTOS, "rb") as archivo:
        while True:
            bloque = archivo.read(4096)

            if not bloque:
                break

            sha256.update(bloque)

    return sha256.hexdigest()


def guardar_hash():
    if not RUTA_CONTACTOS.exists():
        raise FileNotFoundError(
            "No existe el archivo de contactos para calcular su hash."
        )

    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)

    resultado = calcular_hash()

    with open(RUTA_HASH, "w", encoding="utf-8") as archivo:
        archivo.write(resultado)

    return resultado


def verificar_integridad():
    if not RUTA_CONTACTOS.exists():
        return "sin_archivo", "Todavía no existe el archivo de contactos."

    if not RUTA_HASH.exists():
        guardar_hash()
        return (
            "nuevo",
            "Se creó el registro inicial de integridad SHA-256."
        )

    hash_actual = calcular_hash()

    with open(RUTA_HASH, "r", encoding="utf-8") as archivo:
        hash_guardado = archivo.read().strip()

    if hash_actual == hash_guardado:
        return "correcto", "La integridad del archivo es correcta."

    return (
        "alterado",
        "ADVERTENCIA: el archivo contactos.dat fue modificado "
        "o presenta diferencias respecto al hash guardado."
    )