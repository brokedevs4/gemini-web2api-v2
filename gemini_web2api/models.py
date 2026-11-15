"""Model definitions and mapping from Gemini frontend UI and JS source.

Corresponding to Gemini Web (November 2026 UI update):
- Everyday help (New): 4 Hydrogen
- Code & analysis: 4 Argon
- Detailed research: 3.1 Pro
- Quick answers: 3.5 Flash-Lite
- Thinking level: High (0), Medium (2), Low/Auto (4)
"""

# MODE_CATEGORY enum from Gemini Web JS bundles:
#   1 = FAST / Everyday (Flash, 4 Hydrogen)
#   2 = THINKING / Code & Analysis (4 Argon, Flash-Thinking)
#   3 = PRO / Detailed Research (3.1 Pro)
#   4 = AUTO
#   5 = FAST_DYNAMIC_THINKING
#   6 = FLASH_LITE / Quick answers (3.5 Flash-Lite)

MODELS = {
    # ── Current Gemini Web UI Models ──────────────────────────────────────────
    "gemini-4-hydrogen": {
        "mode": 1,
        "think": 4,
        "desc": "Everyday help (Gemini 4 Hydrogen) - Fast everyday assistance, coding and agentic execution",
        "ui_label": "Everyday help",
        "ui_tier": "4 Hydrogen",
    },
    "gemini-4-argon": {
        "mode": 2,
        "think": 0,
        "desc": "Code & analysis (Gemini 4 Argon) - Frontier reasoning model specialized for deep coding and complex problem-solving",
        "ui_label": "Code & analysis",
        "ui_tier": "4 Argon",
    },
    "gemini-3.1-pro": {
        "mode": 3,
        "think": 4,
        "desc": "Detailed research (Gemini 3.1 Pro) - Advanced research, analysis and math (requires Gemini Advanced cookie)",
        "ui_label": "Detailed research",
        "ui_tier": "3.1 Pro",
    },
    "gemini-3.5-flash-lite": {
        "mode": 6,
        "think": 4,
        "desc": "Quick answers (Gemini 3.5 Flash-Lite) - Lightweight, lowest latency for quick questions",
        "ui_label": "Quick answers",
        "ui_tier": "3.5 Flash-Lite",
    },

    # ── Aliases for Convenient Access ─────────────────────────────────────────
    "gemini-hydrogen": {
        "mode": 1, "think": 4, "desc": "Alias for gemini-4-hydrogen", "alias_for": "gemini-4-hydrogen",
    },
    "gemini-everyday": {
        "mode": 1, "think": 4, "desc": "Alias for gemini-4-hydrogen (Everyday help)", "alias_for": "gemini-4-hydrogen",
    },
    "gemini-4-everyday": {
        "mode": 1, "think": 4, "desc": "Alias for gemini-4-hydrogen", "alias_for": "gemini-4-hydrogen",
    },
    "gemini-argon": {
        "mode": 2, "think": 0, "desc": "Alias for gemini-4-argon", "alias_for": "gemini-4-argon",
    },
    "gemini-code": {
        "mode": 2, "think": 0, "desc": "Alias for gemini-4-argon (Code & analysis)", "alias_for": "gemini-4-argon",
    },
    "gemini-4-code": {
        "mode": 2, "think": 0, "desc": "Alias for gemini-4-argon", "alias_for": "gemini-4-argon",
    },
    "gemini-research": {
        "mode": 3, "think": 4, "desc": "Alias for gemini-3.1-pro (Detailed research)", "alias_for": "gemini-3.1-pro",
    },
    "gemini-pro": {
        "mode": 3, "think": 4, "desc": "Alias for gemini-3.1-pro", "alias_for": "gemini-3.1-pro",
    },
    "gemini-flash-lite": {
        "mode": 6, "think": 4, "desc": "Alias for gemini-3.5-flash-lite", "alias_for": "gemini-3.5-flash-lite",
    },
    "gemini-quick": {
        "mode": 6, "think": 4, "desc": "Alias for gemini-3.5-flash-lite (Quick answers)", "alias_for": "gemini-3.5-flash-lite",
    },

    # ── Legacy & Compatibility Models ─────────────────────────────────────────
    "gemini-3.7-flash": {
        "mode": 1, "think": 4, "desc": "Gemini 3.7 Flash",
    },
    "gemini-3.6-flash": {
        "mode": 1, "think": 4, "desc": "Gemini 3.6 Flash (Legacy default)",
    },
    "gemini-3.5-flash": {
        "mode": 1, "think": 4, "desc": "Alias for Flash tier",
    },
    "gemini-3.5-flash-thinking": {
        "mode": 2, "think": 0, "desc": "Deep thinking mode (~20k chars)",
    },
    "gemini-3.5-flash-thinking-lite": {
        "mode": 5, "think": 0, "desc": "Dynamic thinking with adaptive depth",
    },
    "gemini-3.1-pro-enhanced": {
        "mode": 3, "think": 4, "extra": {31: 2, 80: 3}, "desc": "Pro with enhanced output (experimental)",
    },
    "gemini-auto": {
        "mode": 4, "think": 4, "desc": "Auto model selection",
    },
}

# Standard OpenAI reasoning_effort mapping
REASONING_EFFORT_MAP = {
    "high": 0,     # Deep reasoning / maximum think budget
    "deep": 0,
    "medium": 2,   # Moderate thinking
    "low": 4,      # Shallow thinking / auto
    "auto": 4,
    "none": 4,
}


def resolve_model(model_name: str, reasoning_effort: str = None, default: str = "gemini-4-hydrogen"):
    """Resolve model name and reasoning effort to (name, mode_id, think_mode, error, extra_fields).

    Unknown model names fall back to default rather than erroring,
    since upstream clients may request arbitrary model identifiers.
    """
    think_override = None

    # 1. Handle '@think=N' suffix
    if "@think=" in model_name:
        model_name, think_str = model_name.rsplit("@think=", 1)
        try:
            think_override = int(think_str)
        except ValueError:
            return None, None, None, f"Invalid think level: {think_str}", None

    # 2. Handle OpenAI 'reasoning_effort' parameter if not already overridden
    if think_override is None and reasoning_effort:
        effort_key = str(reasoning_effort).strip().lower()
        if effort_key in REASONING_EFFORT_MAP:
            think_override = REASONING_EFFORT_MAP[effort_key]

    cfg = MODELS.get(model_name)
    if not cfg:
        from .gemini import log
        log(f"Unknown model '{model_name}', falling back to '{default}'")
        model_name = default
        cfg = MODELS[default]

    mode_id = cfg["mode"]
    think_mode = think_override if think_override is not None else cfg["think"]
    extra = cfg.get("extra")
    return model_name, mode_id, think_mode, None, extra
