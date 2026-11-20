# -*- coding: utf-8 -*-
"""
YAMEEN (يمين) - Arabic RTL Assistant & Patcher for AI Desktop Apps
نقطة انطلاق وتشغيل تطبيق يمين
"""

import sys
import os

# Ensure current directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import YameenApp

def main():
    app = YameenApp()
    app.mainloop()

if __name__ == "__main__":
    main()
