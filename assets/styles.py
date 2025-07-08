# Definición de estilos y colores para la aplicación

# Colores principales
PRIMARY_COLOR = "#3498db"  # Azul
SECONDARY_COLOR = "#2c3e50"  # Azul oscuro
ACCENT_COLOR = "#e74c3c"  # Rojo
SUCCESS_COLOR = "#2ecc71"  # Verde
WARNING_COLOR = "#f39c12"  # Naranja
INFO_COLOR = "#3498db"  # Azul claro
DARK_COLOR = "#2c3e50"  # Azul oscuro
LIGHT_COLOR = "#ecf0f1"  # Gris claro

# Fuentes
DEFAULT_FONT = "Helvetica"
HEADING_FONT = "Helvetica"
BUTTON_FONT = "Helvetica"

# Tamaños de fuente
SMALL_FONT_SIZE = 10
DEFAULT_FONT_SIZE = 12
LARGE_FONT_SIZE = 14
HEADING_FONT_SIZE = 18
TITLE_FONT_SIZE = 24

# Estilos de widgets
BUTTON_STYLE = {
    "font": (BUTTON_FONT, DEFAULT_FONT_SIZE),
    "width": 15,
    "padding": 5
}

LABEL_STYLE = {
    "font": (DEFAULT_FONT, DEFAULT_FONT_SIZE),
    "padding": 5
}

HEADING_STYLE = {
    "font": (HEADING_FONT, HEADING_FONT_SIZE),
    "padding": 10
}

ENTRY_STYLE = {
    "font": (DEFAULT_FONT, DEFAULT_FONT_SIZE),
    "width": 20
}

# Configuraciones de la aplicación
APP_NAME = "Dcorelp"
APP_VERSION = "1.0.0"
APP_TITLE = f"{APP_NAME} - Sistema de Gestión de Ventas v{APP_VERSION}"
APP_WIDTH = 1200
APP_HEIGHT = 700
APP_MIN_WIDTH = 800
APP_MIN_HEIGHT = 600

# Configuraciones de la tabla
TABLE_ROW_HEIGHT = 25
TABLE_HEADER_BG = SECONDARY_COLOR
TABLE_HEADER_FG = LIGHT_COLOR
TABLE_ROW_BG = LIGHT_COLOR
TABLE_ROW_BG_ALT = "#d6eaf8"  # Azul muy claro para filas alternadas
TABLE_ROW_FG = DARK_COLOR