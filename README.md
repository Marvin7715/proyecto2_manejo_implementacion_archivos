# Agenda de Contactos

## 1. Descripción del proyecto

Agenda de Contactos es una aplicación de escritorio desarrollada en Python que permite administrar información de contactos mediante archivos de acceso directo y registros de longitud fija.

El sistema utiliza un índice principal en formato JSON para localizar los registros de manera eficiente y ofrece herramientas para exportar información, verificar la integridad de los archivos y generar respaldos.

La interfaz gráfica está desarrollada con PySide6 y cuenta con temas visuales claro y oscuro.

## 2. Tecnologías utilizadas

- **Python 3.14:** lenguaje de programación.
- **PySide6:** desarrollo de la interfaz gráfica.
- **JSON:** administración del índice y exportación de información.
- **ReportLab:** generación de reportes PDF.
- **SHA-256:** verificación de integridad de los archivos.
- **ZIP:** compresión y respaldo de información.
- **Git y GitHub:** control de versiones y almacenamiento del código fuente.

## 3. Funcionalidades principales

### Gestión de contactos
- Registro y consulta de contactos.
- Modificación de información almacenada.
- Identificación única mediante un ID numérico.
- Validación de los datos ingresados.

### Administración de archivos
- Almacenamiento mediante registros de longitud fija.
- Acceso directo a los registros utilizando `seek()` y `tell()`.
- Modificación de registros sin reconstruir todo el archivo.
- Administración de un índice principal en formato JSON.

### Exportaciones
- Exportación de contactos a formato JSON.
- Generación de reportes PDF a partir de los datos exportados.
- Inclusión de la fecha de generación del reporte.

### Integridad y seguridad de archivos
- Generación de códigos hash mediante SHA-256.
- Verificación de modificaciones externas en el archivo de contactos.
- Creación de respaldos ZIP.
- Comparación del tamaño original y comprimido.
- Consulta de metadatos de archivos, incluyendo tamaño, fecha de modificación y permisos de lectura y escritura.

### Interfaz gráfica
- Navegación mediante ventanas y módulos.
- Tema claro y tema oscuro.
- Visualización de información y herramientas desde la aplicación.

## 4. Estructura del proyecto

```text
proyecto2_manejo_implementacion_archivos/
│
├── src/
│   └── agenda_contactos/
│       ├── almacenamiento/
│       │   ├── registros.py
│       │   ├── indice.py
│       │   ├── integridad.py
│       │   └── __init__.py
│       │
│       ├── contactos/
│       │   ├── modelo.py
│       │   ├── servicio.py
│       │   └── __init__.py
│       │
│       ├── exportaciones/
│       │   ├── json_exportador.py
│       │   ├── pdf_exportador.py
│       │   └── __init__.py
│       │
│       ├── herramientas/
│       │   ├── metadatos.py
│       │   ├── respaldos.py
│       │   └── __init__.py
│       │
│       ├── interfaz/
│       │   ├── estilos.py
│       │   ├── ventana_contactos.py
│       │   ├── ventana_exportar.py
│       │   ├── ventana_herramientas.py
│       │   ├── ventana_principal.py
│       │   └── __init__.py
│       │
│       └── __init__.py
│
├── data/
│   ├── contactos.dat
│   ├── indice.json
│   └── contactos.sha256
│
├── exports/
│   ├── contactos.json
│   └── reporte_contactos.pdf
│
├── backups/
│   └── respaldo_contactos.zip
│
├── docs/
├── tests/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 5. Requisitos del sistema

- Sistema operativo Windows.
- Python 3.14.
- PySide6.
- ReportLab.
- Git (opcional, para clonar el repositorio).

## 6. Instalación

### Clonar el repositorio

```bash
git clone https://github.com/Marvin7715/proyecto2_manejo_implementacion_archivos.git
```

Ingresar a la carpeta:

```bash
cd proyecto2_manejo_implementacion_archivos
```

### Crear un entorno virtual

```bash
python -m venv .venv
```

### Activar el entorno virtual

En PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Instalar las dependencias

```bash
pip install -r requirements.txt
```

## 7. Ejecución del sistema

Desde la carpeta principal del proyecto y con el entorno virtual activado, ejecutar:

```bash
python main.py
```

Se abrirá la aplicación de escritorio Agenda de Contactos.

## 8. Archivos generados

El sistema utiliza las siguientes carpetas para organizar la información:

| Carpeta | Contenido |
|---|---|
| `data/` | Archivo de contactos, índice JSON y hash SHA-256. |
| `exports/` | Exportaciones JSON y reportes PDF. |
| `backups/` | Respaldos comprimidos en formato ZIP. |
| `docs/` | Documentación del proyecto. |
| `tests/` | Espacio destinado a pruebas del sistema. |

## 9. Organización del código

El proyecto utiliza una estructura modular que separa las responsabilidades de cada componente:

- **almacenamiento:** administra los registros, el índice y la integridad de los archivos.
- **contactos:** contiene el modelo y los servicios para gestionar la información.
- **exportaciones:** genera archivos JSON y reportes PDF.
- **herramientas:** administra los respaldos ZIP y la consulta de metadatos.
- **interfaz:** contiene las ventanas y los estilos visuales de la aplicación.

Esta organización facilita el mantenimiento, la comprensión y la ampliación del sistema.

## 10. Control de versiones

El código fuente se encuentra alojado en GitHub y su desarrollo se registró mediante commits incrementales, permitiendo identificar los cambios realizados durante las diferentes etapas de implementación.

**Repositorio:**  
https://github.com/Marvin7715/proyecto2_manejo_implementacion_archivos

## 11. Autoría

Proyecto académico desarrollado como parte del Laboratorio 2 de Manejo de Archivos.
