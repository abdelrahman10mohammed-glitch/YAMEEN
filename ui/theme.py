# -*- coding: utf-8 -*-
"""
YAMEEN - Classic Burgundy & Charcoal Theme
تصميم كلاسيكي فخم باللون الكحلي الفحمي مع لمسات الأحمر الكلاسيكي (Crimson/Burgundy)
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
CAIRO_FONT_PATH = FONTS_DIR / "Cairo.ttf"

# Colors - Classic Charcoal & Crimson Palette
COLORS = {
    "bg_dark": "#121316",          # Deep Charcoal Black
    "bg_surface": "#1A1C22",       # Card Surface
    "bg_surface_alt": "#21242C",   # Alternate Card Surface
    "bg_surface_hover": "#282C35", # Hover State
    "border": "#2E333D",           # Classic Crisp Border
    "border_focus": "#E11D48",     # Crimson Red Focus

    "accent_primary": "#E11D48",   # Classic Crimson Red
    "accent_hover": "#BE123C",     # Deep Burgundy Hover
    "accent_dark": "#881337",      # Dark Wine
    "accent_subtle": "#31141C",    # Subtle Red Background Tint

    "status_green": "#10B981",     # Active Indicator
    "status_gray": "#6B7280",      # Inactive Indicator

    "text_primary": "#F4F4F6",     # Crisp Off-White
    "text_secondary": "#A1A7B4",   # Refined Silver Gray
    "text_muted": "#6C7280",       # Muted Labels
    "text_on_accent": "#FFFFFF",   # Text on Red Buttons
}

FONT_FAMILY = "Cairo"

def get_font(size: int = 13, weight: str = "normal"):
    """Returns the font tuple for CustomTkinter widgets."""
    return (FONT_FAMILY, size, weight)
