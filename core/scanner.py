# -*- coding: utf-8 -*-
"""
YAMEEN - Dynamic Application & Process Scanner
فاحص العمليات والتطبيقات النشطة في النظام بشكل ديناميكي وحي
"""

import os
import csv
import subprocess
import urllib.request
import json

try:
    import websocket
except ImportError:
    websocket = None

# Known AI and Editor apps catalog
KNOWN_TARGETS = {
    "antigravity.exe": {"name": "Antigravity", "category": "AI Editor", "icon": "⚡"},
    "claude.exe": {"name": "Claude Desktop", "category": "AI Assistant", "icon": "🟣"},
    "manus.exe": {"name": "Manus Desktop", "category": "AI Agent", "icon": "🤖"},
    "manustaskpanel.exe": {"name": "Manus Panel", "category": "AI Agent", "icon": "🤖"},
    "chatgpt.exe": {"name": "ChatGPT Desktop", "category": "AI Assistant", "icon": "🟢"},
    "cursor.exe": {"name": "Cursor", "category": "AI Editor", "icon": "⚡"},
    "code.exe": {"name": "VS Code", "category": "Code Editor", "icon": "💻"},
    "brave.exe": {"name": "Brave Browser", "category": "Web Browser", "icon": "🦁"},
    "chrome.exe": {"name": "Google Chrome", "category": "Web Browser", "icon": "🌐"},
    "msedge.exe": {"name": "Microsoft Edge", "category": "Web Browser", "icon": "🌊"},
}

RTL_CSS_RULE = (
    "* { unicode-bidi: plaintext !important; } "
    "div, p, li, span, blockquote, [contenteditable='true'], textarea, [class*='markdown'], [class*='message'] { "
    "direction: auto !important; text-align: start !important; }"
)

class DynamicScanner:
    @staticmethod
    def get_running_processes() -> dict:
        """
        Dynamically inspects running processes in the current user session.
        Returns a dict of running processes with categories.
        """
        active_apps = []
        try:
            output = subprocess.check_output(
                ["tasklist.exe", "/FO", "CSV", "/NH"],
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            reader = csv.reader(output.splitlines())
            seen_procs = set()

            for row in reader:
                if not row or len(row) < 4:
                    continue
                proc_name = row[0].strip().lower()
                session_num = row[3].strip()

                # Focus on interactive console session (user desktop session)
                if session_num == "1" and proc_name not in seen_procs:
                    seen_procs.add(proc_name)
                    if proc_name in KNOWN_TARGETS:
                        info = KNOWN_TARGETS[proc_name]
                        active_apps.append({
                            "process": proc_name,
                            "name": info["name"],
                            "category": info["category"],
                            "icon": info["icon"],
                            "running": True,
                        })

        except Exception as e:
            print("[YAMEEN] Scanner error:", e)

        return active_apps

    @staticmethod
    def get_active_devtools_ports() -> list:
        """Detects any running Electron apps exposing DevToolsActivePort."""
        appdata = os.environ.get("APPDATA", "")
        detected_ports = []
        
        candidates = ["Antigravity", "Claude", "ChatGPT", "Cursor", "Code"]
        for c in candidates:
            port_file = os.path.join(appdata, c, "DevToolsActivePort")
            if os.path.exists(port_file):
                try:
                    with open(port_file, "r", encoding="utf-8") as f:
                        port = f.readline().strip()
                        detected_ports.append({"app": c, "port": port})
                except Exception:
                    pass
                    
        return detected_ports

    @classmethod
    def inject_rtl_to_all_active(cls, remove: bool = False) -> int:
        """Injects RTL rule into all discoverable DevTools ports."""
        if not websocket:
            return 0

        ports = cls.get_active_devtools_ports()
        injected = 0

        for p in ports:
            port = p["port"]
            try:
                req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=2)
                pages = json.loads(req.read().decode())

                js_code = f"""
                (function() {{
                    var existing = document.getElementById('yameen-rtl-style');
                    if ({'true' if remove else 'false'}) {{
                        if (existing) existing.remove();
                        return 'Removed';
                    }}
                    if (!existing) {{
                        existing = document.createElement('style');
                        existing.id = 'yameen-rtl-style';
                        document.head.appendChild(existing);
                    }}
                    existing.textContent = `{RTL_CSS_RULE}`;
                    return 'Injected';
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
                        injected += 1
                    except Exception:
                        pass
            except Exception:
                pass

        return injected
