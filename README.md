# Velvet Chrome — VS Code Theme

Velvet Chrome is a minimal dark theme that pairs a unified chrome frame with crisp cyan-violet accents and warm amber highlights. It's tuned for long sessions and clean syntax contrast across TypeScript, TSX, Python, SQL, Java, JSON, and Markdown.

## Highlights

- Unified, low-noise UI chrome with clear focus states.
- Split cyan-violet accents for structure and navigation.
- Warm gold for strings and important highlights.
- Muted green for comments and Git cues.

## Accessibility

Velvet Chrome is designed with measurable contrast targets in mind.

- Core text and UI pairs are checked with `scripts/contrast_report.py`.
- Target for text readability is WCAG AA contrast ($\ge 4.5:1$).
- Diff view uses a teal-vs-plum split for added/removed regions to reduce reliance on red/green-only distinction.

Current measured diff metrics:

- `editor.foreground` on inserted diff background: `8.40:1`
- `editor.foreground` on removed diff background: `13.23:1`
- inserted vs removed text backgrounds: `1.58:1`
- inserted vs removed line backgrounds: `1.68:1`

These values come from the built-in report script and can be re-checked after any palette changes.

## Palette reference

| Token | Hex | Usage |
| --- | --- | --- |
| Background | `#191919` | Editor background |
| Foreground | `#ECECEC` | Editor text |
| Accent Violet | `#CFA0FF` | Active borders, cursor |
| Accent Cyan | `#74C6FF` | Types, info, focus |
| Accent Gold | `#E6C36A` | Strings, warnings |
| Accent Orange | `#DDA167` | Declarations |
| Accent Green | `#6A9E86` | Comments, git added |
| Accent Red | `#D97A7A` | Errors, git removed |
| Accent Purple | `#D6A8FF` | Keywords |

## Installation

### Marketplace

1. Open the Extensions view in VS Code.
2. Search for **Velvet Chrome**.
3. Click **Install**.

### VSIX

1. Download the `.vsix` package from the releases page.
2. In VS Code, run **Extensions: Install from VSIX...**
3. Select the downloaded file.

## Activate the theme

1. Open the Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux).
2. Run **Preferences: Color Theme**.
3. Select **Velvet Chrome**.

## Development

1. Open this repository in VS Code.
2. Press `F5` to launch the Extension Development Host.
3. In the new window, activate **Velvet Chrome** via **Preferences: Color Theme**.
4. Run `scripts/contrast_report.py` to verify contrast after edits.

## Contributing

Suggestions and improvements are welcome. Please open an issue or submit a pull request.

## License

GNU GPLv3. See `LICENSE` for details.
