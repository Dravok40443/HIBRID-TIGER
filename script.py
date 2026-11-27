import ctypes
import hashlib
import json
import math
import os
import random
import re
import shutil
import socket
import ssl
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

console = Console()
BASE_DIR = Path(__file__).resolve().parent
EXT_DIR = BASE_DIR / "external_tools"
DATA_DIR = BASE_DIR / "tiger_vault"
BASELINE_FILE = DATA_DIR / "baseline_hashes.json"

SCRIPT_VERSION = "v6.0-TIGER-WIN11"
TARGET_SYSTEM = "USER SYSTEM"
GITHUB_MAIN = "DRAVOK40443"
GITHUB_ALT = "ANONYMOUS40443"
TIKTOK_HANDLE = "DRAVOK67"

ANGEL_PALETTE = [
    "#ffffff",
    "#e0f7fa",
    "#bae6fd",
    "#7dd3fc",
    "#38bdf8",
    "#00e5ff",
    "#bae6fd",
    "#ffffff",
]

EVIL_PALETTE = [
    "#ff002b",
    "#ff2a55",
    "#ff4d6d",
    "#dc2626",
    "#b91c1c",
    "#ff1e42",
    "#ff5c77",
    "#ff002b",
]

SNOWMAN_ART = [
    """  CONTROL IS AN ILLUSION
                ⣴⠀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢾⣷⣿⣿⣿⣿⣿⠿⠟⠛⠉⠉⠉⠉⠉⠙⠳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⢿⡏⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡴⠒⠒⠒⠒⢢⣤⠀⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀
⠀⠀⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣷⣿⡆⠀⠀
⠀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⠀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⣤⣤⣄⣠⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠻⣿⣿⣄⠀⠀⠀⠀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⢹⡌⢻⣿⣦⣄⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣧⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⢹⣿⡇⢿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢹⣄⣀⣀⠈⠛⢻⣿⣿⣿⣿⡏⠀⠀⠀⣿⣿⠀⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣯⠉⠀⠀⠀⢸⣿⣿⣿⣿⣆⠀⠀⠀⢿⣿⡇⠸⣿⣿⣿⣿⣿⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢹⡆⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⠀⠀⠘⣿⡇⠀⢹⣿⣿⣿⣿⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⢹⣧⡀⠀⣿⣿⣿⣿⡿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠀⠀⢸⣿⣿⣿⣿⣿⣿⣧⠀⠀⣿⣿⣷⣄⢹⣿⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡄⠀⢿⣿⢿⡻⢝⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⠀⠐⠈⠁⠁⠀⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⢸⣿⡟⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠘⣿⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠟⠛⠛⠿⠿⠿⠿⠿⣿⣿⣿⣿⠿⠿⠿⢿⠿⠟⠛⠛⠃
"""      
]

ANGEL_BANNER = [
    "   █████╗ ███╗   ██╗ ██████╗ ███████╗██╗         ████████╗██╗ ██████╗ ███████╗██████╗ ",
    "  ██╔══██╗████╗  ██║██╔════╝ ██╔════╝██║         ╚══██╔══╝██║██╔════╝ ██╔════╝██╔══██╗",
    "  ███████║██╔██╗ ██║██║  ███╗█████╗  ██║            ██║   ██║██║  ███╗█████╗  ██████╔╝",
    "  ██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██║            ██║   ██║██║   ██║██╔══╝  ██╔══██╗",
    "  ██║  ██║██║ ╚████║╚██████╔╝███████╗███████╗       ██║   ██║╚██████╔╝███████╗██║  ██║",
    "  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝       ╚═╝   ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝",
]

EVIL_BANNER = [
    "  ███████╗██╗   ██╗██╗██╗         ████████╗██╗ ██████╗ ███████╗██████╗ ",
    "  ██╔════╝██║   ██║██║██║         ╚══██╔══╝██║██╔════╝ ██╔════╝██╔══██╗",
    "  █████╗  ██║   ██║██║██║            ██║   ██║██║  ███╗█████╗  ██████╔╝",
    "  ██╔══╝  ╚██╗ ██╔╝██║██║            ██║   ██║██║   ██║██╔══╝  ██╔══██╗",
    "  ███████╗ ╚████╔╝ ██║███████╗       ██║   ██║╚██████╔╝███████╗██║  ██║",
    "  ╚══════╝  ╚═══╝  ╚═╝╚══════╝       ╚═╝   ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝",
]

# Catálogo expandido de OSINT & Reconhecimento Passivo (GitHub)
OSINT_CATALOG = {
    "1": {
        "name": "holehe",
        "category": "Email OSINT",
        "repo": "https://github.com/megadose/holehe.git",
        "folder": "holehe",
        "entry": ["holehe", "holehe.exe"],
        "fallback_py": "holehe/__main__.py",
    },
    "2": {
        "name": "h8mail",
        "category": "Breach Check",
        "repo": "https://github.com/khast3x/h8mail.git",
        "folder": "h8mail",
        "entry": ["h8mail", "h8mail.exe"],
        "fallback_py": "h8mail/__main__.py",
    },
    "3": {
        "name": "sherlock",
        "category": "Username OSINT",
        "repo": "https://github.com/sherlock-project/sherlock.git",
        "folder": "sherlock",
        "entry": ["sherlock", "sherlock.exe"],
        "fallback_py": "sherlock_project/sherlock.py",
    },
    "4": {
        "name": "maigret",
        "category": "Deep Profile",
        "repo": "https://github.com/soxoj/maigret.git",
        "folder": "maigret",
        "entry": ["maigret", "maigret.exe"],
        "fallback_py": "maigret.py",
    },
    "5": {
        "name": "blackbird",
        "category": "User & Email",
        "repo": "https://github.com/p1ngul1n0/blackbird.git",
        "folder": "blackbird",
        "entry": ["blackbird", "blackbird.exe"],
        "fallback_py": "blackbird.py",
    },
    "6": {
        "name": "social-analyzer",
        "category": "Social Graph",
        "repo": "https://github.com/qeeqez/social-analyzer.git",
        "folder": "social-analyzer",
        "entry": ["social-analyzer", "social-analyzer.exe"],
        "fallback_py": "social_analyzer/social_analyzer.py",
    },
    "7": {
        "name": "instaloader",
        "category": "Social Archive",
        "repo": "https://github.com/instaloader/instaloader.git",
        "folder": "instaloader",
        "entry": ["instaloader", "instaloader.exe"],
        "fallback_py": None,
    },
    "8": {
        "name": "exiftool",
        "category": "File Metadata",
        "repo": "https://github.com/exiftool/exiftool.git",
        "folder": "exiftool",
        "entry": ["exiftool", "exiftool.exe"],
        "fallback_py": None,
    },
    "9": {
        "name": "theHarvester",
        "category": "Domain OSINT",
        "repo": "https://github.com/laramies/theHarvester.git",
        "folder": "theHarvester",
        "entry": ["theHarvester", "theHarvester.exe"],
        "fallback_py": "theHarvester.py",
    },
    "10": {
        "name": "Sublist3r",
        "category": "Subdomains",
        "repo": "https://github.com/aboul3la/Sublist3r.git",
        "folder": "Sublist3r",
        "entry": ["sublist3r", "sublist3r.exe"],
        "fallback_py": "sublist3r.py",
    },
    "11": {
        "name": "wafw00f",
        "category": "WAF Detector",
        "repo": "https://github.com/EnableSecurity/wafw00f.git",
        "folder": "wafw00f",
        "entry": ["wafw00f", "wafw00f.exe"],
        "fallback_py": "wafw00f/main.py",
    },
    "12": {
        "name": "dnsrecon",
        "category": "DNS Enum",
        "repo": "https://github.com/darkoperator/dnsrecon.git",
        "folder": "dnsrecon",
        "entry": ["dnsrecon", "dnsrecon.exe"],
        "fallback_py": "dnsrecon.py",
    },
    "13": {
        "name": "PhotoForensics + pHash",
        "category": "Image Forensics",
        "repo": None,
        "folder": None,
        "entry": ["__NATIVE__"],
        "fallback_py": None,
    },
}

