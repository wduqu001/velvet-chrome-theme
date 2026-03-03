# Change Log

All notable changes to the "velvet-chrome-theme" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.


## [0.0.3] - 2026-03-02

### Changed

- Bumped extension version to `0.0.3` for Marketplace publication.
- Added extension icon manifest field (`"icon": "assets/icon/icon.png"`) so the Marketplace listing shows the theme icon.
- Synced `package-lock.json` version metadata with the published extension version.

## [0.0.2]

### Added

- Added diff-specific accessibility checks to `scripts/contrast_report.py`.
- Added a dedicated Accessibility section to `README.md` with measurable contrast targets and current diff metrics.
- Added SVG assets for article cover and icon.

### Changed

- Tuned diff editor colors to improve readability and color-blind distinguishability.
- Reduced green dominance in inserted diff regions and increased inserted-vs-removed visual separation.
- Corrected publisher name in `package.json` to match Visual Studio Marketplace publisher credentials.

## [0.0.1] - 2026-02-15

### Added

- Initial extension scaffolding (`package.json`, `package-lock.json`, `.gitignore`, `.vscodeignore`, and `CHANGELOG.md`).
- Initial dark theme configuration (later renamed to Velvet Chrome).
- Project `README.md` with installation, usage, and contribution guidance.
- `scripts/contrast_report.py` to measure theme contrast ratios.

### Changed

- Renamed `my-theme` to `velvet-chrome` and aligned theme contribution settings with VS Code best practices.
- Refactored theme colors for improved readability and consistency.
- Updated `README.md` content and removed obsolete links/config references.
