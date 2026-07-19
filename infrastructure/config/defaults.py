"""Module responsible for defining immutable application layout styles, themes, and asset defaults."""

from typing import Final, List, Tuple

# ----------------------------------------------------------------------
# Core Application Theme Settings
# ----------------------------------------------------------------------
DEFAULT_THEME: Final[str] = "blue"
DEFAULT_APPEARANCE_MODE: Final[str] = "dark"
DEFAULT_FONT_FAMILY: Final[str] = "Comic Sans MS"

APPEARANCE_MODES: Final[List[str]] = ["light", "dark", "system"]
CUSTOM_THEMES: Final[List[str]] = [
    "autumn",
    "breeze",
    "carrot",
    "cherry",
    "coffee",
    "lavender",
    "marsh",
    "metal",
    "midnight",
    "orange",
    "patina",
    "pink",
    "red",
    "rime",
    "rose",
    "sky",
    "violet",
]
DEFAULT_THEMES: Final[List[str]] = ["dark-blue", "green", "blue"]

# ----------------------------------------------------------------------
# UI Layout Dimensions & Paddings
# ----------------------------------------------------------------------
PAD_X: Final[int] = 5
PAD_Y: Final[int] = 5
TITLE_PAD_X: Final[int] = 35
CORNER_RADIUS: Final[int] = 5
LABEL_FORM_PAD_Y: Final[int] = 30
WINDOW_HEADER_HEIGHT: Final[int] = 23
PAD_Y_HABIT_FORM_BUTTONS: Final[int] = 20

NAV_HEADER_WIDTH: Final[int] = 170
COLUMN_HABIT_TABLE_WIDTH: Final[int] = 380
BOARD_BUTTONS_WIDTH: Final[int] = int((COLUMN_HABIT_TABLE_WIDTH / 2) - PAD_X)

# ----------------------------------------------------------------------
# Core Brand Palette & Interface Colors
# ----------------------------------------------------------------------
# Light and Dark mode variations mapped as strict tuples
COLOR_AUTHOR_TAG: Final[Tuple[str, str]] = ("gray20", "gray70")
COLOR_MAIN_NAV_BAR: Final[str] = "#303030"
COLOR_ACCENT_CONTRAST: Final[str] = "#0fa987"
COLOR_FOREGROUND_FRAME: Final[str] = "#333333"
COLOR_BACKGROUND_MAIN: Final[str] = "#2b2b2b"
COLOR_DASH_DIVIDER: Final[str] = "#D1D1D1"

# ----------------------------------------------------------------------
# Immutable Asset Palettes (Icons & HEX Color Swatches)
# ----------------------------------------------------------------------
CATEGORY_ICONS: Final[List[str]] = [
    "",    # No icon placeholder
    "💪",  # Health
    "📚",  # Education
    "💼",  # Work
    "💻",  # Development
    "🌱",  # Wellness
    "🏠",  # Home
    "🎯",  # Goals
    "🎨",  # Creativity
    "💰",  # Finance
    "👥",  # Social
    "🧠",  # Personal Growth
    "✨",  # General
    "🏆",  # Achievements
    "🛫",  # Travel
    "🛍",  # Shopping
    "📱",  # Technology
    "🎮",  # Leisure
    "🧘",  # Spirituality
    "🍽",  # Nutrition
    "🚗",  # Transportation
    "🐶",  # Pets
    "🏥",  # Medical
    "📦",  # Organization
]

HEX_COLOR_PALETTE: Final[List[str]] = [
    # Reds (10)
    "#7F1D1D", "#991B1B", "#B91C1C", "#C62828", "#8B0000",
    "#9F1239", "#881337", "#A4161A", "#B23A48", "#800020",
    
    # Pinks / Fuchsia (8)
    "#9D174D", "#BE185D", "#A21CAF", "#86198F",
    "#C2185B", "#AD1457", "#880E4F", "#7B1FA2",
    
    # Oranges / Earth (10)
    "#7C2D12", "#9A3412", "#B45309", "#C2410C", "#CC7722",
    "#92400E", "#78350F", "#8C2F39", "#A0522D", "#5D4037",
    
    # Mustard / Gold (6)
    "#854D0E", "#A16207", "#B7791F",
    "#975A16", "#744210", "#996515",
    
    # Greens (10)
    "#14532D", "#166534", "#15803D", "#1B4332", "#065F46",
    "#047857", "#064E3B", "#4F8A77", "#2F5233", "#1F7A1F",
    
    # Olive / Dark Lime (6)
    "#3F6212", "#365314", "#4D7C0F",
    "#556B2F", "#4B5320", "#3A5F0B",
    
    # Blues (10)
    "#1E3A8A", "#1D4ED8", "#1E40AF", "#1E293B", "#0F172A",
    "#1B3A4B", "#274C77", "#3B6BA5", "#14213D", "#0A2463",
    
    # Indigo / Navy (8)
    "#312E81", "#3730A3", "#1A237E", "#283593",
    "#1C1F4A", "#2C3E50", "#1F3A93", "#192A56",
    
    # Purples (8)
    "#4C1D95", "#581C87", "#6A1B9A", "#7C3AED",
    "#7E5A9B", "#5B2C6F", "#4A148C", "#301934",
    
    # Teal / Cyan (6)
    "#134E4A", "#0F766E", "#115E59",
    "#264653", "#0E7490", "#155E75",
    
    # Grays / Slate (10)
    "#111111", "#1A1A1A", "#222222", "#2A2A2A", "#333333",
    "#3D3D3D", "#444444", "#4D4D4D", "#555555", "#1F2937",
]