OUI_HINTS = {
    "00:50:56": "VMware",
    "08:00:27": "VirtualBox",
    "B8:27:EB": "Raspberry Pi",
    "DC:A6:32": "Raspberry Pi",
    "3C:5A:B4": "Google",
    "F4:F5:D8": "Google",
    "00:1A:2B": "Cisco",
    "C0:25:E9": "TP-Link",
    "50:C7:BF": "TP-Link",
    "18:D6:C7": "TP-Link",
}

COMMON_PORTS = [21, 22, 23, 53, 80, 135, 139, 443, 445, 554, 8080, 8443]
RISKY_PORTS = {21, 23, 135, 139, 445, 554, 8080}

# Padrões heurísticos para o Antivírus Próprio
SUSPICIOUS_PATTERNS = [
    (re.compile(rb"powershell.*-enc", re.I), "Encoded PowerShell command"),
    (re.compile(rb"Invoke-Expression|IEX\s*\(", re.I), "Dynamic script execution (IEX)"),
    (re.compile(rb"DownloadString|DownloadFile|BitsTransfer", re.I), "Remote payload download pattern"),
    (re.compile(rb"Set-MpPreference.*DisableRealtimeMonitoring", re.I), "Attempt to disable Windows Defender"),
    (re.compile(rb"vssadmin.*delete\s+shadows", re.I), "Shadow copy deletion pattern (Ransomware indicator)"),
    (re.compile(rb"reg\s+add.*CurrentVersion\\Run", re.I), "Registry Run key persistence"),
    (re.compile(rb"schtasks\s+/create", re.I), "Scheduled task creation"),
    (re.compile(rb"VirtualAlloc|WriteProcessMemory|CreateRemoteThread", re.I), "Process injection Win32 API strings"),
]


