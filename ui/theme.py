# -*- coding: utf-8 -*-
"""
YAMEEN - 90s Retro Station Theme with Robust Asset Resolution
"""

import sys
import os
from pathlib import Path

# Resolve path correctly in both normal Python and PyInstaller --onefile
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(getattr(sys, '_MEIPASS', os.path.dirname(sys.executable)))
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
CAIRO_FONT_PATH = FONTS_DIR / "Cairo.ttf"

# Colors - 90s Classic Retro Station (Physical Cards Aesthetic)
COLORS = {
    "bg_main": "#1A1C23",          # Solid Retro Desktop Background
    
    # 3D Raised Physical Cards
    "card_bg": "#262934",          # Raised Card Surface
    "card_border_light": "#424858",# Top/Left highlight for 3D bevel
    "card_border_dark": "#12141A", # Bottom/Right shadow
    "card_inset": "#13151A",       # Sunken/Inset screen area
    
    # Classic Buttons
    "crimson_btn": "#A6142E",      # Deep Classic Crimson Red
    "crimson_hover": "#C51A37",
    
    "retro_btn": "#323746",        # Solid Tactile Button
    "retro_btn_hover": "#3F4557",
    "retro_btn_border": "#4B5368",
    
    "status_on": "#10B981",        # LED Active
    "status_off": "#64748B",       # LED Inactive
    
    "text_main": "#F1F2F6",        # Clean Retro Off-White
    "text_muted": "#8C94A6",       # Label Slate Gray
    "text_tag": "#D1D5DB",
}

def get_font(size: int = 12, weight: str = "normal"):
    return ("Cairo", size, weight)
