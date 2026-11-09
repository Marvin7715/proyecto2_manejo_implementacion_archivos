import zipfile
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parents[3]

CARPETA_DATOS = RUTA_PROYECTO / "data"
CARPETA_RESPALDOS = RUTA_PROYECTO / "backups"

ARCHIVOS_RESPALDO = [
    CARPETA_DATOS / "contactos.dat",
    CARPETA_DATOS / "indice.json"
]

RUTA_ZIP = CARPETA_RESPALDOS / "respaldo_contactos.zip"


def crear_respaldo():
    for ruta in ARCHIVOS_RESPALDO:
        if not ruta.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo necesario: {ruta.name}"
            )

    CARPETA_RESPALDOS.mkdir(parents=True, exist_ok=True)

    tamano_original = sum(
        ruta.stat().st_size for ruta in ARCHIVOS_RESPALDO
    )

    with zipfile.ZipFile(
        RUTA_ZIP,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as respaldo:

        for ruta in ARCHIVOS_RESPALDO:
            respaldo.write(ruta, arcname=ruta.name)

    tamano_comprimido = RUTA_ZIP.stat().st_size

    return {
        "ruta": RUTA_ZIP,
        "tamano_original": tamano_original,
        "tamano_comprimido": tamano_comprimido
    }