class UIState:
    def __init__(self) -> None:
        self.tick = 0
        self.evil_mode = False

    @property
    def palette(self) -> list[str]:
        return EVIL_PALETTE if self.evil_mode else ANGEL_PALETTE

    @property
    def primary(self) -> str:
        return self.palette[self.tick % len(self.palette)]

    @property
    def secondary(self) -> str:
        return self.palette[(self.tick + 2) % len(self.palette)]

    @property
    def border(self) -> str:
        return "#ff002b" if self.evil_mode else "#7dd3fc"

    def step(self, n: int = 1) -> None:
        self.tick = (self.tick + n) % len(self.palette)

    def paint_lines(self, lines: list[str], offset: int = 0) -> Text:
        txt = Text()
        pal = self.palette
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch == " ":
                    txt.append(" ")
                else:
                    col = pal[(self.tick + r + (c // 3) + offset) % len(pal)]
                    txt.append(ch, style=f"bold {col}")
            if r < len(lines) - 1:
                txt.append("\n")
        return txt

    def pulse_bar(self, width: int = 72) -> Text:
        w = max(40, min(width, console.size.width - 4))
        txt = Text()
        pal = self.palette
        glyphs = ["|", ":", ".", "v", "*"] if self.evil_mode else ["*", "+", "~", ".", "o"]
        for row in range(2):
            for col in range(w):
                seed = (col * 5 + row * 9 + self.tick * 4) % 13
                if seed < 4:
                    g = glyphs[(col + row + self.tick) % len(glyphs)]
                    col_hex = pal[(col + self.tick + row) % len(pal)]
                    txt.append(g, style=f"bold {col_hex}")
                else:
                    txt.append(" ")
            if row == 0:
                txt.append("\n")
        return txt


state = UIState()


def ask_clean(prompt_label: str, choices: list[str] | None = None, default: str = "") -> str:
    return Prompt.ask(
        f"[bold {state.secondary}]{prompt_label}[/]",
        choices=choices,
        default=default,
        show_choices=False,
    ).strip()


def hard_clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def is_admin_os() -> bool:
    if os.name != "nt":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def run_ps(cmd: str, timeout: int = 35) -> str:
    full = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd]
    proc = subprocess.run(full, capture_output=True, text=True, timeout=timeout, errors="replace")
    return (proc.stdout or proc.stderr or "").strip()


def pause() -> None:
    ask_clean("Press Enter to continue", default="")


# =====================================================================
# ANIMAÇÕES
# =====================================================================
def angel_boot_animation() -> None:
    if not console.is_terminal:
        return
    messages = [
        "Igniting Angel Tiger frost core...",
        "Loading Antivirus & Heuristic engine...",
        "Calibrating Windows De-Bloat & Scanner...",
        "Ready.",
    ]
    w, h = 64, 5
    flakes = [[random.randint(0, w - 1), random.randint(0, h - 1), random.choice(["*", "+", ".", "~"])] for _ in range(24)]
    with Live(console=console, refresh_per_second=14, transient=True) as live:
        for step in range(18):
            state.step(1)
            msg = messages[min(len(messages) - 1, (step * len(messages)) // 18)]
            pct = int(((step + 1) / 18) * 100)
            bar_n = int((pct / 100) * 32)
            bar = f"[{'#' * bar_n}{'-' * (32 - bar_n)}] {pct}%"

            grid = [[" " for _ in range(w)] for _ in range(h)]
            for fl in flakes:
                grid[fl[1]][fl[0]] = fl[2]
                fl[1] = (fl[1] + 1) % h
                fl[0] = (fl[0] + random.choice([-1, 0, 1])) % w

            snow = Text()
            for r in range(h):
                for c in range(w):
                    ch = grid[r][c]
                    snow.append(" " if ch == " " else ch, style="bold #ffffff" if ch in ("*", "+") else "bold #7dd3fc")
                snow.append("\n")

            body = Text()
            body.append_text(snow)
            body.append_text(state.paint_lines(SNOWMAN_ART, offset=step))
            body.append("\n")
            body.append_text(state.paint_lines(ANGEL_BANNER, offset=step + 2))
            body.append(f"\n\n  {msg}\n  {bar}", style=f"bold {state.secondary}")
            live.update(Align.center(Panel(body, border_style="#7dd3fc", box=box.DOUBLE, padding=(1, 2))))
            time.sleep(0.08)


def switch_to_evil_animation() -> None:
    if not console.is_terminal:
        state.evil_mode = True
        return

    shrapnel = ["#", "*", "X", "!", "/", "\\", "+", "%", "@"]
    with Live(console=console, refresh_per_second=16, transient=True) as live:
        for f in range(7):
            chaos = Text()
            for _ in range(6):
                row_c = [random.choice(shrapnel) if random.random() < (0.18 + f * 0.09) else " " for _ in range(62)]
                chaos.append("".join(row_c) + "\n", style="bold #ff2a55" if f < 4 else "bold #ff002b")
            chaos.append("\n  >>> SHATTERING ANGEL INTERFACE <<<", style="bold #ffffff")
            live.update(Align.center(Panel(chaos, border_style="#ff002b", box=box.HEAVY)))
            time.sleep(0.07)

        for f in range(5):
            blast = Text()
            radius = f + 2
            for r in range(8):
                row_s = []
                for c in range(62):
                    dist = abs(r - 4) * 3 + abs(c - 31) // 2
                    row_s.append(random.choice(["*", "#", "@", "+", "X"]) if dist <= radius * 3 else " ")
                blast.append("".join(row_s) + "\n", style="bold #ff002b" if f % 2 == 0 else "bold #ff4d6d")
            blast.append(f"\n  *** EVIL CORE IGNITION [{min(100, (f + 1) * 20)}%] ***", style="bold #ffffff")
            live.update(Align.center(Panel(blast, border_style="#ff002b", box=box.DOUBLE)))
            time.sleep(0.07)

        state.evil_mode = True
        for f in range(7):
            state.step(1)
            recon = Text()
            recon.append_text(state.paint_lines(EVIL_BANNER, offset=f))
            recon.append(f"\n\n  Rebuilding EVIL TIGER... {min(100, (f + 1) * 15)}%", style="bold #ff4d6d")
            live.update(Align.center(Panel(recon, border_style="#ff002b", box=box.DOUBLE, padding=(1, 2))))
            time.sleep(0.07)


def switch_to_angel_animation() -> None:
    if not console.is_terminal:
        state.evil_mode = False
        return

    with Live(console=console, refresh_per_second=16, transient=True) as live:
        for f in range(6):
            freeze = Text()
            for _ in range(6):
                row_c = [random.choice(["*", "+", "~", "."]) if random.random() < (0.20 + f * 0.1) else " " for _ in range(62)]
                freeze.append("".join(row_c) + "\n", style="bold #7dd3fc" if f % 2 == 0 else "bold #ffffff")
            freeze.append("\n  >>> FREEZING EVIL CORE <<<", style="bold #e0f7fa")
            live.update(Align.center(Panel(freeze, border_style="#38bdf8", box=box.HEAVY)))
            time.sleep(0.07)

        state.evil_mode = False
        for f in range(7):
            state.step(1)
            recon = Text()
            recon.append_text(state.paint_lines(SNOWMAN_ART, offset=f))
            recon.append("\n")
            recon.append_text(state.paint_lines(ANGEL_BANNER, offset=f))
            recon.append(f"\n\n  Restoring ANGEL TIGER... {min(100, (f + 1) * 15)}%", style="bold #7dd3fc")
            live.update(Align.center(Panel(recon, border_style="#7dd3fc", box=box.DOUBLE, padding=(1, 2))))
            time.sleep(0.07)


def exit_animation() -> None:
    if not console.is_terminal:
        return
    with Live(console=console, refresh_per_second=14, transient=True) as live:
        for i in range(9):
            state.step(1)
            txt = Text()
            txt.append_text(state.paint_lines(SNOWMAN_ART, offset=i))
            txt.append(f"\n  Closing session... {(i + 1) * 11}%", style=f"bold {state.primary}")
            live.update(Align.center(Panel(txt, border_style=state.border, box=box.ROUNDED)))
            time.sleep(0.07)


def render_header() -> None:
    hard_clear()
    state.step(1)
    mode_tag = "[bold #ffffff on #b91c1c] ADMIN MODE [/]" if state.evil_mode else "[bold #0f172a on #bae6fd] USER MODE [/]"

    top = Text()
    if not state.evil_mode:
        top.append_text(state.paint_lines(SNOWMAN_ART, offset=0))
        top.append("\n")
    top.append_text(state.paint_lines(EVIL_BANNER if state.evil_mode else ANGEL_BANNER, offset=2))

    console.print(Align.center(top))
    console.print(
        Align.center(
            f"[bold {state.secondary}]Ver:[/] [bold #ffffff]{SCRIPT_VERSION}[/]  |  "
            f"[bold {state.secondary}]Target:[/] [bold #ffffff]{TARGET_SYSTEM}[/]  |  "
            f"{mode_tag}"
        )
    )
    console.print(
        Align.center(
            f"[bold {state.primary}]DEVELOPER {GITHUB_MAIN} ON GITHUB[/]  |  "
            f"[bold {state.primary}]ALT: {GITHUB_ALT}[/]  |  "
            f"[bold {state.primary}]{TIKTOK_HANDLE} ON TIK TOK[/]"
        )
    )
    console.print(Align.center(state.pulse_bar(76)))
    console.print(Rule(style=state.border))


# =====================================================================
# AUTO-INSTALADOR DE DEPENDÊNCIAS & CATÁLOGO OSINT
# =====================================================================
def resolve_osint_tool(tool_key: str) -> list[str] | None:
    spec = OSINT_CATALOG[tool_key]
    if spec["entry"] == ["__NATIVE__"]:
        return ["__NATIVE__"]

    for bin_name in spec["entry"]:
        found = shutil.which(bin_name)
        if found:
            return [found]

    scripts_dir = Path(sys.executable).resolve().parent / "Scripts"
    for bin_name in spec["entry"]:
        cand = scripts_dir / bin_name
        if cand.exists():
            return [str(cand)]

    folder = spec.get("folder")
    fallback = spec.get("fallback_py")
    if folder and fallback:
        script_p = EXT_DIR / folder / fallback
        if script_p.exists():
            return [sys.executable, str(script_p)]

    return None


def module_auto_installer() -> None:
    render_header()
    EXT_DIR.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str]] = []

    with console.status(f"[bold {state.secondary}]Installing Python libraries (rich, pillow, imagehash)...[/]", spinner="dots"):
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", "rich", "pillow", "imagehash"],
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
    results.append(("Python Core Libs", "READY"))

    git_bin = shutil.which("git")
    if not git_bin:
        results.append(("Git Binary", "NO (Install Git)"))
    else:
        for key, spec in OSINT_CATALOG.items():
            if spec["entry"] == ["__NATIVE__"]:
                results.append((spec["name"], "READY"))
                continue

            if resolve_osint_tool(key):
                results.append((spec["name"], "READY"))
                continue

            target_dir = EXT_DIR / spec["folder"]
            repo = spec["repo"]
            with console.status(f"[bold {state.secondary}]Installing {spec['name']}...[/]", spinner="dots"):
                try:
                    if not target_dir.exists() and repo:
                        subprocess.run(
                            [git_bin, "clone", "--depth", "1", repo, str(target_dir)],
                            capture_output=True,
                            text=True,
                            timeout=90,
                            check=True,
                        )
                    req_f = target_dir / "requirements.txt"
                    if req_f.exists():
                        subprocess.run(
                            [sys.executable, "-m", "pip", "install", "--quiet", "-r", str(req_f)],
                            capture_output=True,
                            text=True,
                            timeout=240,
                            check=False,
                        )
                    elif (target_dir / "pyproject.toml").exists() or (target_dir / "setup.py").exists():
                        subprocess.run(
                            [sys.executable, "-m", "pip", "install", "--quiet", str(target_dir)],
                            capture_output=True,
                            text=True,
                            timeout=240,
                            check=False,
                        )
                except Exception:
                    pass

            st = "READY" if resolve_osint_tool(key) else "NO"
            results.append((spec["name"], st))

    tbl = Table(title="DEPENDENCY & OSINT INSTALLER", box=box.ROUNDED, border_style=state.border, expand=False)
    tbl.add_column("Component", style="bold #ffffff", width=28)
    tbl.add_column("Status", justify="center", width=18)
    for comp, status in results:
        st_fmt = "[bold #00ff66]READY[/]" if status == "READY" else f"[bold #ff002b]{status}[/]"
        tbl.add_row(comp, st_fmt)
    console.print(Align.center(tbl))
    pause()


# =====================================================================
# MÓDULO ANTIVÍRUS PRÓPRIO & SCANNER HEURÍSTICO (ANGEL TIGER)
# =====================================================================
def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    length = len(data)
    ent = 0.0
    for count in freq:
        if count:
            p = count / length
            ent -= p * math.log2(p)
    return ent


def analyze_file_heuristics(file_path: Path) -> dict[str, str]:
    risk_score = 0
    reasons: list[str] = []

    name_lower = file_path.name.lower()
    if re.search(r"\.(pdf|jpg|jpeg|png|docx|xlsx|txt|mp4)\.(exe|scr|bat|cmd|ps1|vbs|js)$", name_lower):
        risk_score += 50
        reasons.append("Double extension disguise")

    try:
        size = file_path.stat().st_size
        with file_path.open("rb") as f:
            sample = f.read(512 * 1024)
    except OSError as exc:
        return {"file": str(file_path), "verdict": "UNREADABLE", "score": "0", "details": str(exc)}

    ent = shannon_entropy(sample)
    if ent > 7.35 and file_path.suffix.lower() in (".exe", ".dll", ".scr", ".sys", ".bin"):
        risk_score += 30
        reasons.append(f"High entropy ({ent:.2f}) - packed/encrypted")

    for rx, desc in SUSPICIOUS_PATTERNS:
        if rx.search(sample):
            risk_score += 25
            reasons.append(desc)

    if size == 0:
        reasons.append("Zero-byte file")

    if risk_score >= 50:
        verdict = "HIGH RISK"
    elif risk_score >= 25:
        verdict = "SUSPICIOUS"
    else:
        verdict = "CLEAN"

    return {
        "file": file_path.name,
        "verdict": verdict,
        "score": str(risk_score),
        "details": "; ".join(reasons) if reasons else f"Entropy {ent:.2f} | No heuristic flags",
    }


def module_custom_antivirus() -> None:
    render_header()
    console.print(f"[bold {state.secondary}][1][/] Scan File or Folder (Heuristic + Entropy + Signatures)")
    console.print(f"[bold {state.secondary}][2][/] Hunt Unsigned Processes in Temp / User Folders")
    console.print(f"[bold {state.secondary}][3][/] Trigger Windows Defender Quick Scan")
    console.print(f"[bold {state.secondary}][0][/] Back\n")
    op = ask_clean("Select", choices=["1", "2", "3", "0"], default="1")
    if op == "0":
        return

    if op == "1":
        raw_p = ask_clean("Target file or folder path")
        target = Path(raw_p.strip('"').strip("'")).expanduser()
        if not target.exists():
            console.print(f"[bold {state.primary}]Path not found.[/]")
            pause()
            return

        files_to_scan = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()][:150]
        findings: list[dict[str, str]] = []
        with console.status(f"[bold {state.secondary}]Scanning {len(files_to_scan)} file(s)...[/]", spinner="dots"):
            for fp in files_to_scan:
                res = analyze_file_heuristics(fp)
                if target.is_file() or res["verdict"] != "CLEAN":
                    findings.append(res)

        tbl = Table(title=f"ANGEL TIGER AV SCAN ({len(files_to_scan)} FILES)", box=box.ROUNDED, border_style=state.border, expand=False)
        tbl.add_column("File", style="bold #ffffff", width=24)
        tbl.add_column("Verdict", justify="center", width=13)
        tbl.add_column("Score", justify="right", width=7)
        tbl.add_column("Analysis", style="#e0f7fa", width=36)

        if not findings:
            tbl.add_row("All scanned files", "[bold #00ff66]CLEAN[/]", "0", "No suspicious patterns found")
        else:
            for item in findings[:25]:
                v = item["verdict"]
                v_fmt = f"[bold #ff002b]{v}[/]" if v == "HIGH RISK" else (f"[bold #ffd166]{v}[/]" if v == "SUSPICIOUS" else f"[bold #00ff66]{v}[/]")
                tbl.add_row(item["file"][:24], v_fmt, item["score"], item["details"][:36])

        console.print(Align.center(tbl))
        pause()
        return

    if op == "2":
        ps_proc = (
            "Get-Process | Where-Object { $_.Path -and ($_.Path -match '\\\\Temp\\\\|\\\\AppData\\\\|\\\\Users\\\\Public\\\\|\\\\Downloads\\\\') } | "
            "Select-Object -First 20 Id,ProcessName,Path | ForEach-Object { "
            "$sig = (Get-AuthenticodeSignature $_.Path).Status; "
            "[PSCustomObject]@{PID=$_.Id;Name=$_.ProcessName;Sig=$sig;Path=$_.Path} } | ConvertTo-Json -Compress"
        )
        with console.status(f"[bold {state.secondary}]Inspecting running processes in user/temp paths...[/]", spinner="dots"):
            raw = run_ps(ps_proc)

        tbl = Table(title="PROCESS HUNTER (TEMP / APPDATA / PUBLIC)", box=box.ROUNDED, border_style=state.border, expand=False)
        tbl.add_column("PID", justify="right", width=7)
        tbl.add_column("Process", style="bold #ffffff", width=18)
        tbl.add_column("Signature", justify="center", width=13)
        tbl.add_column("Path", width=38)

        try:
            rows = json.loads(raw) if raw else []
            if isinstance(rows, dict):
                rows = [rows]
            for r in rows:
                s = str(r.get("Sig", "N/A"))
                s_fmt = f"[bold #00ff66]{s}[/]" if s == "Valid" else f"[bold #ff4d6d]{s}[/]"
                tbl.add_row(str(r.get("PID", "")), str(r.get("Name", "")), s_fmt, str(r.get("Path", ""))[:38])
            if not rows:
                tbl.add_row("-", "None detected", "[bold #00ff66]CLEAN[/]", "No user/temp processes running")
        except Exception as exc:
            tbl.add_row("-", "Error", "-", str(exc))

        console.print(Align.center(tbl))
        pause()
        return

    if op == "3":
        with console.status(f"[bold {state.secondary}]Running Windows Defender Quick Scan...[/]", spinner="dots"):
            out = run_ps("Start-MpScan -ScanType QuickScan; 'QuickScan completed.'", timeout=120)
        console.print(Align.center(Panel(f"[bold #00ff66]{out}[/]", border_style=state.border)))
        pause()


# =====================================================================
# OTIMIZADOR & DE-BLOAT SEGURO DO WINDOWS (ANGEL TIGER)
# =====================================================================
def module_windows_optimizer() -> None:
    render_header()
    console.print(f"[bold {state.secondary}][1][/] Clean Windows Temp, Prefetch & Thumbnail Cache")
    console.print(f"[bold {state.secondary}][2][/] Disable Telemetry, Copilot & Start Menu Ads (Policies)")
    console.print(f"[bold {state.secondary}][3][/] Flush DNS & Reset Network Stack")
    console.print(f"[bold {state.secondary}][4][/] Restore Default Telemetry Policies")
    console.print(f"[bold {state.secondary}][0][/] Back\n")
    op = ask_clean("Select", choices=["1", "2", "3", "4", "0"], default="0")
    if op == "0":
        return

    if op == "1":
        removed_count = 0
        freed_bytes = 0
        temp_dirs = [Path(os.environ.get("TEMP", "")), Path(r"C:\Windows\Temp")]
        with console.status(f"[bold {state.secondary}]Cleaning temporary files...[/]", spinner="dots"):
            for tdir in temp_dirs:
                if not tdir.exists():
                    continue
                for item in tdir.iterdir():
                    try:
                        if item.is_file():
                            sz = item.stat().st_size
                            item.unlink()
                            removed_count += 1
                            freed_bytes += sz
                        elif item.is_dir():
                            shutil.rmtree(item, ignore_errors=True)
                            removed_count += 1
                    except Exception:
                        continue
        mb = freed_bytes / (1024 * 1024)
        console.print(Align.center(Panel(f"Cleaned [bold #ffffff]{removed_count}[/] temp items (~{mb:.2f} MB freed).", border_style=state.border)))
        pause()
        return

    if op == "2":
        if not is_admin_os():
            console.print("[bold #ff4d6d]Run terminal as Administrator to apply system registry policies.[/]")
            pause()
            return
        ps_debloat = (
            "New-Item -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Force | Out-Null; "
            "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Name 'AllowTelemetry' -Type DWord -Value 0; "
            "New-Item -Path 'HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot' -Force | Out-Null; "
            "Set-ItemProperty -Path 'HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot' -Name 'TurnOffWindowsCopilot' -Type DWord -Value 1; "
            "New-Item -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager' -Force | Out-Null; "
            "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager' -Name 'SubscribedContent-338388Enabled' -Type DWord -Value 0; "
            "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager' -Name 'SystemPaneSuggestionsEnabled' -Type DWord -Value 0; "
            "Stop-Service -Name 'DiagTrack' -Force -ErrorAction SilentlyContinue; "
            "Set-Service -Name 'DiagTrack' -StartupType Disabled -ErrorAction SilentlyContinue; "
            "'Telemetry, Copilot policy, Start suggestions & DiagTrack disabled.'"
        )
        with console.status(f"[bold {state.secondary}]Applying Windows privacy & de-bloat policies...[/]", spinner="dots"):
            msg = run_ps(ps_debloat)
        console.print(Align.center(Panel(f"[bold #00ff66]{msg}[/]", border_style=state.border)))
        pause()
        return

    if op == "3":
        with console.status(f"[bold {state.secondary}]Flushing DNS cache...[/]", spinner="dots"):
            out = run_ps("ipconfig /flushdns")
        console.print(Align.center(Panel(out, border_style=state.border)))
        pause()
        return

    if op == "4":
        if not is_admin_os():
            console.print("[bold #ff4d6d]Run terminal as Administrator to restore policies.[/]")
            pause()
            return
        ps_restore = (
            "Remove-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Name 'AllowTelemetry' -ErrorAction SilentlyContinue; "
            "Remove-ItemProperty -Path 'HKCU:\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot' -Name 'TurnOffWindowsCopilot' -ErrorAction SilentlyContinue; "
            "Set-Service -Name 'DiagTrack' -StartupType Automatic -ErrorAction SilentlyContinue; "
            "'Default Windows policies restored.'"
        )
        with console.status(f"[bold {state.secondary}]Restoring default policies...[/]", spinner="dots"):
            msg = run_ps(ps_restore)
        console.print(Align.center(Panel(f"[bold #00ff66]{msg}[/]", border_style=state.border)))
        pause()


# =====================================================================
# MÓDULOS DE REDE, WEB POSTURE, WI-FI SCANNER & INTEGRIDADE
# =====================================================================
def normalize_domain(raw: str) -> str:
    c = re.sub(r"^https?://", "", raw.strip().lower())
    return c.split("/")[0].split(":")[0].strip()


def module_web_posture() -> None:
    render_header()
    domain = normalize_domain(ask_clean("Target domain (e.g. example.com)"))
    if not domain or "." not in domain:
        console.print(f"[bold {state.primary}]Invalid domain.[/]")
        pause()
        return

    score = 0
    rows: list[tuple[str, str]] = []
    with console.status(f"[bold {state.secondary}]Checking DNS, TLS and security headers...[/]", spinner="dots"):
        try:
            ip = socket.gethostbyname(domain)
            rows.append(("DNS IPv4", ip))
            score += 1
        except socket.gaierror:
            rows.append(("DNS IPv4", "Failed"))

        hdrs: dict[str, str] = {}
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(f"https://{domain}", headers={"User-Agent": "AngelTiger/6.0"})
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                hdrs = {k.lower(): v for k, v in resp.headers.items()}
                rows.append(("HTTPS / TLS", f"Active (HTTP {resp.status})"))
                score += 1
        except Exception as exc:
            rows.append(("HTTPS / TLS", f"Unavailable ({type(exc).__name__})"))

        sec = ["strict-transport-security", "content-security-policy", "x-frame-options", "x-content-type-options"]
        found = [h for h in sec if h in hdrs]
        if len(found) >= 3:
            score += 2
        elif len(found) >= 1:
            score += 1
        rows.append(("Security Headers", f"{len(found)}/4 ({', '.join(found) or 'none'})"))

        srv = hdrs.get("server", "Hidden")
        edge = any(k in hdrs for k in ("cf-ray", "via")) or any(x in srv.lower() for x in ("cloudflare", "akamai", "fastly"))
        if edge:
            score += 1
        rows.append(("Edge / CDN", f"{'Yes' if edge else 'No'} ({srv})"))

    stars = max(1, min(5, score))
    star_str = "*" * stars + "-" * (5 - stars)
    rows.append(("Security Rating", f"{star_str} ({stars}/5)"))

    tbl = Table(title=f"WEB POSTURE - {domain.upper()}", box=box.ROUNDED, border_style=state.border, expand=False)
    tbl.add_column("Check", style=f"bold {state.secondary}", width=22)
    tbl.add_column("Result", style="bold #ffffff", width=44)
    for k, v in rows:
        tbl.add_row(k, v)
    console.print(Align.center(tbl))
    pause()


def module_network_identity() -> None:
    render_header()
    local_ip = "N/A"
    mac = "N/A"
    pub_ip = "Unavailable"
    loc = "N/A"
    vpn = "Undetermined"

    with console.status(f"[bold {state.secondary}]Fetching IP, MAC, location and VPN status...[/]", spinner="dots"):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            pass

        try:
            out = subprocess.check_output(["getmac", "/fo", "csv", "/nh"], text=True, stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                parts = [p.strip('"') for p in line.split(",")]
                if len(parts) >= 2 and re.match(r"^([0-9A-Fa-f]{2}[-:]){5}[0-9A-Fa-f]{2}$", parts[1]):
                    mac = parts[1].upper()
                    break
        except Exception:
            pass

        try:
            with urllib.request.urlopen("https://ipwho.is/", timeout=7) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
                if data.get("success"):
                    pub_ip = str(data.get("ip", "N/A"))
                    loc = f"{data.get('city', '')}, {data.get('region', '')} - {data.get('country', '')}".strip(", -")
                    sec = data.get("security") or {}
                    is_vpn = bool(sec.get("vpn") or sec.get("proxy") or sec.get("tor") or sec.get("hosting"))
                    vpn = "Active (VPN / Proxy / Hosting)" if is_vpn else "Not detected"
        except Exception:
            pass

    tbl = Table(title="NETWORK IDENTITY", box=box.ROUNDED, border_style=state.border, expand=False)
    tbl.add_column("Field", style=f"bold {state.secondary}", width=22)
    tbl.add_column("Value", style="bold #ffffff", width=44)
    for k, v in [("Local IP", local_ip), ("MAC Address", mac), ("Public IP", pub_ip), ("Approx. Location", loc), ("VPN / Proxy", vpn)]:
        tbl.add_row(k, v)
    console.print(Align.center(tbl))
    pause()


def oui_hint(mac_norm: str) -> str:
    prefix = mac_norm.replace("-", ":")[:8].upper()
    if prefix in OUI_HINTS:
        return OUI_HINTS[prefix]
    if len(mac_norm) > 1 and mac_norm[1].upper() in ("2", "6", "A", "E"):
        return "Randomized MAC"
    return "LAN Host"


def get_lan_devices_and_gateway() -> tuple[str | None, list[dict[str, str]]]:
    gw_ip = None
    ps_gw = "(Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | Sort-Object RouteMetric | Select-Object -First 1).NextHop"
    out_gw = run_ps(ps_gw, timeout=10).strip()
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", out_gw):
        gw_ip = out_gw

    arp_raw = subprocess.check_output(["arp", "-a"], text=True, errors="replace")
    devices: list[dict[str, str]] = []
    seen = set()
    for line in arp_raw.splitlines():
        m = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})\s+(\w+)", line)
        if m:
            ip, mac_s, kind = m.group(1), m.group(2).upper().replace("-", ":"), m.group(3)
            if ip in seen or ip.endswith(".255"):
                continue
            seen.add(ip)
            role = "Router / Gateway" if ip == gw_ip else oui_hint(mac_s)
            devices.append({"ip": ip, "mac": mac_s, "type": kind, "device": role})
    return gw_ip, devices


