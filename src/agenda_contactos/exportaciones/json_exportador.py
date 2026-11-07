import json
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parents[3]
CARPETA_EXPORTACIONES = RUTA_PROYECTO / "exports"
RUTA_JSON = CARPETA_EXPORTACIONES / "contactos.json"


def exportar_contactos_json(contactos):
    CARPETA_EXPORTACIONES.mkdir(parents=True, exist_ok=True)

    datos = []

    for contacto in contactos:
        datos.append({
            "id": contacto.id,
            "nombre": contacto.nombre,
            "telefono": contacto.telefono,
            "correo": contacto.correo,
            "ciudad": contacto.ciudad
        })

    with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    return RUTA_JSON