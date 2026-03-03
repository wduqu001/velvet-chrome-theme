import json
import re
from pathlib import Path

THEME_PATH = Path(__file__).resolve().parents[1] / "themes" / "velvet-chrome-color-theme.json"


def hex_to_rgba(value: str):
    """Parse a hex color string into an RGBA tuple.

    Supports #RGB, #RGBA, #RRGGBB, and #RRGGBBAA formats. Returns None for
    unsupported inputs.
    """
    value = value.strip()
    if not value.startswith("#"):
        return None
    value = value[1:]
    if len(value) in (3, 4):
        value = "".join([ch * 2 for ch in value])
    if len(value) == 6:
        r, g, b = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
        a = 255
    elif len(value) == 8:
        r, g, b = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
        a = int(value[6:8], 16)
    else:
        return None
    return (r, g, b, a)


def srgb_to_linear(channel: int) -> float:
    """Convert an sRGB channel (0-255) into linear light space."""
    c = channel / 255.0
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb) -> float:
    """Compute relative luminance for an (R, G, B) tuple."""
    r, g, b = rgb
    r_lin, g_lin, b_lin = (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b))
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def blend(fg, bg):
    """Alpha-blend a foreground RGBA color over an opaque background RGBA."""
    fr, fg_g, fb, fa = fg
    br, bg_g, bb, _ = bg
    alpha = fa / 255.0
    r = round(fr * alpha + br * (1 - alpha))
    g = round(fg_g * alpha + bg_g * (1 - alpha))
    b = round(fb * alpha + bb * (1 - alpha))
    return (r, g, b)


def contrast_ratio(fg, bg) -> float:
    """Return the WCAG contrast ratio between two RGB colors."""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    l1, l2 = (l1, l2) if l1 >= l2 else (l2, l1)
    return (l1 + 0.05) / (l2 + 0.05)


def resolve_rgb(color_hex: str, fallback_bg_rgba):
    """Resolve a theme color token into an RGB tuple.

    If the color has transparency, it is alpha-blended over fallback_bg_rgba.
    """
    rgba = hex_to_rgba(color_hex)
    if not rgba:
        return None
    if rgba[3] < 255:
        return blend(rgba, fallback_bg_rgba)
    return rgba[:3]


def main() -> None:
    """Load theme colors and print contrast ratios for key UI pairs."""
    text = re.sub(r"//.*", "", THEME_PATH.read_text())
    colors = json.loads(text).get("colors", {})

    pairs = [
        ("editor.foreground", "editor.background"),
        ("editor.selectionForeground", "editor.selectionBackground"),
        ("editor.selectionForeground", "editor.inactiveSelectionBackground"),
        ("editorCursor.foreground", "editor.background"),
        ("editorLineNumber.foreground", "editor.background"),
        ("editorLineNumber.activeForeground", "editor.background"),
        ("list.activeSelectionForeground", "list.activeSelectionBackground"),
        ("list.inactiveSelectionForeground", "list.inactiveSelectionBackground"),
        ("statusBar.foreground", "statusBar.background"),
        ("sideBar.foreground", "sideBar.background"),
        ("tab.activeForeground", "tab.activeBackground"),
        ("tab.inactiveForeground", "tab.inactiveBackground"),
    ]

    editor_bg = colors.get("editor.background")
    editor_bg_rgba = hex_to_rgba(editor_bg) if editor_bg else None
    results = []

    for fg_key, bg_key in pairs:
        fg_hex = colors.get(fg_key)
        bg_hex = colors.get(bg_key) or editor_bg
        if not fg_hex or not bg_hex:
            continue
        fg = hex_to_rgba(fg_hex)
        bg = hex_to_rgba(bg_hex)
        if not fg or not bg:
            continue
        fg_rgb = blend(fg, bg) if fg[3] < 255 else fg[:3]
        bg_rgb = bg[:3]
        ratio = contrast_ratio(fg_rgb, bg_rgb)
        results.append((ratio, fg_key, bg_key, fg_hex, bg_hex))

    results.sort()
    print("Contrast ratios (lowest first):")
    for ratio, fg_key, bg_key, fg_hex, bg_hex in results:
        print(f"{fg_key} on {bg_key}: {fg_hex} / {bg_hex} -> {ratio:.2f}:1")

    # Diff-specific checks.
    diff_token_keys = [
        "editor.foreground",
        "diffEditor.insertedTextBackground",
        "diffEditor.removedTextBackground",
        "diffEditor.insertedLineBackground",
        "diffEditor.removedLineBackground",
    ]

    if editor_bg_rgba and all(colors.get(key) for key in diff_token_keys):
        editor_fg_rgb = resolve_rgb(colors["editor.foreground"], editor_bg_rgba)
        inserted_text_rgb = resolve_rgb(colors["diffEditor.insertedTextBackground"], editor_bg_rgba)
        removed_text_rgb = resolve_rgb(colors["diffEditor.removedTextBackground"], editor_bg_rgba)
        inserted_line_rgb = resolve_rgb(colors["diffEditor.insertedLineBackground"], editor_bg_rgba)
        removed_line_rgb = resolve_rgb(colors["diffEditor.removedLineBackground"], editor_bg_rgba)

        diff_results = [
            (
                "editor.foreground on diffEditor.insertedTextBackground",
                contrast_ratio(editor_fg_rgb, inserted_text_rgb),
                4.5,
                "AA text readability",
            ),
            (
                "editor.foreground on diffEditor.removedTextBackground",
                contrast_ratio(editor_fg_rgb, removed_text_rgb),
                4.5,
                "AA text readability",
            ),
            (
                "diffEditor.insertedTextBackground vs diffEditor.removedTextBackground",
                contrast_ratio(inserted_text_rgb, removed_text_rgb),
                1.2,
                "non-text distinguishability",
            ),
            (
                "diffEditor.insertedLineBackground vs diffEditor.removedLineBackground",
                contrast_ratio(inserted_line_rgb, removed_line_rgb),
                1.2,
                "non-text distinguishability",
            ),
        ]

        print("\nDiff accessibility checks:")
        for label, ratio, threshold, criteria in diff_results:
            status = "PASS" if ratio >= threshold else "WARN"
            print(f"{label}: {ratio:.2f}:1 [{status}] ({criteria}, threshold {threshold:.1f}:1)")


if __name__ == "__main__":
    main()
