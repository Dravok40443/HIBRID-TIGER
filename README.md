# 🐯 HIBRID-TIGER

> **CONTROL IS AN ILLUSION**

Dual-mode Windows console toolkit for defensive triage, heuristic analysis, system optimization, and passive OSINT reconnaissance. Built in Python with **Rich** terminal animations and smooth mode switching between **ANGEL TIGER** and **EVIL TIGER**.

---

## 📌 Overview

- **Project:** `HIBRID-TIGER`
- **Primary Script:** `script.py`
- **Target OS:** Windows 10 / 11 (Python 3.9+)
- **Developer:** `Dravok40443`
- **Secondary GitHub:** `anonymous40443`
- **TikTok:** `dravok67`
- **Purpose:** Authorized laboratory research, diagnostics, and educational study

---

## ⚠️ Disclaimer

- **HIBRID-TIGER** is intended strictly for educational use, personal lab environments, and authorized security testing.
- You are responsible for ensuring you have explicit authorization before scanning or querying any network, domain, or target.
- Built for defensive triage, system maintenance, and passive OSINT workflows.

---

## 🌳 Features Tree

```text
├── ❄️ - ANGEL TIGER (Defense, Scanner & System Optimizer)
│   ├── Auto-Install Dependencies & OSINT
│   │   ├── Installs Python packages (rich, pillow, imagehash)
│   │   └── Clones & prepares MONSTER-OSINT tools into external_tools/
│   ├── Custom Antivirus & Process Hunter
│   │   ├── File & folder heuristic scan (entropy, double extensions, suspicious strings)
│   │   ├── Process hunter in Temp / AppData / Public / Downloads + signature check
│   │   └── Windows Defender Quick Scan trigger
│   ├── Windows De-Bloat & Optimizer
│   │   ├── Clean Temp & temporary files
│   │   ├── Disable telemetry, Copilot policy & Start suggestions (with restore option)
│   │   └── Flush DNS cache
│   ├── Wi-Fi & Port Scanner
│   │   ├── Quick Scan & Deep Scan on local network
│   │   └── TCP port scan on gateway or selected LAN host
│   ├── Web Posture Audit
│   │   ├── DNS IPv4 & HTTPS / TLS check
│   │   └── Security headers & CDN/edge inspection
│   ├── IP, MAC & VPN
│   │   ├── Local IP & MAC lookup
│   │   └── Public IP, approximate location & VPN/proxy indicator
│   ├── Shield & Persistence
│   │   ├── Windows Defender & Firewall status
│   │   └── Startup Run keys inspection
│   └── SHA-256 Integrity
│       ├── Single-file SHA-256 hash
│       └── Folder baseline creation & change tracking (Modified / Added / Removed)
│
└── 🔥 - EVIL TIGER (Recon & MONSTER-OSINT Suite)
    ├── MONSTER-OSINT Suite (READY / NO status)
    │   ├── Email & Breach: holehe, h8mail
    │   ├── Usernames & Social: sherlock, maigret, blackbird, social-analyzer, instaloader
    │   ├── Domain & Subdomains: theHarvester, Sublist3r, wafw00f, dnsrecon
    │   └── Media & Forensics: exiftool, PhotoForensics + pHash
    ├── Wi-Fi & Port Scanner
    ├── Passive DNS & CT Subdomains (crt.sh)
    ├── Web Posture & Headers Audit
    └── Custom AV & Heuristic Scanner
```

---

## ⚙️ Step-by-Step Windows Setup & Execution

### 1. Install Python & Git on Windows

1. **Python (3.9 or higher):**
   - Download from [python.org/downloads](https://www.python.org/downloads/) or install via Windows Terminal (`winget install Python.Python.3.12`).
   - **Important:** During installation, check **"Add Python to PATH"**.
2. **Git for Windows:**
   - Download from [git-scm.com/download/win](https://git-scm.com/download/win) or install via Windows Terminal (`winget install Git.Git`).

Verify both are working in **PowerShell** or **CMD**:

```powershell
py --version
git --version
```

---

### 2. Clone the Repository & Run

Open **PowerShell** or **CMD** (run as **Administrator** if you plan to use Windows De-Bloat policies or Defender scans) and run each command in order:

```powershell
# 1. Clone the repository
git clone https://github.com/Dravok40443/HIBRID-TIGER.git

# 2. Enter the project folder
cd HIBRID-TIGER

# 3. Install Python dependencies
py -m pip install -r requirements.txt

# 4. Launch HIBRID-TIGER
py script.py
```

---

### 3. Alternative: Run Without Git (ZIP Download)

1. Click **Code** -> **Download ZIP** on this GitHub page.
2. Extract the `HIBRID-TIGER-main.zip` folder anywhere on your PC.
3. Open **PowerShell** or **CMD** inside the extracted folder.
4. Install requirements and start the tool:

```powershell
py -m pip install -r requirements.txt
py script.py
```

---

## 🎮 Inside the Menu

- **ANGEL TIGER (Default Mode):** Starts automatically on boot. Select option **`1`** (`Auto-Install Dependencies & OSINT`) on your first run so the toolkit downloads and configures all external OSINT repositories automatically.
- **EVIL TIGER (Recon & OSINT Mode):** Select option **`9`** (`Admin`) inside Angel Tiger to switch interfaces, or option **`6`** inside Evil Tiger to return to Angel Tiger.

---

## 🔄 Updating Your Local Copy

To pull future updates from GitHub into your local folder:

```powershell
cd HIBRID-TIGER
git pull
py -m pip install -r requirements.txt
```
