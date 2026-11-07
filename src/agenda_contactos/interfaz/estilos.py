COLORES = {
    "fondo": "#F4F6FA",
    "sidebar": "#17243A",
    "sidebar_hover": "#263852",
    "sidebar_activo": "#315A91",
    "blanco": "#FFFFFF",
    "texto": "#243247",
    "texto_secundario": "#7B8798",
    "borde": "#E3E8EF",
    "azul": "#3976C6",
    "verde": "#299D78",
    "naranja": "#E69A42",
}


ESTILO_GENERAL = f"""
QMainWindow {{
    background-color: {COLORES["fondo"]};
}}

QWidget {{
    font-family: 'Segoe UI';
    color: {COLORES["texto"]};
}}

QLabel#titulo {{
    font-size: 25px;
    font-weight: 700;
}}

QLabel#subtitulo {{
    font-size: 13px;
    color: {COLORES["texto_secundario"]};
}}

QFrame#sidebar {{
    background-color: {COLORES["sidebar"]};
    border: none;
}}

QLabel#logo {{
    color: white;
    font-size: 21px;
    font-weight: 700;
}}

QLabel#logo_subtitulo {{
    color: #AAB8CB;
    font-size: 11px;
}}

QPushButton#menu_boton {{
    background-color: transparent;
    color: #D5DEEA;
    border: none;
    text-align: left;
    padding: 13px 17px;
    border-radius: 7px;
    font-size: 14px;
}}

QPushButton#menu_boton:hover {{
    background-color: {COLORES["sidebar_hover"]};
    color: white;
}}

QPushButton#menu_boton[activo="true"] {{
    background-color: {COLORES["sidebar_activo"]};
    color: white;
    font-weight: 600;
}}

QFrame#tarjeta {{
    background-color: white;
    border: 1px solid {COLORES["borde"]};
    border-radius: 12px;
}}

QLabel#tarjeta_titulo {{
    color: {COLORES["texto_secundario"]};
    font-size: 12px;
}}

QLabel#tarjeta_valor {{
    color: {COLORES["texto"]};
    font-size: 25px;
    font-weight: 700;
}}

QFrame#panel_contenido {{
    background-color: white;
    border: 1px solid {COLORES["borde"]};
    border-radius: 12px;
}}

QLabel#seccion_titulo {{
    font-size: 17px;
    font-weight: 600;
}}

QLabel#seccion_descripcion {{
    color: {COLORES["texto_secundario"]};
    font-size: 12px;
}}
"""