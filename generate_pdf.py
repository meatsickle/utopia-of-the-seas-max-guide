#!/usr/bin/env python3
"""Render the self-contained Utopia infographic HTML to PDF with local Chromium."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent
HTML_PATH = REPO_DIR / "utopia-max-infographic.html"
PDF_PATH = REPO_DIR / "Utopia_of_the_Seas_MAX_Guide_Final.pdf"
ALT_PDF_PATH = REPO_DIR / "final.pdf"


def resolve_chromium() -> str:
    for candidate in ("chromium", "google-chrome", "chromium-browser"):
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError("Could not find Chromium or Chrome in PATH.")


def main() -> int:
    if not HTML_PATH.exists():
        print(f"Missing HTML source: {HTML_PATH}", file=sys.stderr)
        return 1

    browser = resolve_chromium()
    url = HTML_PATH.resolve().as_uri()

    with tempfile.TemporaryDirectory(prefix="utopia-pdf-", ignore_cleanup_errors=True) as profile_dir:
        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-first-run",
            "--run-all-compositor-stages-before-draw",
            f"--user-data-dir={profile_dir}",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={PDF_PATH}",
            "--window-size=1632,1056",
            url,
        ]

        try:
            result = subprocess.run(
                cmd,
                cwd=REPO_DIR,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            if not PDF_PATH.exists():
                print("Chromium timed out before writing the PDF.", file=sys.stderr)
                return 1
        else:
            if result.returncode != 0:
                print(result.stdout)
                print(result.stderr, file=sys.stderr)
                return result.returncode

    shutil.copyfile(PDF_PATH, ALT_PDF_PATH)
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"PDF created: {PDF_PATH.name} ({size_kb:.1f} KB)")
    print(f"Mirror copy: {ALT_PDF_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
