# -*- coding: utf-8 -*-
"""
YAMEEN - Electron & AI Desktop App Live Patcher
محقن الأنماط التلقائي لتطبيقات الذكاء الاصطناعي (Antigravity, Claude, ChatGPT)
"""

import os
import json
import urllib.request
from pathlib import Path

try:
    import websocket
except ImportError:
    websocket = None

RTL_CSS_RULE = (
    "* { unicode-bidi: plaintext !important; } "
    "div, p, li, span, blockquote, [contenteditable='true'], textarea, [class*='markdown'], [class*='message'] { "
    "direction: auto !important; text-align: start !important; }"
)

class AppPatcher:
    """Manages detection and live RTL style injection for desktop AI apps."""

    @staticmethod
    def get_supported_apps():
        """Scans system for AI applications and their live status."""
        appdata = os.environ.get("APPDATA", "")
        localappdata = os.environ.get("LOCALAPPDATA", "")
        
        apps = [
            {
                "id": "antigravity",
                "name": "Antigravity",
                "port_file": os.path.join(appdata, "Antigravity", "DevToolsActivePort"),
                "icon": "⚡",
                "installed": os.path.exists(os.path.join(localappdata, "Programs", "antigravity")),
            },
            {
                "id": "claude",
                "name": "Claude Desktop",
                "port_file": os.path.join(appdata, "Claude", "DevToolsActivePort"),
                "icon": "🟣",
                "installed": os.path.exists(os.path.join(localappdata, "Programs", "Claude")) or 
                             os.path.exists(r"C:\Program Files\WindowsApps\Claude_6.28899.2.0_x64__pzs8sxrjxfjjc"),
            },
            {
                "id": "chatgpt",
                "name": "ChatGPT Desktop",
                "port_file": os.path.join(appdata, "ChatGPT", "DevToolsActivePort"),
                "icon": "🟢",
                "installed": os.path.exists(os.path.join(localappdata, "Programs", "ChatGPT")),
            }
        ]
        
        for app in apps:
            app["running"] = os.path.exists(app["port_file"])
            app["active_port"] = None
            if app["running"]:
                try:
                    with open(app["port_file"], "r", encoding="utf-8") as f:
                        app["active_port"] = f.readline().strip()
                except Exception:
                    pass

        return apps

    @staticmethod
    def inject_rtl_into_port(port: str, remove: bool = False) -> int:
        """Injects or removes YAMEEN RTL stylesheet via Chrome DevTools Protocol."""
        if not websocket or not port:
            return 0

        injected_count = 0
        try:
            req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=2)
            pages = json.loads(req.read().decode())

            js_code = f"""
            (function() {{
                var existing = document.getElementById('yameen-rtl-style');
                if ({'true' if remove else 'false'}) {{
                    if (existing) existing.remove();
                    return 'YAMEEN: Removed';
                }}
                if (!existing) {{
                    existing = document.createElement('style');
                    existing.id = 'yameen-rtl-style';
                    document.head.appendChild(existing);
                }}
                existing.textContent = `{RTL_CSS_RULE}`;
                return 'YAMEEN: Active';
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
                    injected_count += 1
                except Exception:
                    pass

        except Exception:
            pass

        return injected_count

    @classmethod
    def patch_all_running(cls, remove: bool = False) -> dict:
        """Patches all currently running supported apps."""
        results = {}
        for app in cls.get_supported_apps():
            if app["running"] and app["active_port"]:
                count = cls.inject_rtl_into_port(app["active_port"], remove=remove)
                results[app["name"]] = count > 0
            else:
                results[app["name"]] = False
        return results
