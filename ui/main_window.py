# -*- coding: utf-8 -*-
"""
YAMEEN - 90s Retro Station Edition
واجهة يمين الكلاسيكية المستوحاة من برامج التسعينات (Retro Cards)
"""

import os
import ctypes
from pathlib import Path
import customtkinter as ctk
import pyperclip

from ui.theme import COLORS, get_font, CAIRO_FONT_PATH
from core.scanner import PrecisionScanner
from core.clipboard_watcher import ClipboardWatcher

def register_cairo_font():
    """Register Cairo font in Windows GDI for the process."""
    if os.name == 'nt' and CAIRO_FONT_PATH.exists():
        try:
            ctypes.windll.gdi32.AddFontResourceExW(str(CAIRO_FONT_PATH), 0x10, 0)
        except Exception:
            pass

class YameenApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        register_cairo_font()

        ctk.set_appearance_mode("dark")
        self.title("YAMEEN (يمين) - الإصدار الكلاسيكي")
        self.geometry("700x720")
        self.minsize(640, 660)
        self.configure(fg_color=COLORS["bg_main"])

        self.font_size = 13
        self._build_ui()
        self._refresh_apps()

        # Start passive clipboard listener
        self.watcher = ClipboardWatcher(on_text_detected=self._on_clip_text)
        self.watcher.start()

    def _build_ui(self):
        # --- 1. HEADER CARD (بطاقة العنوان) ---
        header_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card_bg"],
            corner_radius=4,
            border_width=2,
            border_color=COLORS["card_border"]
        )
        header_card.pack(fill="x", padx=16, pady=(14, 8))

        h_inner = ctk.CTkFrame(header_card, fg_color="transparent")
        h_inner.pack(fill="x", padx=14, pady=10)

        # Left status badge
        self.lbl_status = ctk.CTkLabel(
            h_inner,
            text="[ ● المراقبة نشطة ]",
            font=get_font(11, "bold"),
            text_color=COLORS["status_on"],
            fg_color=COLORS["card_inset"],
            corner_radius=3,
            padx=8,
            pady=3
        )
        self.lbl_status.pack(side="left")

        # Right Title
        title = ctk.CTkLabel(
            h_inner,
            text="YAMEEN | يمين",
            font=get_font(18, "bold"),
            text_color=COLORS["crimson_btn"]
        )
        title.pack(side="right")

        # --- 2. APPS MANAGEMENT CARD (كارت فحص وتفعيل البرامج) ---
        apps_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card_bg"],
            corner_radius=4,
            border_width=2,
            border_color=COLORS["card_border"]
        )
        apps_card.pack(fill="x", padx=16, pady=6)

        # Card Title Bar
        app_bar = ctk.CTkFrame(apps_card, fg_color=COLORS["card_inset"], corner_radius=2)
        app_bar.pack(fill="x", padx=10, pady=(10, 6))

        btn_refresh = ctk.CTkButton(
            app_bar,
            text="تحديث الفحص ⟳",
            font=get_font(11),
            width=85,
            height=24,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=2,
            command=self._refresh_apps
        )
        btn_refresh.pack(side="left", padx=6, pady=4)

        app_title = ctk.CTkLabel(
            app_bar,
            text="تطبيقات الذكاء الاصطناعي (AI Desktop Apps)",
            font=get_font(11, "bold"),
            text_color=COLORS["text_main"]
        )
        app_title.pack(side="right", padx=10, pady=4)

        # App Grid Box
        self.apps_container = ctk.CTkFrame(apps_card, fg_color="transparent")
        self.apps_container.pack(fill="x", padx=10, pady=6)

        # Control Buttons
        btn_box = ctk.CTkFrame(apps_card, fg_color="transparent")
        btn_box.pack(fill="x", padx=10, pady=(8, 12))

        self.btn_reset = ctk.CTkButton(
            btn_box,
            text="استرجاع الوضع الافتراضي",
            font=get_font(11),
            width=160,
            height=32,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=3,
            command=self._unpatch
        )
        self.btn_reset.pack(side="left")

        self.btn_apply = ctk.CTkButton(
            btn_box,
            text="تفعيل محاذاة اليمين (Safe RTL)",
            font=get_font(12, "bold"),
            height=32,
            fg_color=COLORS["crimson_btn"],
            hover_color=COLORS["crimson_hover"],
            text_color="#FFFFFF",
            corner_radius=3,
            command=self._apply_patch
        )
        self.btn_apply.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # --- 3. RETRO LIVE READER CARD (كارت القارئ المباشر) ---
        reader_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card_bg"],
            corner_radius=4,
            border_width=2,
            border_color=COLORS["card_border"]
        )
        reader_card.pack(fill="both", expand=True, padx=16, pady=6)

        # Reader Toolbar
        r_bar = ctk.CTkFrame(reader_card, fg_color=COLORS["card_inset"], corner_radius=2)
        r_bar.pack(fill="x", padx=10, pady=(10, 6))

        # Toolbar Buttons
        self.btn_copy = ctk.CTkButton(
            r_bar,
            text="نسخ",
            font=get_font(11),
            width=50,
            height=22,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=2,
            command=self._copy_content
        )
        self.btn_copy.pack(side="left", padx=4, pady=4)

        self.btn_clear = ctk.CTkButton(
            r_bar,
            text="مسح",
            font=get_font(11),
            width=50,
            height=22,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=2,
            command=self._clear_content
        )
        self.btn_clear.pack(side="left", padx=4, pady=4)

        btn_plus = ctk.CTkButton(
            r_bar,
            text="+",
            font=get_font(11, "bold"),
            width=28,
            height=22,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=2,
            command=self._font_up
        )
        btn_plus.pack(side="left", padx=2, pady=4)

        btn_minus = ctk.CTkButton(
            r_bar,
            text="-",
            font=get_font(11, "bold"),
            width=28,
            height=22,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=2,
            command=self._font_down
        )
        btn_minus.pack(side="left", padx=2, pady=4)

        r_title = ctk.CTkLabel(
            r_bar,
            text="القارئ الفوري المباشر للنصوص",
            font=get_font(11, "bold"),
            text_color=COLORS["text_main"]
        )
        r_title.pack(side="right", padx=10, pady=4)

        # Inset Text Display Box
        self.text_display = ctk.CTkTextbox(
            reader_card,
            fg_color=COLORS["card_inset"],
            text_color=COLORS["text_main"],
            font=get_font(self.font_size),
            border_width=1,
            border_color=COLORS["card_border"],
            corner_radius=2,
            wrap="word"
        )
        self.text_display.pack(fill="both", expand=True, padx=10, pady=(2, 10))

        welcome = (
            "أهلاً بك في أداة يمين.\n\n"
            "• عند نسخ أي نص من أي شات ذكاء اصطناعي، سيظهر هنا فوراً وبخط واضح مع إمكانية تكبير وتصغير الخط.\n"
            "• استخدم زر [تفعيل محاذاة اليمين] لمحاذاة فقرات الردود في النوافذ المفتوحة بأمان وبدون أي تأثير على شكل النصوص."
        )
        self.text_display.insert("1.0", welcome)

        # --- 4. RETRO STATUS BAR ---
        self.status_bar = ctk.CTkLabel(
            self,
            text="الحالة: جاهز للاستخدام | YAMEEN Classic Edition v1.2",
            font=get_font(10),
            text_color=COLORS["text_muted"],
            anchor="e"
        )
        self.status_bar.pack(fill="x", padx=18, pady=(2, 10))

    def _refresh_apps(self):
        for w in self.apps_container.winfo_children():
            w.destroy()

        apps = PrecisionScanner.get_running_ai_apps()
        for app in apps:
            item = ctk.CTkFrame(
                self.apps_container,
                fg_color=COLORS["card_inset"],
                corner_radius=3,
                border_width=1,
                border_color=COLORS["card_border"]
            )
            item.pack(fill="x", pady=2)

            is_on = app["running"]
            st_text = "● قيد التشغيل" if is_on else "○ غير مفتوح"
            st_color = COLORS["status_on"] if is_on else COLORS["status_off"]

            lbl_st = ctk.CTkLabel(item, text=st_text, font=get_font(10, "bold"), text_color=st_color)
            lbl_st.pack(side="left", padx=10, pady=5)

            lbl_name = ctk.CTkLabel(
                item,
                text=f"{app['icon']} {app['name']}",
                font=get_font(11, "bold"),
                text_color=COLORS["text_main"]
            )
            lbl_name.pack(side="right", padx=10, pady=5)

    def _apply_patch(self):
        count = PrecisionScanner.apply_safe_rtl(remove=False)
        if count > 0:
            self.status_bar.configure(text=f"تم تطبيق المحاذاة الآمنة في {count} نافذة بنجاح.", text_color=COLORS["status_on"])
        else:
            self.status_bar.configure(text="النوافذ مفحوصة - المراقبة المباشرة جاهزة.", text_color=COLORS["text_main"])

    def _unpatch(self):
        PrecisionScanner.apply_safe_rtl(remove=True)
        self.status_bar.configure(text="تم استرجاع التنسيق الأصلي للبرامج.", text_color=COLORS["text_muted"])

    def _on_clip_text(self, text: str):
        self.after(0, self._set_text, text)

    def _set_text(self, text: str):
        self.text_display.delete("1.0", "end")
        self.text_display.insert("1.0", text)
        self.status_bar.configure(text="تم استلام نص عربي جديد من الحافظة.", text_color=COLORS["status_on"])

    def _copy_content(self):
        val = self.text_display.get("1.0", "end-1c")
        if val:
            pyperclip.copy(val)
            self.status_bar.configure(text="تم نسخ النص إلى الحافظة.", text_color=COLORS["status_on"])

    def _clear_content(self):
        self.text_display.delete("1.0", "end")

    def _font_up(self):
        if self.font_size < 24:
            self.font_size += 2
            self.text_display.configure(font=get_font(self.font_size))

    def _font_down(self):
        if self.font_size > 10:
            self.font_size -= 2
            self.text_display.configure(font=get_font(self.font_size))
