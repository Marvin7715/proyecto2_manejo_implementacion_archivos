import os
from pathlib import Path
from datetime import datetime

RUTA_PROYECTO = Path(__file__).resolve().parents[3]

ARCHIVOS = [
    RUTA_PROYECTO / "data" / "contactos.dat",
    RUTA_PROYECTO / "data" / "indice.json",
    RUTA_PROYECTO / "data" / "contactos.sha256",
    RUTA_PROYECTO / "backups" / "respaldo_contactos.zip"
]


def consultar_metadatos():
    resultados = []

    for ruta in ARCHIVOS:
        if not ruta.exists():
            resultados.append({
                "nombre": ruta.name,
                "tamano": "No disponible",
                "modificacion": "No disponible",
                "lectura": "No disponible",
                "escritura": "No disponible",
                "estado": "No existe"
            })
            continue

        try:
            informacion = os.stat(ruta)

            fecha = datetime.fromtimestamp(
                informacion.st_mtime
            ).strftime("%d/%m/%Y %H:%M:%S")

            resultados.append({
                "nombre": ruta.name,
                "tamano": f"{informacion.st_size} bytes",
                "modificacion": fecha,
                "lectura": (
                    "Sí" if os.access(ruta, os.R_OK) else "No"
                ),
                "escritura": (
                    "Sí" if os.access(ruta, os.W_OK) else "No"
                ),
                "estado": "Disponible"
            })

        except OSError as error:
            resultados.append({
                "nombre": ruta.name,
                "tamano": "Error",
                "modificacion": "Error",
                "lectura": "Error",
                "escritura": "Error",
                "estado": str(error)
            })

    return resultados