TEMAS = {
    "claro": {
        "fondo": "#F3F6FB",
        "superficie": "#FFFFFF",
        "superficie_alt": "#F8FAFD",
        "sidebar": "#17243A",
        "sidebar_hover": "#263852",
        "sidebar_activo": "#315A91",
        "texto": "#243247",
        "texto_secundario": "#68778C",
        "borde": "#DCE4EF",
        "entrada": "#FFFFFF",
        "texto_entrada": "#243247",
        "tabla_alterna": "#F4F7FB",
        "seleccion": "#DCEBFA",
        "primario": "#3976C6",
        "primario_hover": "#2D64AC",
        "exito": "#23865D",
        "exito_hover": "#1B704D",
        "advertencia": "#B7791F",
        "advertencia_hover": "#946116",
        "peligro": "#C24141",
        "peligro_hover": "#A83232",
        "borde_foco": "#6B9DE0",
        "texto_sidebar": "#D5DEEA",
        "texto_sidebar_secundario": "#AAB8CB",
    },
    "oscuro": {
        "fondo": "#111827",
        "superficie": "#1F2937",
        "superficie_alt": "#273449",
        "sidebar": "#0B1220",
        "sidebar_hover": "#1E2B40",
        "sidebar_activo": "#315A91",
        "texto": "#E5EAF2",
        "texto_secundario": "#A6B3C5",
        "borde": "#39485D",
        "entrada": "#182334",
        "texto_entrada": "#F1F5F9",
        "tabla_alterna": "#243247",
        "seleccion": "#29496B",
        "primario": "#3B82F6",
        "primario_hover": "#2563EB",
        "exito": "#16845B",
        "exito_hover": "#116C49",
        "advertencia": "#B7791F",
        "advertencia_hover": "#946116",
        "peligro": "#C24141",
        "peligro_hover": "#A83232",
        "borde_foco": "#60A5FA",
        "texto_sidebar": "#E2E8F0",
        "texto_sidebar_secundario": "#9FB0C7",
    },
}

COLORES = TEMAS["claro"]


