# -*- coding: utf-8 -*-
"""
YAMEEN - Background Clipboard Watcher Daemon
مراقب الحافظة التلقائي في الخلفية لمعالجة نصوص الذكاء الاصطناعي فور نسخها
"""

import time
import threading
import pyperclip
from core.bidi_engine import contains_arabic, format_arabic_for_display, enhance_arabic_for_clipboard

class ClipboardWatcher(threading.Thread):
    def __init__(self, on_arabic_text_detected, auto_enhance_clipboard=True):
        super().__init__(daemon=True)
        self.on_arabic_text_detected = on_arabic_text_detected
        self.auto_enhance_clipboard = auto_enhance_clipboard
        self.running = False
        self._last_content = ""

    def run(self):
        self.running = True
        try:
            self._last_content = pyperclip.paste()
        except Exception:
            self._last_content = ""

        while self.running:
            try:
                current_content = pyperclip.paste()
                if current_content and current_content != self._last_content:
                    self._last_content = current_content
                    
                    if contains_arabic(current_content):
                        # Prepare display text and enhanced text
                        display_text = format_arabic_for_display(current_content)
                        enhanced_text = enhance_arabic_for_clipboard(current_content)

                        if self.auto_enhance_clipboard and current_content != enhanced_text:
                            # Update clipboard with directional marks silently
                            self._last_content = enhanced_text
                            pyperclip.copy(enhanced_text)

                        # Notify UI listener
                        if callable(self.on_arabic_text_detected):
                            self.on_arabic_text_detected(current_content, display_text)

            except Exception:
                pass

            time.sleep(0.35)

    def stop(self):
        self.running = False
