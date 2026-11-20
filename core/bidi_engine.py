# -*- coding: utf-8 -*-
"""
YAMEEN - Arabic BiDi & Text Direction Engine
محرك معالجة ومحاذاة النصوص العربية وضبط الاتجاه
"""

import re
import arabic_reshaper
from bidi.algorithm import get_display

# Unicode Directional Marks
RLM = "\u200F"  # Right-to-Left Mark
LRM = "\u200E"  # Left-to-Right Mark

ARABIC_RANGE_REGEX = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')

def contains_arabic(text: str) -> bool:
    """Returns True if the text contains any Arabic characters."""
    if not text:
        return False
    return bool(ARABIC_RANGE_REGEX.search(text))

def ar(text: str) -> str:
    """
    Formats UI strings (labels, buttons, titles) so Arabic letters connect
    properly and flow correctly from Right-to-Left inside Tkinter/CustomTkinter.
    """
    if not text or not contains_arabic(text):
        return text
    try:
        # Reshape connected letters then apply BiDi ordering
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text

def format_arabic_for_display(text: str) -> str:
    """
    Reshapes and applies Unicode BiDi algorithm for multiline AI responses.
    Preserves code blocks (```...```) in pure LTR.
    """
    if not text or not contains_arabic(text):
        return text

    lines = text.split("\n")
    processed_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            processed_lines.append(line)
            continue

        if in_code_block or not contains_arabic(line):
            processed_lines.append(line)
            continue

        try:
            reshaped_text = arabic_reshaper.reshape(line)
            bidi_text = get_display(reshaped_text)
            processed_lines.append(bidi_text)
        except Exception:
            processed_lines.append(line)

    return "\n".join(processed_lines)

def enhance_arabic_for_clipboard(text: str) -> str:
    """
    Prepares Arabic text with Unicode Directional Marks (RLM)
    so when pasted into other apps, brackets and punctuation stay intact.
    """
    if not text or not contains_arabic(text):
        return text

    lines = text.split("\n")
    formatted_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            formatted_lines.append(line)
            continue

        if in_code_block or not line.strip() or not contains_arabic(line):
            formatted_lines.append(line)
            continue

        clean_line = line.strip()
        if not clean_line.startswith(RLM):
            formatted_line = f"{RLM}{clean_line}{RLM}"
        else:
            formatted_line = clean_line

        formatted_lines.append(formatted_line)

    return "\n".join(formatted_lines)