def scan_tcp_ports(target_ip: str, ports: list[int], timeout: float = 0.25) -> list[tuple[int, str, str]]:
    results: list[tuple[int, str, str]] = []
    for p in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            code = sock.connect_ex((target_ip, p))
            if code == 0:
                risk = "HIGH RISK" if p in RISKY_PORTS else "REVIEW"
                results.append((p, "OPEN", risk))
            else:
                results.append((p, "CLOSED", "SAFE"))
        except Exception:
            results.append((p, "CLOSED", "SAFE"))
        finally:
            sock.close()
    return results


def module_scanner_wifi(show_scan_modes: bool = True) -> None:
    render_header()
    if show_scan_modes:
        console.print(f"[bold {state.secondary}][1][/] Wi-Fi Quick Scan")
        console.print(f"[bold {state.secondary}][2][/] Wi-Fi Deep Scan")
        console.print(f"[bold {state.secondary}][3][/] Port Scan (IP / MAC / Router)")
        console.print(f"[bold {state.secondary}][0][/] Back\n")
        mode = ask_clean("Select", choices=["1", "2", "3", "0"], default="1")
    else:
        console.print(f"[bold {state.secondary}][1][/] Wi-Fi Host Discovery")
        console.print(f"[bold {state.secondary}][2][/] Port Scan (IP / MAC / Router)")
        console.print(f"[bold {state.secondary}][0][/] Back\n")
        raw_m = ask_clean("Select", choices=["1", "2", "0"], default="1")
        mode = "1" if raw_m == "1" else ("3" if raw_m == "2" else "0")

    if mode == "0":
        return

    if mode in ("1", "2"):
        timeout_val = 0.15 if mode == "1" else 0.45
        ports_probe = [80, 443] if mode == "1" else [22, 80, 135, 443, 445, 8080]
        label_mode = "QUICK" if mode == "1" else "DEEP"

        with console.status(f"[bold {state.secondary}]Scanning Wi-Fi network ({label_mode})...[/]", spinner="dots"):
            gw_ip, devs = get_lan_devices_and_gateway()
            enriched = []
            for d in devs:
                open_p = [str(p) for p, st, _ in scan_tcp_ports(d["ip"], ports_probe, timeout=timeout_val) if st == "OPEN"]
                d_copy = dict(d)
                d_copy["open_ports"] = ", ".join(open_p) if open_p else "None"
                enriched.append(d_copy)

        tbl = Table(title=f"WI-FI SCANNER ({label_mode}) - GW: {gw_ip or 'N/A'}", box=box.ROUNDED, border_style=state.border, expand=False)
        tbl.add_column("IP", style=f"bold {state.secondary}", width=16)
        tbl.add_column("MAC Address", style="bold #ffffff", width=19)
        tbl.add_column("Device", style="white", width=20)
        tbl.add_column("Open Ports", style=f"bold {state.primary}", width=20)
        for item in enriched:
            tbl.add_row(item["ip"], item["mac"], item["device"], item["open_ports"])
        console.print(Align.center(tbl))
        pause()
        return

    if mode == "3":
        gw_ip, devs = get_lan_devices_and_gateway()
        print("\n[1] Scan Router / Gateway" + (f" ({gw_ip})" if gw_ip else ""))
        print("[2] Pick IP from network")
        sub = ask_clean("Select", choices=["1", "2"], default="1")

        target_ip = gw_ip
        target_mac = "N/A"
        target_label = "Router"
        for d in devs:
            if d["ip"] == gw_ip:
                target_mac = d["mac"]
                target_label = d["device"]

        if sub == "2" or not target_ip:
            tbl_d = Table(title="LAN DEVICES", box=box.ROUNDED, border_style=state.border, expand=False)
            tbl_d.add_column("ID", justify="center", width=5)
            tbl_d.add_column("IP", width=16)
            tbl_d.add_column("MAC", width=19)
            tbl_d.add_column("Device", width=20)
            for idx, d in enumerate(devs, 1):
                tbl_d.add_row(str(idx), d["ip"], d["mac"], d["device"])
            console.print(Align.center(tbl_d))
            typed = ask_clean("Target IP")
            if not re.match(r"^\d+\.\d+\.\d+\.\d+$", typed):
                console.print(f"[bold {state.primary}]Invalid IP.[/]")
                pause()
                return
            target_ip = typed
            for d in devs:
                if d["ip"] == target_ip:
                    target_mac = d["mac"]
                    target_label = d["device"]

        with console.status(f"[bold {state.secondary}]Scanning ports on {target_ip}...[/]", spinner="dots"):
            port_res = scan_tcp_ports(target_ip, COMMON_PORTS, timeout=0.3)

        tbl_p = Table(
            title=f"PORTS - {target_label.upper()} | IP: {target_ip} | MAC: {target_mac}",
            box=box.ROUNDED,
            border_style=state.border,
            expand=False,
        )
        tbl_p.add_column("Port", justify="center", style=f"bold {state.secondary}", width=8)
        tbl_p.add_column("Device", style="bold #ffffff", width=18)
        tbl_p.add_column("IP / MAC", style="white", width=33)
        tbl_p.add_column("State", justify="center", width=10)
        tbl_p.add_column("Risk", justify="center", width=12)

        for p, st, risk in port_res:
            st_col = f"bold {state.primary}" if st == "OPEN" else "#bae6fd"
            rk_col = "bold #ff5555" if risk == "HIGH RISK" else ("bold #ffd166" if risk == "REVIEW" else "bold #7dd3fc")
            tbl_p.add_row(str(p), target_label, f"{target_ip} / {target_mac}", f"[{st_col}]{st}[/]", f"[{rk_col}]{risk}[/]")

        console.print(Align.center(tbl_p))
        pause()


