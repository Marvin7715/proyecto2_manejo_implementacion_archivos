import json
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

RUTA_PROYECTO = Path(__file__).resolve().parents[3]
RUTA_JSON = RUTA_PROYECTO / "exports" / "contactos.json"
CARPETA_EXPORTACIONES = RUTA_PROYECTO / "exports"
RUTA_PDF = CARPETA_EXPORTACIONES / "reporte_contactos.pdf"


def generar_reporte_pdf():
    if not RUTA_JSON.exists():
        raise FileNotFoundError(
            "Primero debes generar el archivo contactos.json."
        )

    with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
        contactos = json.load(archivo)

    if not isinstance(contactos, list):
        raise ValueError("El formato del archivo JSON no es válido.")

    CARPETA_EXPORTACIONES.mkdir(parents=True, exist_ok=True)

    documento = SimpleDocTemplate(
        str(RUTA_PDF),
        pagesize=landscape(letter),
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloReporte",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        fontSize=19,
        spaceAfter=12
    )

    elementos = []

    elementos.append(
        Paragraph("REPORTE DE CONTACTOS", titulo)
    )

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    elementos.append(
        Paragraph(f"Fecha de generación: {fecha}", estilos["Normal"])
    )

    elementos.append(Spacer(1, 20))

    datos_tabla = [
        ["ID", "Nombre", "Teléfono", "Correo", "Ciudad"]
    ]

    for contacto in contactos:
        if not isinstance(contacto, dict):
            raise ValueError("Un contacto del JSON no tiene formato válido.")

        datos_tabla.append([
            str(contacto.get("id", "")),
            str(contacto.get("nombre", "")),
            str(contacto.get("telefono", "")),
            str(contacto.get("correo", "")),
            str(contacto.get("ciudad", ""))
        ])

    tabla = Table(
        datos_tabla,
        colWidths=[55, 125, 90, 210, 110],
        repeatRows=1
    )

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#315A91")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5DCE5")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#F1F4F8")
        ]),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 15))
    elementos.append(
        Paragraph(
            f"Total de contactos registrados: {len(contactos)}",
            estilos["Normal"]
        )
    )

    documento.build(elementos)

    return RUTA_PDF