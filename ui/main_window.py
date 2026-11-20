# -*- coding: utf-8 -*-
"""
YAMEEN - Main User Interface (Classic Charcoal & Crimson Edition)
واجهة المستخدم الكلاسيكية الفخمة لبرنامج يمين
"""

import os
import ctypes
from pathlib import Path
import customtkinter as ctk
import pyperclip

from ui.theme import COLORS, get_font, CAIRO_FONT_PATH
from core.bidi_engine import format_arabic_for_display, enhance_arabic_for_clipboard, ar
from core.clipboard_watcher import ClipboardWatcher
from core.scanner import DynamicScanner

def register_cairo_font():
    """Registers Cairo font for the process."""
    if os.name == 'nt' and CAIRO_FONT_PATH.exists():
        try:
            ctypes.windll.gdi32.AddFontResourceExW(str(CAIRO_FONT_PATH), 0x10, 0)
        except Exception:
            pass

class YameenApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        register_cairo_font()

        # Window Appearance
        ctk.set_appearance_mode("dark")
        self.title("YAMEEN | يمين")
        self.geometry("740x780")
        self.minsize(680, 700)
        self.configure(fg_color=COLORS["bg_dark"])

        self.font_size = 14
        self.auto_clipboard_active = True

        self._build_ui()
        self._refresh_scanner()

        # Start Clipboard Watcher
        self.watcher = ClipboardWatcher(
            on_arabic_text_detected=self._on_clipboard_detected,
            auto_enhance_clipboard=self.auto_clipboard_active
        )
        self.watcher.start()

    def _build_ui(self):
        """Builds a classic, clean, elegant desktop layout."""

        # --- 1. TOP HEADER ---
        header = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"]
        )
        header.pack(fill="x", padx=20, pady=(16, 10))

        # Title Row
        top_row = ctk.CTkFrame(header, fg_color="transparent")
        top_row.pack(fill="x", padx=18, pady=(14, 4))

        # Left: Status indicator
        self.lbl_status = ctk.CTkLabel(
            top_row,
            text=ar("النظام نشط ومراقب الحافظة يعمل"),
            font=get_font(11, "bold"),
            text_color=COLORS["status_green"],
            fg_color=COLORS["bg_surface_alt"],
            corner_radius=6,
            padx=10,
            pady=4
        )
        self.lbl_status.pack(side="left")

        # Right: Main Title
        title_lbl = ctk.CTkLabel(
            top_row,
            text="YAMEEN | " + ar("يمين"),
            font=get_font(18, "bold"),
            text_color=COLORS["accent_primary"]
        )
        title_lbl.pack(side="right")

        # Subtitle
        subtitle = ctk.CTkLabel(
            header,
            text=ar("مصحح اتجاه النصوص والأقواس للغة العربية في برامج الذكاء الاصطناعي"),
            font=get_font(11),
            text_color=COLORS["text_secondary"],
            justify="right",
            anchor="e"
        )
        subtitle.pack(fill="x", padx=18, pady=(0, 12))

        # --- 2. DYNAMIC APPS SCANNER SECTION ---
        scanner_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"]
        )
        scanner_frame.pack(fill="x", padx=20, pady=6)

        # Scanner Header
        sc_header = ctk.CTkFrame(scanner_frame, fg_color="transparent")
        sc_header.pack(fill="x", padx=16, pady=(10, 6))

        btn_refresh = ctk.CTkButton(
            sc_header,
            text=ar("تحديث الفحص ⟳"),
            font=get_font(11),
            width=90,
            height=26,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["bg_surface_hover"],
            text_color=COLORS["text_secondary"],
            border_width=1,
            border_color=COLORS["border"],
            command=self._refresh_scanner
        )
        btn_refresh.pack(side="left")

        sc_title = ctk.CTkLabel(
            sc_header,
            text=ar("التطبيقات النشطة المكتشفة حالياً في النظام:"),
            font=get_font(12, "bold"),
            text_color=COLORS["text_primary"]
        )
        sc_title.pack(side="right")

        # Apps Container (Dynamic List)
        self.apps_box = ctk.CTkFrame(scanner_frame, fg_color=COLORS["bg_dark"], corner_radius=6)
        self.apps_box.pack(fill="x", padx=16, pady=4)

        # Action Buttons Row
        action_row = ctk.CTkFrame(scanner_frame, fg_color="transparent")
        action_row.pack(fill="x", padx=16, pady=(10, 14))

        self.btn_reset = ctk.CTkButton(
            action_row,
            text=ar("استرجاع الوضع الافتراضي ↺"),
            font=get_font(12),
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["bg_surface_hover"],
            text_color=COLORS["text_secondary"],
            border_width=1,
            border_color=COLORS["border"],
            height=36,
            width=170,
            command=self._unpatch_all
        )
        self.btn_reset.pack(side="left")

        self.btn_inject = ctk.CTkButton(
            action_row,
            text=ar("تفعيل الاتجاه لليمين فوراً (Direct Inject) ⚡"),
            font=get_font(12, "bold"),
            fg_color=COLORS["accent_primary"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["text_on_accent"],
            height=36,
            command=self._patch_all
        )
        self.btn_inject.pack(side="right", fill="x", expand=True, padx=(12, 0))

        # --- 3. LIVE READER & CONVERTER ---
        reader_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_surface"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"]
        )
        reader_frame.pack(fill="both", expand=True, padx=20, pady=6)

        # Toolbar
        toolbar = ctk.CTkFrame(reader_frame, fg_color="transparent")
        toolbar.pack(fill="x", padx=16, pady=(10, 6))

        # Left tools
        self.btn_copy = ctk.CTkButton(
            toolbar,
            text=ar("نسخ 📋"),
            font=get_font(11),
            width=65,
            height=26,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["bg_surface_hover"],
            text_color=COLORS["text_primary"],
            border_width=1,
            border_color=COLORS["border"],
            command=self._copy_text
        )
        self.btn_copy.pack(side="left", padx=3)

        self.btn_clear = ctk.CTkButton(
            toolbar,
            text=ar("تفريغ 🗑"),
            font=get_font(11),
            width=65,
            height=26,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["bg_surface_hover"],
            text_color=COLORS["text_muted"],
            border_width=1,
            border_color=COLORS["border"],
            command=self._clear_text
        )
        self.btn_clear.pack(side="left", padx=3)

        self.btn_plus = ctk.CTkButton(
            toolbar,
            text="A+",
            font=get_font(11, "bold"),
            width=36,
            height=26,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["bg_surface_hover"],
            text_color=COLORS["accent_primary"],
            border_width=1,
            border_color=COLORS["border"],
            command=self._inc_font
        )
        self.btn_plus.pack(side="left", padx=3)

        self.btn_minus = ctk.CTkButton(
            toolbar,
            text="A-",
            font=get_font(11, "bold"),
            width=36,
            height=26,
            fg_color=COLORS["bg_surface_alt"],
            hover_color=COLORS["bg_surface_hover"],
            text_color=COLORS["accent_primary"],
            border_width=1,
            border_color=COLORS["border"],
            command=self._dec_font
        )
        self.btn_minus.pack(side="left", padx=3)

        reader_label = ctk.CTkLabel(
            toolbar,
            text=ar("القارئ المباشر للنصوص المعدولة (Live Reader)"),
            font=get_font(12, "bold"),
            text_color=COLORS["text_primary"]
        )
        reader_label.pack(side="right")

        # Text Area
        self.text_box = ctk.CTkTextbox(
            reader_frame,
            fg_color=COLORS["bg_dark"],
            text_color=COLORS["text_primary"],
            font=get_font(self.font_size),
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=6,
            wrap="word"
        )
        self.text_box.pack(fill="both", expand=True, padx=16, pady=(4, 8))

        welcome = format_arabic_for_display(
            "مرحباً بك في أداة يمين (YAMEEN).\n\n"
            "• عند نسخ أي نص عربي من برامج الذكاء الاصطناعي، سيظهر هنا معدولاً تلقائياً مع ترتيب الأقواس والكلمات الإنجليزية.\n"
            "• اضغط زر 'تفعيل الاتجاه لليمين' لحقن المحاذاة داخل التطبيقات المفتوحة مباشرة."
        )
        self.text_box.insert("1.0", welcome)

        # Options Row
        options_row = ctk.CTkFrame(reader_frame, fg_color="transparent")
        options_row.pack(fill="x", padx=16, pady=(0, 10))

        self.clip_toggle = ctk.CTkSwitch(
            options_row,
            text=ar("إصلاح الحافظة تلقائياً عند النسخ (Auto-fix Clipboard)"),
            font=get_font(11),
            text_color=COLORS["text_secondary"],
            progress_color=COLORS["accent_primary"],
            command=self._on_toggle_clip
        )
        self.clip_toggle.select()
        self.clip_toggle.pack(side="right")

        # --- 4. FOOTER ---
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.pack(fill="x", padx=20, pady=(2, 14))

        self.lbl_msg = ctk.CTkLabel(
            footer,
            text=ar("جاهز • YAMEEN v1.0.0 (Open Source)"),
            font=get_font(11),
            text_color=COLORS["text_muted"]
        )
        self.lbl_msg.pack(side="right")

    def _refresh_scanner(self):
        """Scans running user processes dynamically."""
        for w in self.apps_box.winfo_children():
            w.destroy()

        apps = DynamicScanner.get_running_processes()
        if not apps:
            empty_lbl = ctk.CTkLabel(
                self.apps_box,
                text=ar("لا توجد تطبيقات معروفة قيد التشغيل حالياً."),
                font=get_font(11),
                text_color=COLORS["text_muted"]
            )
            empty_lbl.pack(pady=8)
            return

        for app in apps:
            row = ctk.CTkFrame(self.apps_box, fg_color=COLORS["bg_surface_alt"], corner_radius=4)
            row.pack(fill="x", padx=4, pady=2)

            st_lbl = ctk.CTkLabel(
                row,
                text=ar("● قيد التشغيل"),
                font=get_font(10, "bold"),
                text_color=COLORS["status_green"]
            )
            st_lbl.pack(side="left", padx=10, pady=4)

            name_lbl = ctk.CTkLabel(
                row,
                text=f"{app['icon']} {app['name']} ({app['category']})",
                font=get_font(11, "bold"),
                text_color=COLORS["text_primary"]
            )
            name_lbl.pack(side="right", padx=10, pady=4)

    def _patch_all(self):
        count = DynamicScanner.inject_rtl_to_all_active(remove=False)
        if count > 0:
            self.lbl_msg.configure(text=ar(f"تم تفعيل YAMEEN بنجاح في {count} نافذة!"), text_color=COLORS["status_green"])
        else:
            self.lbl_msg.configure(text=ar("تم فحص النوافذ - جاهز للاستخدام ومراقبة الحافظة"), text_color=COLORS["accent_primary"])

    def _unpatch_all(self):
        DynamicScanner.inject_rtl_to_all_active(remove=True)
        self.lbl_msg.configure(text=ar("تم استرجاع الوضع الافتراضي"), text_color=COLORS["text_secondary"])

    def _on_clipboard_detected(self, raw: str, formatted: str):
        self.after(0, self._render_new_text, formatted)

    def _render_new_text(self, text: str):
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", text)
        self.lbl_msg.configure(text=ar("تم التقاط نص عربي من الحافظة وتنسيقه بنجاح!"), text_color=COLORS["status_green"])

    def _copy_text(self):
        val = self.text_box.get("1.0", "end-1c")
        if val:
            pyperclip.copy(enhance_arabic_for_clipboard(val))
            self.lbl_msg.configure(text=ar("تم نسخ النص المعدول للحافظة بنجاح"), text_color=COLORS["status_green"])

    def _clear_text(self):
        self.text_box.delete("1.0", "end")

    def _inc_font(self):
        if self.font_size < 26:
            self.font_size += 2
            self.text_box.configure(font=get_font(self.font_size))

    def _dec_font(self):
        if self.font_size > 10:
            self.font_size -= 2
            self.text_box.configure(font=get_font(self.font_size))

    def _on_toggle_clip(self):
        self.auto_clipboard_active = self.clip_toggle.get() == 1
        if self.watcher:
            self.watcher.auto_enhance_clipboard = self.auto_clipboard_active
