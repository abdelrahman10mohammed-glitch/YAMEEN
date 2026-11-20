# -*- coding: utf-8 -*-
"""
YAMEEN - Passive Clipboard Listener
يراقب الحافظة بأمان لقراءة النصوص دون التعديل عليها تلقائياً
"""

import time
import threading
import pyperclip
from core.bidi_engine import contains_arabic, clean_arabic_text

class ClipboardWatcher(threading.Thread):
    def __init__(self, on_text_detected):
        super().__init__(daemon=True)
        self.on_text_detected = on_text_detected
        self.running = False
        self._last_clip = ""

    def run(self):
        self.running = True
        try:
            self._last_clip = pyperclip.paste()
        except Exception:
            self._last_clip = ""

        while self.running:
            try:
                current = pyperclip.paste()
                if current and current != self._last_clip:
                    self._last_clip = current
                    if contains_arabic(current):
                        cleaned = clean_arabic_text(current)
                        if callable(self.on_text_detected):
                            self.on_text_detected(cleaned)
            except Exception:
                pass

            time.sleep(0.4)

    def stop(self):
        self.running = False
