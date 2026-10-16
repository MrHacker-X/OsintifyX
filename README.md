<div align="center">

# ⃤ O S I N T I F Y X ⃤

### *Instagram OSINT in your terminal - 16 modules, one session, zero browser.*

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Instagram](https://img.shields.io/badge/Source-Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20macOS-38;5;150?style=flat-square)
![Modules](https://img.shields.io/badge/OSINT%20Modules-16-38;5;245?style=flat-square)
![Stars](https://img.shields.io/github/stars/MrHacker-X/OsintifyX?style=flat-square&color=orange)
![License](https://img.shields.io/badge/License-MIT-38;5;179?style=flat-square)

</div>

---

## 📋 Table of Contents

- [🎯 Why OsintifyX?](#-why-osintifyx)
- [🧭 What It Does](#-what-it-does)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [✨ Features](#-features)
- [⌨️ Usage](#%EF%B8%8F-usage)
- [⚙️ Configuration](#%EF%B8%8F-configuration)
- [🧰 Tech Stack](#-tech-stack)
- [⚠️ Disclaimer](#%EF%B8%8F-disclaimer)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👨‍💻 Developer](#-developer)

---

## 🎯 Why OsintifyX?

> Instagram profile research usually means screenshots, copy-paste, and a desktop browser. **OsintifyX is one menu**: log in with a disposable account once, then pull profile facts, engagement stats, lists, captions and media straight into your terminal - and save them as text reports.
>
> **v2.0 modernizes the engine.** Built on **instaloader** with a premium violet-gold rich theme, the upgrade brings: single-pass scraping (all 16 modules reuse one cached post fetch per target), per-module error containment (login, rate limits, private accounts - the loop never crashes out), pure-Python file handling instead of shell `rm -rf`/`mv`, session reuse between runs, and fail-fast config validation. Setup detects Termux and four Linux package managers automatically and verifies every dependency before claiming success.

---

## 🧭 What It Does

| # | Module | What you get |
|---|--------|-------------|
| 1️⃣ | **Account side** | Profile info dump, biography, follower/following lists, tagged-user counts |
| 2️⃣ | **Post content** | Post details, captions, hashtags with counts, media-type breakdown, photos downloads |
| 3️⃣ | **Engagement** | Commenter list, all comments, liker lists per post, locations, stories |

**What this tool is NOT:** it is **not** a hacking tool, **not** an exploit kit, and **not** a bypass for Instagram privacy. It only reads what your logged-in account can already see - the same views you get in the app. See the [Disclaimer](#%EF%B8%8F-disclaimer) and [TERMS.md](TERMS.md).

**Rule of thumb:** only investigate accounts you have a right to research, and respect Instagram's terms of service and rate limits.

---

## 🚀 Quick Start

```bash
git clone https://github.com/MrHacker-X/OsintifyX.git
cd OsintifyX
./setup.sh                       # installs deps (Termux / apt / dnf / pacman / apk)
nano config.py                   # disposable Instagram login, or use env vars
python3 osintifyx.py             # menu starts
```

<details>
<summary><b>🔑 What login does OsintifyX need?</b></summary>

A **disposable Instagram account** (never your main one - Instagram may flag heavy viewing activity). Set it in `config.py` or export `INSTAGRAM_USERNAME` / `INSTAGRAM_PASSWORD`. The session is cached locally and reused between runs.

</details>

---

## 📦 Installation

### Termux (Android)

```bash
apt update -y && apt install git python -y
git clone https://github.com/MrHacker-X/OsintifyX.git
cd OsintifyX
chmod +x setup.sh
./setup.sh
```

### Desktop Linux / macOS

```bash
git clone https://github.com/MrHacker-X/OsintifyX.git
cd OsintifyX
./setup.sh          # or: pip install -r requirements.txt
```

### Supported Systems

| OS | Status | Notes |
|----|--------|-------|
| 📱 Termux (Android) | ✅ Fully supported | Auto-detected |
| 🐧 Debian / Ubuntu / Kali | ✅ Fully supported | `apt` detected automatically |
| 🐧 Fedora / RHEL | ✅ Fully supported | `dnf` detected automatically |
| 🐧 Arch / Manjaro | ✅ Fully supported | `pacman` detected automatically |
| 🐧 Alpine | ✅ Fully supported | `apk` detected automatically |
| 🍎 macOS | ✅ Fully supported | pip-only path, needs Python preinstalled |

> 💡 The setup script **verifies every dependency** at the end and tells you exactly what's missing - it will never print "installed successfully" when it isn't.

---

## ✨ Features

| | Feature | Description |
|---|---------|-------------|
| 🔍 | **16 OSINT modules** | Info → Hashtag → Follows → Followings → Tagged → Post → Caption → Location → Stories → ProPic → Images → Commenters → Comments → Likers → Biography → Media types |
| ⚡ | **Single-pass scraping** | All modules reuse one cached post fetch per target - half the API load of the original |
| 🛡️ | **Error containment** | Bad credentials, rate limits, private profiles and dead targets report cleanly and return to the menu |
| ♻️ | **Session reuse** | Login session cached locally, restored on the next run |
| 🎨 | **Premium color theme** | Same violet-gold rich palette as ArtifyX / GPTX - one visual identity |
| 🧹 | **Safe file ops** | Pure-Python output handling - no shell `rm -rf` or `mv` with user input |
| 🩹 | **Fail-fast validation** | Missing credentials → one clear line at startup, no stack trace |
| 📁 | **Report saving** | Optional `y/n` save mode - every module writes plain-text tables to `output/` |
| 🪶 | **Minimal dependencies** | 3 packages: `instaloader`, `rich`, `tabulate` |

---

## ⌨️ Usage

Run the tool, pick a module:

```bash
python3 osintifyx.py
```

| Input | Result |
|-------|--------|
| Target username | Validated against Instagram before the menu opens |
| `01`–`16` | Run a scraping module (single or double digit both work) |
| `91` | About - tool info and usage notes |
| `95` | Network link |
| `99`, `exit`, `bye`, Ctrl+C, Ctrl+D | Clean exit |

With saving enabled, every module writes `output/<target>_<module>.txt` - profile info, hashtag tables, follower lists, comment dumps, and so on.

---

## ⚙️ Configuration

Everything lives in [`config.py`](config.py) - and every setting can be overridden from the shell:

| Setting | Env var | Default | Description |
|---------|---------|---------|-------------|
| Login username | `INSTAGRAM_USERNAME` | *(required)* | Your disposable account |
| Login password | `INSTAGRAM_PASSWORD` | *(required)* | Its password |
| Output folder | `OSINTIFYX_OUTPUT_DIR` | `output` | Where reports are saved |
| Rate delay | `OSINTIFYX_RATE_DELAY` | `2` | Seconds between Instagram calls |

```bash
# either edit config.py, or:
export INSTAGRAM_USERNAME="disposable_account"
export INSTAGRAM_PASSWORD="password"
```

> 🔒 Session files (`*_session`) and scraped output are local-only - keep them out of any repo (`.gitignore` handles it).

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| Instagram | `instaloader` (session login, scraping, downloads) |
| Terminal UI | `rich` - custom violet/gold theme |
| Tables | `tabulate` (fancy_grid) |
| Setup | POSIX bash with 5 environment detections |

---

## ⚠️ Disclaimer

> ### Read this before using OsintifyX.
>
> 1. **Read-only, within your access.** OsintifyX only retrieves views available to the logged-in account. It does not bypass privacy, hack accounts, or fetch anything Instagram hides.
> 2. **Disposable account mandatory.** Log in with a fake/throwaway account - heavy viewing activity can get an account rate-limited or flagged.
> 3. **Instagram's terms apply.** You are responsible for how you scrape and what you do with the data. Respect privacy and local law.
> 4. **No warranty.** Provided "as is" under the MIT License - the author is **not liable** for misuse, account restrictions, or any damage resulting from use.

Full terms: [TERMS.md](TERMS.md).

---

## 📜 License

Distributed under the MIT License. See the [`LICENSE`](LICENSE) file for the full text.

---

## 🤝 Contributing

Contributions to OsintifyX are always welcome! If you find any issues or have suggestions for improvement, please open an issue on the GitHub repository.

Ideas worth exploring: one-shot CLI mode (`--module 3 -u target`), JSON report output alongside tables, stat exports across multiple targets, post-URL deep-dive module.

---

## 👨‍💻 Developer

| | |
|---|---|
| **Dev** | MrHacker-X |
| **GitHub** | [github.com/MrHacker-X](https://github.com/MrHacker-X) |
| **Email** | [contact@vritrasec.com](mailto:contact@vritrasec.com) |
| **Website** | [vritrasec.com](https://vritrasec.com) |
| **Network** | [link.vritrasec.com](https://link.vritrasec.com) |

---
