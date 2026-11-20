# -*- coding: utf-8 -*-
"""
YAMEEN - Precision AI Application Scanner & Safe Patcher
فاحص دقيق ومحدد لتطبيقات الذكاء الاصطناعي فقط بدون إضافة برامج خلفية
"""

import os
import csv
import subprocess
import json
import urllib.request

try:
    import websocket
except ImportError:
    websocket = None

# Only the specific AI applications
AI_TARGETS = [
    {
        "id": "antigravity",
        "name": "Antigravity",
        "process": "antigravity.exe",
        "icon": "⚡",
        "port_dir": os.path.join(os.environ.get("APPDATA", ""), "Antigravity")
    },
    {
        "id": "claude",
        "name": "Claude Desktop",
        "process": "claude.exe",
        "icon": "🟣",
        "port_dir": os.path.join(os.environ.get("APPDATA", ""), "Claude")
    },
    {
        "id": "manus",
        "name": "Manus Desktop",
        "process": "manus.exe",
        "icon": "🤖",
        "port_dir": os.path.join(os.environ.get("APPDATA", ""), "Manus")
    },
    {
        "id": "chatgpt",
        "name": "ChatGPT Desktop",
        "process": "chatgpt.exe",
        "icon": "🟢",
        "port_dir": os.path.join(os.environ.get("APPDATA", ""), "ChatGPT")
    }
]

# Safe, targeted CSS rule for message bubbles only (NOT on * to prevent layout destruction)
SAFE_RTL_CSS = (
    "div[class*='message'] p, div[class*='chat'] p, div[class*='bubble'] p, "
    ".markdown-body p, [data-message-author-role='assistant'] p { "
    "direction: rtl !important; text-align: right !important; }"
)

class PrecisionScanner:
    @staticmethod
    def get_running_ai_apps() -> list:
        """Checks which of the primary AI applications are currently running."""
        running_procs = set()
        try:
            output = subprocess.check_output(
                ["tasklist.exe", "/FO", "CSV", "/NH"],
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            for row in csv.reader(output.splitlines()):
                if row and len(row) > 0:
                    running_procs.add(row[0].strip().lower())
        except Exception:
            pass

        results = []
        for target in AI_TARGETS:
            is_running = target["process"] in running_procs
            port_file = os.path.join(target["port_dir"], "DevToolsActivePort")
            has_devtools = os.path.exists(port_file)
            
            port = None
            if has_devtools:
                try:
                    with open(port_file, "r", encoding="utf-8") as f:
                        port = f.readline().strip()
                except Exception:
                    pass

            results.append({
                "id": target["id"],
                "name": target["name"],
                "icon": target["icon"],
                "running": is_running,
                "port": port
            })

        return results

    @classmethod
    def apply_safe_rtl(cls, remove: bool = False) -> int:
        """Applies or cleans the safe RTL style on active DevTools ports."""
        if not websocket:
            return 0

        apps = cls.get_running_ai_apps()
        success_count = 0

        for app in apps:
            port = app.get("port")
            if not port:
                continue

            try:
                req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=2)
                pages = json.loads(req.read().decode())

                js_code = f"""
                (function() {{
                    var old = document.getElementById('yameen-safe-rtl');
                    if (old) old.remove();
                    if ({'true' if remove else 'false'}) {{
                        return 'Removed';
                    }}
                    var s = document.createElement('style');
                    s.id = 'yameen-safe-rtl';
                    s.textContent = `{SAFE_RTL_CSS}`;
                    document.head.appendChild(s);
                    return 'Applied';
                }})()
                """

                for page in pages:
                    ws_url = page.get("webSocketDebuggerUrl")
                    if not ws_url:
                        continue
                    try:
                        ws = websocket.create_connection(ws_url, suppress_origin=True, timeout=2)
                        cmd = json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": js_code}})
                        ws.send(cmd)
                        _ = ws.recv()
                        ws.close()
                        success_count += 1
                    except Exception:
                        pass
            except Exception:
                pass

        return success_count
