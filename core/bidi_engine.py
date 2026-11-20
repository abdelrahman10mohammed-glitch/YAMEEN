# -*- coding: utf-8 -*-
"""
YAMEEN - Clean Text Processor
معالج نصوص نقي وآمن بدون أي تشويه للحروف أو علامات تخريبية
"""

import re

ARABIC_REGEX = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')

def contains_arabic(text: str) -> bool:
    """Returns True if text contains Arabic letters."""
    if not text:
        return False
    return bool(ARABIC_REGEX.search(text))

def clean_arabic_text(text: str) -> str:
    """
    Cleans text without corrupting character order.
    Removes invisible formatting junk while preserving the exact wording and code.
    """
    if not text:
        return ""
    # Remove rogue directional override characters that cause words to reverse
    cleaned = text.replace('\u202E', '').replace('\u202D', '')
    return cleaned
