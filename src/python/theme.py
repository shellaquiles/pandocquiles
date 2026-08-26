"""
theme.py

Gestor de paletas de colores y estilos dinámicos para PanDocquiles.
Permite seleccionar temas predefinidos o configurar colores personalizados.
"""
import os
from typing import Dict

THEMES: Dict[str, Dict[str, str]] = {
    "blue": {
        "name": "Azul Corporativo / Tech",
        "primary": "#1E40AF",
        "accent": "#2563EB",
        "bg_subtle": "#EFF6FF",
        "text_subtle": "#1E3A8A",
        "code_color": "#1E40AF",
        "link_color": "#2563EB"
    },
    "cdmx": {
        "name": "CDMX Institucional / Guinda",
        "primary": "#9D2449",
        "accent": "#B32850",
        "bg_subtle": "#FDF4F6",
        "text_subtle": "#5A122A",
        "code_color": "#9D2449",
        "link_color": "#9D2449"
    },
    "emerald": {
        "name": "Esmeralda / Naturaleza",
        "primary": "#065F46",
        "accent": "#059669",
        "bg_subtle": "#ECFDF5",
        "text_subtle": "#064E3B",
        "code_color": "#065F46",
        "link_color": "#059669"
    },
    "purple": {
        "name": "Púrpura / Moderno",
        "primary": "#6B21A8",
        "accent": "#7C3AED",
        "bg_subtle": "#FAF5FF",
        "text_subtle": "#581C87",
        "code_color": "#6B21A8",
        "link_color": "#7C3AED"
    },
    "amber": {
        "name": "Ámbar / Cálido",
        "primary": "#9A3412",
        "accent": "#EA580C",
        "bg_subtle": "#FFF7ED",
        "text_subtle": "#7C2D12",
        "code_color": "#9A3412",
        "link_color": "#EA580C"
    },
    "slate": {
        "name": "Gris Neutro / Minimalista",
        "primary": "#334155",
        "accent": "#475569",
        "bg_subtle": "#F8FAFC",
        "text_subtle": "#1E293B",
        "code_color": "#334155",
        "link_color": "#2563EB"
    }
}

# Alias para facilitar selección
ALIASES = {
    "corporate": "blue",
    "tech": "blue",
    "guinda": "cdmx",
    "forest": "emerald",
    "green": "emerald",
    "violet": "purple",
    "warm": "amber",
    "orange": "amber",
    "minimal": "slate",
    "gray": "slate"
}

def get_current_theme() -> Dict[str, str]:
    """
    Obtiene la paleta de colores activa basada en variables de entorno.
    Por defecto es 'blue'.
    """
    theme_key = os.environ.get("COLOR_THEME", os.environ.get("PDF_THEME_PALETTE", "blue")).lower().strip()
    theme_key = ALIASES.get(theme_key, theme_key)
    
    base_theme = THEMES.get(theme_key, THEMES["blue"]).copy()
    
    # Permitir sobrescribir colores individuales
    if os.environ.get("COLOR_PRIMARY"):
        base_theme["primary"] = os.environ.get("COLOR_PRIMARY").strip()
    if os.environ.get("COLOR_ACCENT"):
        base_theme["accent"] = os.environ.get("COLOR_ACCENT").strip()
    if os.environ.get("COLOR_BG_SUBTLE"):
        base_theme["bg_subtle"] = os.environ.get("COLOR_BG_SUBTLE").strip()
    if os.environ.get("COLOR_TEXT_SUBTLE"):
        base_theme["text_subtle"] = os.environ.get("COLOR_TEXT_SUBTLE").strip()
    if os.environ.get("COLOR_CODE"):
        base_theme["code_color"] = os.environ.get("COLOR_CODE").strip()
    if os.environ.get("COLOR_LINK"):
        base_theme["link_color"] = os.environ.get("COLOR_LINK").strip()
        
    return base_theme

def generate_css_variables() -> str:
    """
    Genera el bloque de variables CSS (:root) con la paleta activa.
    """
    theme = get_current_theme()
    return f"""<style>
:root {{
    --color-primary: {theme['primary']};
    --color-accent: {theme['accent']};
    --color-bg-subtle: {theme['bg_subtle']};
    --color-text-subtle: {theme['text_subtle']};
    --color-code: {theme.get('code_color', theme['primary'])};
    --color-link: {theme.get('link_color', theme['accent'])};
}}
</style>"""
