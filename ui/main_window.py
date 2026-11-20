# -*- coding: utf-8 -*-
"""
YAMEEN - 90s Classic Retro Station (Physical Cards Edition)
تصميم بطاقات وكروت كلاسيكية بارزة ومستقلة
"""

import os
import sys
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
        self.geometry("720x760")
        self.minsize(660, 700)
        self.configure(fg_color=COLORS["bg_main"])

        self.font_size = 13
        self._build_ui()
        self._refresh_apps()

        # Start passive clipboard watcher
        self.watcher = ClipboardWatcher(on_text_detected=self._on_clip_text)
        self.watcher.start()

    def _build_ui(self):
        # ========================================================
        # 🎴 CARD 1: HEADER & STATUS (كارت العنوان والتعريف)
        # ========================================================
        card_header = ctk.CTkFrame(
            self,
            fg_color=COLORS["card_bg"],
            corner_radius=6,
            border_width=2,
            border_color=COLORS["card_border_light"]
        )
        card_header.pack(fill="x", padx=16, pady=(14, 8))

        h_layout = ctk.CTkFrame(card_header, fg_color="transparent")
        h_layout.pack(fill="x", padx=14, pady=10)

        # Left Status Box
        self.status_pill = ctk.CTkLabel(
            h_layout,
            text="[ ● المراقبة نشطة ]",
            font=get_font(11, "bold"),
            text_color=COLORS["status_on"],
            fg_color=COLORS["card_inset"],
            corner_radius=4,
            padx=10,
            pady=4
        )
        self.status_pill.pack(side="left")

        # Right Title
        title_lbl = ctk.CTkLabel(
            h_layout,
            text="⚡ YAMEEN | يمين",
            font=get_font(18, "bold"),
            text_color=COLORS["crimson_btn"]
        )
        title_lbl.pack(side="right")

        # ========================================================
        # 🎴 CARD 2: AI APPS GRID (كارت فحص وتفعيل البرامج)
        # ========================================================
        self.card_apps = ctk.CTkFrame(
            self,
            fg_color=COLORS["card_bg"],
            corner_radius=6,
            border_width=2,
            border_color=COLORS["card_border_light"]
        )
        self.card_apps.pack(fill="x", padx=16, pady=6)

        # Title strip inside card
        apps_top = ctk.CTkFrame(self.card_apps, fg_color=COLORS["card_inset"], corner_radius=4)
        apps_top.pack(fill="x", padx=10, pady=(10, 8))

        btn_scan = ctk.CTkButton(
            apps_top,
            text="⟳ إعادة الفحص",
            font=get_font(11),
            width=90,
            height=26,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=3,
            command=self._refresh_apps
        )
        btn_scan.pack(side="left", padx=6, pady=4)

        lbl_apps_head = ctk.CTkLabel(
            apps_top,
            text="تطبيقات الذكاء الاصطناعي المستهدفة",
            font=get_font(11, "bold"),
            text_color=COLORS["text_main"]
        )
        lbl_apps_head.pack(side="right", padx=10, pady=4)

        # 2x2 Grid of physical mini-cards for the 4 AI apps
        self.grid_frame = ctk.CTkFrame(self.card_apps, fg_color="transparent")
        self.grid_frame.pack(fill="x", padx=10, pady=4)
        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)

        # Action Buttons inside Card 2
        actions_bar = ctk.CTkFrame(self.card_apps, fg_color="transparent")
        actions_bar.pack(fill="x", padx=10, pady=(10, 12))

        self.btn_reset = ctk.CTkButton(
            actions_bar,
            text="↺ استرجاع الوضع الأصلي",
            font=get_font(11),
            width=160,
            height=34,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=4,
            command=self._unpatch
        )
        self.btn_reset.pack(side="left")

        self.btn_apply = ctk.CTkButton(
            actions_bar,
            text="⚡ تفعيل محاذاة اليمين فوراً (Safe RTL)",
            font=get_font(12, "bold"),
            height=34,
            fg_color=COLORS["crimson_btn"],
            hover_color=COLORS["crimson_hover"],
            text_color="#FFFFFF",
            corner_radius=4,
            command=self._apply_patch
        )
        self.btn_apply.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # ========================================================
        # 🎴 CARD 3: RETRO LIVE READER (كارت القارئ الفوري المباشر)
        # ========================================================
        card_reader = ctk.CTkFrame(
            self,
            fg_color=COLORS["card_bg"],
            corner_radius=6,
            border_width=2,
            border_color=COLORS["card_border_light"]
        )
        card_reader.pack(fill="both", expand=True, padx=16, pady=6)

        # Reader Controls Strip
        r_bar = ctk.CTkFrame(card_reader, fg_color=COLORS["card_inset"], corner_radius=4)
        r_bar.pack(fill="x", padx=10, pady=(10, 6))

        # Controls Left
        self.btn_copy = ctk.CTkButton(
            r_bar,
            text="📋 نسخ",
            font=get_font(11),
            width=55,
            height=24,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=3,
            command=self._copy_content
        )
        self.btn_copy.pack(side="left", padx=4, pady=4)

        self.btn_clear = ctk.CTkButton(
            r_bar,
            text="🗑 مسح",
            font=get_font(11),
            width=55,
            height=24,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=3,
            command=self._clear_content
        )
        self.btn_clear.pack(side="left", padx=4, pady=4)

        btn_plus = ctk.CTkButton(
            r_bar,
            text="A+",
            font=get_font(11, "bold"),
            width=32,
            height=24,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=3,
            command=self._font_up
        )
        btn_plus.pack(side="left", padx=2, pady=4)

        btn_minus = ctk.CTkButton(
            r_bar,
            text="A-",
            font=get_font(11, "bold"),
            width=32,
            height=24,
            fg_color=COLORS["retro_btn"],
            hover_color=COLORS["retro_btn_hover"],
            border_width=1,
            border_color=COLORS["retro_btn_border"],
            corner_radius=3,
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

        # Inset Screen
        self.text_display = ctk.CTkTextbox(
            card_reader,
            fg_color=COLORS["card_inset"],
            text_color=COLORS["text_main"],
            font=get_font(self.font_size),
            border_width=1,
            border_color=COLORS["card_border_light"],
            corner_radius=4,
            wrap="word"
        )
        self.text_display.pack(fill="both", expand=True, padx=10, pady=(2, 10))

        welcome = (
            "مرحباً بك في أداة يمين (YAMEEN).\n\n"
            "• عند نسخ أي نص من أي شات ذكاء اصطناعي، سيظهر هنا فوراً وبخط واضح مع إمكانية تكبير وتصغير الخط.\n"
            "• استخدم زر [تفعيل محاذاة اليمين] لمحاذاة فقرات الردود في النوافذ المفتوحة بأمان وبدون أي تأثير على شكل النصوص."
        )
        self.text_display.insert("1.0", welcome)

        # ========================================================
        # 🎴 STATUS FOOTER BAR
        # ========================================================
        self.status_bar = ctk.CTkLabel(
            self,
            text="الحالة: جاهز للاستخدام | YAMEEN Classic Edition v1.2",
            font=get_font(10),
            text_color=COLORS["text_muted"],
            anchor="e"
        )
        self.status_bar.pack(fill="x", padx=18, pady=(2, 10))

    def _refresh_apps(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        apps = PrecisionScanner.get_running_ai_apps()
        for idx, app in enumerate(apps):
            row = idx // 2
            col = idx % 2

            mini_card = ctk.CTkFrame(
                self.grid_frame,
                fg_color=COLORS["card_inset"],
                corner_radius=4,
                border_width=1,
                border_color=COLORS["card_border_light"]
            )
            mini_card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

            is_on = app["running"]
            st_text = "● قيد التشغيل" if is_on else "○ غير مفتوح"
            st_color = COLORS["status_on"] if is_on else COLORS["status_off"]

            lbl_st = ctk.CTkLabel(mini_card, text=st_text, font=get_font(10, "bold"), text_color=st_color)
            lbl_st.pack(side="left", padx=10, pady=8)

            lbl_name = ctk.CTkLabel(
                mini_card,
                text=f"{app['icon']} {app['name']}",
                font=get_font(11, "bold"),
                text_color=COLORS["text_main"]
            )
            lbl_name.pack(side="right", padx=10, pady=8)

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
