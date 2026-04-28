"""Модуль конфигурации."""

import sys
from pathlib import Path

TITLE = "Викторина про космос"

if getattr(sys, "frozen", False):  # открыто из EXE
    BASE_DIR = Path(getattr(sys, "_MEIPASS", sys.executable)).resolve()
    STATS_PATH = Path(sys.executable).parent.resolve() / "base.json"
else:  # открыто из py файла
    BASE_DIR = Path(__file__).resolve().parent
    STATS_PATH = BASE_DIR / "base.json"

ASSETS_DIR = BASE_DIR / "assets"
DIR_IMG = ASSETS_DIR / "img"
FONT_DIR = ASSETS_DIR / "font"
DIR_SOUND = ASSETS_DIR / "sound"
STATS_PATH = BASE_DIR / "statistics.json"

FONT_SIZE = 20
