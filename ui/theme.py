# -*- coding: utf-8 -*-
"""
YAMEEN - 90s Classic Retro Station Theme
تصميم كلاسيكي مستوحى من برامج التسعينات بلوحات وبطاقات منفصلة (Retro Station Cards)
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
CAIRO_FONT_PATH = FONTS_DIR / "Cairo.ttf"

# Colors - 90s Retro Dark Station with Classic Crimson
COLORS = {
    "bg_main": "#181A1F",          # Deep Workstation Background
    "card_bg": "#23262F",          # 90s Elevated Card Panel
    "card_border": "#3A3F4E",      # Classic Beveled Border
    "card_inset": "#14161A",       # Inset Display Area
    
    "crimson_btn": "#990024",      # Classic Retro Crimson
    "crimson_hover": "#B3002D",    # Retro Crimson Hover
    
    "retro_btn": "#2D313C",        # Classic Tactile Button
    "retro_btn_hover": "#383E4C",  # Tactile Button Hover
    "retro_btn_border": "#474D5E",
    
    "status_on": "#10B981",        # LED Green
    "status_off": "#64748B",       # LED Gray
    
    "text_main": "#E8EAF0",        # Off-white Classic Text
    "text_muted": "#8E95A5",       # Retro Label Gray
}

def get_font(size: int = 12, weight: str = "normal"):
    # Return Cairo font tuple
    return ("Cairo", size, weight)