def module_persistence_and_shield() -> None:
    render_header()
    ps_code = (
        "$mp = Get-MpComputerStatus -ErrorAction SilentlyContinue; "
        "$fw = Get-NetFirewallProfile -ErrorAction SilentlyContinue; "
        "$runs = @(); "
        "foreach ($k in @('HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run','HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run')) { "
        "  if (Test-Path $k) { "
        "    foreach ($p in (Get-ItemProperty -Path $k).PSObject.Properties) { "
        "      if ($p.Name -notlike 'PS*') { $runs += \"$($p.Name): $($p.Value)\" } "
        "    } "
        "  } "
        "}; "
        "[PSCustomObject]@{"
        "Defender=if ($mp) { $mp.RealTimeProtectionEnabled } else { 'N/A' };"
        "Firewall=(($fw | ForEach-Object { \"$($_.Name):$($_.Enabled)\" }) -join ' | ');"
        "RunCount=$runs.Count;"
        "RunSample=($runs | Select-Object -First 4) -join ' ; '"
        "} | ConvertTo-Json -Compress"
    )
    with console.status(f"[bold {state.secondary}]Checking shield and persistence entries...[/]", spinner="dots"):
        raw = run_ps(ps_code)

    tbl = Table(title="SHIELD & PERSISTENCE", box=box.ROUNDED, border_style=state.border, expand=False)
    tbl.add_column("Control", style=f"bold {state.secondary}", width=22)
    tbl.add_column("Status", style="bold #ffffff", width=46)
    try:
        d = json.loads(raw) if raw else {}
        for k, v in [("Defender Realtime", d.get("Defender", "N/A")), ("Firewall", d.get("Firewall", "N/A")), ("Run Keys Count", str(d.get("RunCount", 0))), ("Run Sample", str(d.get("RunSample", "-")))]:
            tbl.add_row(k, str(v))
    except Exception as exc:
        tbl.add_row("Error", str(exc))
    console.print(Align.center(tbl))
    pause()


