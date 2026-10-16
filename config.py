"""
OsintifyX configuration.

Every setting can also be supplied as an environment variable -
the environment (or shell export) always takes precedence over
whatever is written in this file.

Use a disposable / fake Instagram account for login.
"""

import os

# ---------------------------------------------------------------
# Required credentials - your disposable login account
# ---------------------------------------------------------------

# Instagram login username of your disposable account
# or: export INSTAGRAM_USERNAME="your_throwaway_account"
usernamex = os.environ.get("INSTAGRAM_USERNAME", "")

# Instagram login password of your disposable account
# or: export INSTAGRAM_PASSWORD="your_password"
passwordx = os.environ.get("INSTAGRAM_PASSWORD", "")

# ---------------------------------------------------------------
# Optional behavior
# ---------------------------------------------------------------

# Folder where scraped data is saved
# or: export OSINTIFYX_OUTPUT_DIR="output"
OUTPUT_DIR = os.environ.get("OSINTIFYX_OUTPUT_DIR", "output")

# Seconds between Instagram API calls (be gentle or you get rate-limited)
# or: export OSINTIFYX_RATE_DELAY="2"
RATE_DELAY = float(os.environ.get("OSINTIFYX_RATE_DELAY", "2"))

# ---------------------------------------------------------------
# Validation - fail fast with a clear message, not a stack trace
# ---------------------------------------------------------------

if not usernamex:
    raise SystemExit(
        "Instagram username not configured.\n"
        "  Set usernamex in config.py, or export INSTAGRAM_USERNAME."
    )

if not passwordx:
    raise SystemExit(
        "Instagram password not configured.\n"
        "  Set passwordx in config.py, or export INSTAGRAM_PASSWORD."
    )

if usernamex == "your_throwaway_account" or passwordx == "your_password":
    raise SystemExit(
        "Placeholder credentials detected.\n"
        "  Replace them with your disposable Instagram login in config.py."
    )