def obtener_estilo(nombre_tema="claro"):
    c = TEMAS.get(nombre_tema, TEMAS["claro"])

    return f"""
    * {{
        font-family: "Segoe UI";
        font-size: 13px;
    }}

    QMainWindow, QWidget#contenido_principal, QWidget#pagina {{
        background-color: {c["fondo"]};
        color: {c["texto"]};
    }}

    QWidget {{
        color: {c["texto"]};
    }}

    QLabel {{
        background: transparent;
        color: {c["texto"]};
    }}

    QLabel#titulo {{
        font-size: 25px;
        font-weight: 700;
        color: {c["texto"]};
    }}

    QLabel#subtitulo {{
        font-size: 13px;
        color: {c["texto_secundario"]};
    }}

    QLabel#seccion_titulo {{
        font-size: 18px;
        font-weight: 700;
        color: {c["texto"]};
    }}

    QLabel#seccion_descripcion, QLabel#texto_secundario {{
        font-size: 12px;
        color: {c["texto_secundario"]};
    }}

    QLabel#logo {{
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 1px;
    }}

    QLabel#logo_subtitulo {{
        color: {c["texto_sidebar_secundario"]};
        font-size: 10px;
        letter-spacing: 1px;
    }}

    QLabel#tarjeta_titulo {{
        color: {c["texto_secundario"]};
        font-size: 12px;
        font-weight: 600;
    }}

    QLabel#tarjeta_valor {{
        color: {c["texto"]};
        font-size: 25px;
        font-weight: 700;
    }}

    QLabel#estado {{
        color: {c["texto_secundario"]};
        background-color: {c["superficie_alt"]};
        border: 1px solid {c["borde"]};
        border-radius: 8px;
        padding: 10px 12px;
    }}

    QLabel#etiqueta_campo {{
        color: {c["texto_secundario"]};
        font-size: 12px;
        font-weight: 600;
    }}

    QFrame#sidebar {{
        background-color: {c["sidebar"]};
        border: none;
    }}

    QFrame#tarjeta, QFrame#panel_contenido {{
        background-color: {c["superficie"]};
        border: 1px solid {c["borde"]};
        border-radius: 12px;
    }}

    QFrame#tarjeta_resumen {{
        background-color: {c["superficie"]};
        border: 1px solid {c["borde"]};
        border-radius: 12px;
    }}

    QFrame#separador {{
        background-color: {c["borde"]};
        border: none;
        max-height: 1px;
    }}

    QPushButton {{
        background-color: {c["superficie_alt"]};
        color: {c["texto"]};
        border: 1px solid {c["borde"]};
        border-radius: 8px;
        padding: 10px 16px;
        min-height: 18px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        border-color: {c["primario"]};
        background-color: {c["seleccion"]};
    }}

    QPushButton:pressed {{
        padding-top: 11px;
        padding-bottom: 9px;
    }}

    QPushButton:disabled {{
        color: {c["texto_secundario"]};
        background-color: {c["superficie_alt"]};
        border-color: {c["borde"]};
    }}

    QPushButton#menu_boton {{
        background-color: transparent;
        color: {c["texto_sidebar"]};
        border: none;
        text-align: left;
        padding: 12px 15px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 500;
    }}

    QPushButton#menu_boton:hover {{
        background-color: {c["sidebar_hover"]};
        color: #FFFFFF;
    }}

    QPushButton#menu_boton[activo="true"] {{
        background-color: {c["sidebar_activo"]};
        color: #FFFFFF;
        font-weight: 700;
    }}

    QPushButton#boton_tema {{
        background-color: {c["sidebar_hover"]};
        color: #FFFFFF;
        border: 1px solid #42536B;
        text-align: left;
        padding: 10px 13px;
    }}

    QPushButton#boton_tema:hover {{
        background-color: {c["sidebar_activo"]};
    }}

    QPushButton#boton_primario {{
        background-color: {c["primario"]};
        color: #FFFFFF;
        border: 1px solid {c["primario"]};
    }}

    QPushButton#boton_primario:hover {{
        background-color: {c["primario_hover"]};
        border-color: {c["primario_hover"]};
        color: #FFFFFF;
    }}

    QPushButton#boton_exito {{
        background-color: {c["exito"]};
        color: #FFFFFF;
        border: 1px solid {c["exito"]};
    }}

    QPushButton#boton_exito:hover {{
        background-color: {c["exito_hover"]};
        color: #FFFFFF;
    }}

    QPushButton#boton_advertencia {{
        background-color: {c["advertencia"]};
        color: #FFFFFF;
        border: 1px solid {c["advertencia"]};
    }}

    QPushButton#boton_advertencia:hover {{
        background-color: {c["advertencia_hover"]};
        color: #FFFFFF;
    }}

    QPushButton#boton_peligro {{
        background-color: {c["peligro"]};
        color: #FFFFFF;
        border: 1px solid {c["peligro"]};
    }}

    QPushButton#boton_peligro:hover {{
        background-color: {c["peligro_hover"]};
        color: #FFFFFF;
    }}

    QLineEdit {{
        background-color: {c["entrada"]};
        color: {c["texto_entrada"]};
        border: 1px solid {c["borde"]};
        border-radius: 7px;
        padding: 10px 11px;
        min-height: 20px;
        selection-background-color: {c["primario"]};
        selection-color: #FFFFFF;
    }}

    QLineEdit:focus {{
        border: 1px solid {c["borde_foco"]};
    }}

    QLineEdit:disabled {{
        color: {c["texto_secundario"]};
        background-color: {c["superficie_alt"]};
    }}

    QTableWidget {{
        background-color: {c["superficie"]};
        alternate-background-color: {c["tabla_alterna"]};
        color: {c["texto"]};
        border: 1px solid {c["borde"]};
        border-radius: 8px;
        gridline-color: {c["borde"]};
        selection-background-color: {c["seleccion"]};
        selection-color: {c["texto"]};
        outline: 0;
    }}

    QTableWidget::item {{
        padding: 8px 6px;
        border: none;
        color: {c["texto"]};
    }}

    QTableWidget::item:selected {{
        background-color: {c["seleccion"]};
        color: {c["texto"]};
    }}

    QHeaderView::section {{
        background-color: {c["superficie_alt"]};
        color: {c["texto"]};
        border: none;
        border-bottom: 1px solid {c["borde"]};
        padding: 11px 7px;
        font-weight: 700;
    }}

    QTableCornerButton::section {{
        background-color: {c["superficie_alt"]};
        border: none;
    }}

    QScrollBar:vertical {{
        background-color: {c["superficie_alt"]};
        width: 11px;
        margin: 2px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background-color: {c["borde"]};
        min-height: 25px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {c["texto_secundario"]};
    }}

    QScrollBar:horizontal {{
        background-color: {c["superficie_alt"]};
        height: 11px;
        margin: 2px;
        border-radius: 5px;
    }}

    QScrollBar::handle:horizontal {{
        background-color: {c["borde"]};
        min-width: 25px;
        border-radius: 5px;
    }}

    QGroupBox {{
        background-color: {c["superficie"]};
        border: 1px solid {c["borde"]};
        border-radius: 10px;
        margin-top: 12px;
        padding: 15px 12px 12px 12px;
        font-weight: 700;
        color: {c["texto"]};
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 5px;
        color: {c["texto"]};
    }}

    QToolTip {{
        background-color: {c["sidebar"]};
        color: #FFFFFF;
        border: 1px solid {c["sidebar_hover"]};
        padding: 5px;
    }}

    QMessageBox {{
        background-color: {c["superficie"]};
        color: {c["texto"]};
    }}
    """