def module_integrity_hash() -> None:
    render_header()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw_p = ask_clean("File or folder path")
    target = Path(raw_p.strip('"').strip("'")).expanduser()
    if not target.exists():
        console.print(f"[bold {state.primary}]Path not found.[/]")
        pause()
        return

    if target.is_file():
        h = hashlib.sha256(target.read_bytes()).hexdigest()
        console.print(Align.center(Panel(f"[bold #ffffff]{target}[/]\nSHA-256: [bold {state.secondary}]{h}[/]", border_style=state.border)))
        pause()
        return

    current = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.rglob("*")) if p.is_file()}
    if not BASELINE_FILE.exists():
        BASELINE_FILE.write_text(json.dumps({"hashes": current}, indent=2), encoding="utf-8")
        console.print(f"[bold {state.secondary}]Baseline created ({len(current)} files).[/]")
        pause()
        return

    old = json.loads(BASELINE_FILE.read_text(encoding="utf-8")).get("hashes", {})
    mod = [k for k in current if k in old and current[k] != old[k]]
    add = [k for k in current if k not in old]
    rem = [k for k in old if k not in current]
    tbl = Table(title="SHA-256 BASELINE", box=box.ROUNDED, border_style=state.border, expand=False)
    tbl.add_column("Change", style=f"bold {state.secondary}", width=14)
    tbl.add_column("Count", justify="right", width=8)
    tbl.add_column("Samples", width=42)
    tbl.add_row("Modified", str(len(mod)), ", ".join(mod[:3]) or "-")
    tbl.add_row("Added", str(len(add)), ", ".join(add[:3]) or "-")
    tbl.add_row("Removed", str(len(rem)), ", ".join(rem[:3]) or "-")
    console.print(Align.center(tbl))
    pause()


# =====================================================================
# RECONHECIMENTO PASSIVO & CATÁLOGO OSINT (EVIL TIGER)
# =====================================================================
def module_dns_whois_recon() -> None:
    render_header()
    domain = normalize_domain(ask_clean("Domain for DNS & Subdomain Recon (e.g. example.com)"))
    if not domain or "." not in domain:
        console.print(f"[bold {state.primary}]Invalid domain.[/]")
        pause()
        return

    ps_dns = (
        f"$recs = @(); "
        f"foreach ($t in @('A','AAAA','MX','NS','TXT')) {{ "
        f"  $r = Resolve-DnsName -Name '{domain}' -Type $t -ErrorAction SilentlyContinue; "
        f"  if ($r) {{ $recs += [PSCustomObject]@{{Type=$t;Data=(($r | ForEach-Object {{ $_.IPAddress + $_.NameExchange + $_.NameHost + ($_.Strings -join ' ') }}) -join ' | ')}} }} "
        f"}}; "
        f"$recs | ConvertTo-Json -Compress"
    )
    subs_found: list[str] = []
    with console.status(f"[bold {state.secondary}]Querying DNS records & Certificate Transparency (crt.sh)...[/]", spinner="dots"):
        raw_dns = run_ps(ps_dns, timeout=20)
        try:
            url = f"https://crt.sh/?q=%25.{domain}&output=json"
            req = urllib.request.Request(url, headers={"User-Agent": "EvilTiger-Recon/6.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                entries = json.loads(resp.read().decode("utf-8", errors="replace"))
                seen = set()
                for item in entries:
                    for name in str(item.get("name_value", "")).splitlines():
                        clean_n = name.strip().lower().lstrip("*.")
                        if clean_n.endswith(domain) and clean_n not in seen:
                            seen.add(clean_n)
                            subs_found.append(clean_n)
                        if len(subs_found) >= 15:
                            break
                    if len(subs_found) >= 15:
                        break
        except Exception:
            pass

    tbl = Table(title=f"PASSIVE DNS & CT SUBDOMAINS - {domain.upper()}", box=box.ROUNDED, border_style=state.border, expand=False)
    tbl.add_column("Type", style=f"bold {state.primary}", width=12)
    tbl.add_column("Record / Value", style="bold #ffffff", width=56)
    try:
        dns_rows = json.loads(raw_dns) if raw_dns else []
        if isinstance(dns_rows, dict):
            dns_rows = [dns_rows]
        for dr in dns_rows:
            tbl.add_row(str(dr.get("Type", "")), str(dr.get("Data", ""))[:90])
    except Exception:
        tbl.add_row("DNS", "No records returned")

    tbl.add_row("Subdomains", ", ".join(subs_found[:10]) if subs_found else "None returned from crt.sh")
    console.print(Align.center(tbl))
    pause()


def module_osint_suite() -> None:
    valid_ops = list(OSINT_CATALOG.keys()) + ["0"]
    while True:
        render_header()
        tbl = Table(title="MONSTER-OSINT SUITE (13 TOOLS)", box=box.ROUNDED, border_style=state.border, expand=False)
        tbl.add_column("Op", justify="center", style=f"bold {state.primary}", width=5)
        tbl.add_column("Tool", style="bold #ffffff", width=24)
        tbl.add_column("Category", style=state.secondary, width=18)
        tbl.add_column("Status", justify="center", width=10)

        for k, spec in OSINT_CATALOG.items():
            is_ready = resolve_osint_tool(k) is not None
            st_badge = "[bold #00ff66]READY[/]" if is_ready else "[bold #ff002b]NO[/]"
            tbl.add_row(k, spec["name"], spec["category"], st_badge)

        tbl.add_row("0", "Back", "Evil Tiger Menu", "-")
        console.print(Align.center(tbl))

        op = ask_clean("OSINT", choices=valid_ops, default="0")
        if op == "0":
            return

        cmd = resolve_osint_tool(op)
        spec = OSINT_CATALOG[op]
        if not cmd:
            console.print(f"[bold #ff002b]{spec['name']} is NO (not installed). Run option 1 in Angel Tiger first.[/]")
            pause()
            continue

        if cmd == ["__NATIVE__"]:
            p_raw = ask_clean("Image path")
            p = Path(p_raw.strip('"').strip("'")).expanduser()
            if not p.is_file():
                console.print("[bold #ff002b]File not found.[/]")
                pause()
                continue
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            extra_info = ""
            try:
                import imagehash
                from PIL import Image

                with Image.open(p) as im:
                    extra_info = f"\nDimensions: {im.width}x{im.height} ({im.format})\npHash: {imagehash.phash(im)}"
            except Exception:
                pass
            console.print(Align.center(Panel(f"File: {p}\nSize: {p.stat().st_size} B\nSHA-256: {digest}{extra_info}", border_style=state.border)))
            pause()
            continue

        target_val = ask_clean("Target (email / handle / domain / URL)")
        if not target_val:
            continue

        if op == "2":
            full_cmd = cmd + ["-t", target_val]
        elif op in ("3", "4", "7"):
            full_cmd = cmd + [target_val.lstrip("@")]
        elif op == "5":
            full_cmd = cmd + (["--email", target_val] if "@" in target_val else ["--username", target_val.lstrip("@")])
        elif op == "6":
            full_cmd = cmd + ["--username", target_val.lstrip("@")]
        elif op == "9":
            full_cmd = cmd + ["-d", target_val, "-b", "crtsh"]
        elif op == "10":
            full_cmd = cmd + ["-d", target_val]
        elif op == "12":
            full_cmd = cmd + ["-d", target_val]
        else:
            full_cmd = cmd + [target_val]

        subprocess.run(full_cmd, text=True, timeout=180)
        pause()


def admin_hub_menu() -> None:
    while True:
        render_header()
        tbl = Table(
            title="EVIL TIGER",
            box=box.ROUNDED,
            border_style="#ff002b",
            header_style="bold #ffffff",
            expand=False,
        )
        tbl.add_column("Op", justify="center", style="bold #ff4d6d", width=6)
        tbl.add_column("Module", style="bold #ffffff", width=36)

        tbl.add_row("1", "MONSTER-OSINT Suite (13 Tools)")
        tbl.add_row("2", "Wi-Fi & Port Scanner")
        tbl.add_row("3", "Passive DNS & CT Subdomains")
        tbl.add_row("4", "Web Posture & Headers Audit")
        tbl.add_row("5", "Custom AV & Heuristic Scanner")
        tbl.add_row("6", "Switch to Angel Tiger Mode")
        tbl.add_row("0", "Exit")
        console.print(Align.center(tbl))

        op = ask_clean("evil-tiger", choices=["1", "2", "3", "4", "5", "6", "0"], default="0")
        if op == "0":
            raise SystemExit(0)
        if op == "1":
            module_osint_suite()
        elif op == "2":
            module_scanner_wifi(show_scan_modes=False)
        elif op == "3":
            module_dns_whois_recon()
        elif op == "4":
            module_web_posture()
        elif op == "5":
            module_custom_antivirus()
        elif op == "6":
            switch_to_angel_animation()
            return


def main() -> None:
    angel_boot_animation()

    while True:
        render_header()
        tbl = Table(
            title="ANGEL TIGER",
            box=box.ROUNDED,
            border_style=state.border,
            header_style="bold #ffffff",
            expand=False,
        )
        tbl.add_column("Op", justify="center", style=f"bold {state.secondary}", width=6)
        tbl.add_column("Module", style="bold #ffffff", width=36)

        tbl.add_row("1", "Auto-Install Dependencies & OSINT")
        tbl.add_row("2", "Custom Antivirus & Process Hunter")
        tbl.add_row("3", "Windows De-Bloat & Optimizer")
        tbl.add_row("4", "Wi-Fi & Port Scanner")
        tbl.add_row("5", "Web Posture Audit")
        tbl.add_row("6", "IP, MAC & VPN")
        tbl.add_row("7", "Shield & Persistence")
        tbl.add_row("8", "SHA-256 Integrity")
        tbl.add_row("9", "Admin")
        tbl.add_row("0", "Exit")
        console.print(Align.center(tbl))

        choice = ask_clean("angel-tiger", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], default="0")
        if choice == "0":
            break
        if choice == "1":
            module_auto_installer()
        elif choice == "2":
            module_custom_antivirus()
        elif choice == "3":
            module_windows_optimizer()
        elif choice == "4":
            module_scanner_wifi(show_scan_modes=True)
        elif choice == "5":
            module_web_posture()
        elif choice == "6":
            module_network_identity()
        elif choice == "7":
            module_persistence_and_shield()
        elif choice == "8":
            module_integrity_hash()
        elif choice == "9":
            switch_to_evil_animation()
            admin_hub_menu()

    exit_animation()


if __name__ == "__main__":
    if sys.version_info < (3, 9):
        print("Python 3.9+ is required.")
        sys.exit(1)
    try:
        main()
    except SystemExit:
        exit_animation()