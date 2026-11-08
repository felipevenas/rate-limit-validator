# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Documentation

- Standardized the README in English with verified stack, architecture, execution flow, configuration, testing, packaging, and limitation sections.
- Translated and refreshed `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`, issue templates, and the pull-request template.
- Translated workflow display names and label descriptions to English without changing workflow behavior.
- Translated `.env.example` comments to English and documented that the file is a reference only, not loaded at runtime.
- Removed documentation mojibake and normalized rewritten files to UTF-8.

## [2.0.0] - 2026-08-23

### Added

- **Complete migration to PySide6 (Qt for Python)** with a decoupled Clean Architecture.
- **Premium design system** with instant **Dark Mode (Minimalist Slate & Indigo)** and **Light Mode (Clean Light)** themes.
- **Executive brand bar** with a high-definition vector SVG logo (`app_icon.svg`) and a reactive status indicator.
- **Interactive help buttons (`?`)** with rich HTML tooltips and explanatory dialogs for every parameter, including threads, 429 rate limits, timeout, latency, and RPS.
- **Real-time request table**:
  - Dynamic insertion for every received response.
  - Quick filters for all requests, 2xx successes, 429 rate limits, and errors.
  - Real-time text search by ID, HTTP status, and error message.
  - Dynamic sorting by clicking a column header.
- **Advanced metrics panel** with progress, 2xx successes, 429 blocks, failures, average latency, and effective RPS.
- **System tray integration**:
  - Native Windows tray icon (`QSystemTrayIcon`).
  - Context menu to restore the window, switch themes, and exit.
  - Automatic balloon notifications when a test suite completes.
  - Windows `SetCurrentProcessExplicitAppUserModelID` registration for the taskbar and Alt+Tab icon.
- **CSV report export** with aggregated statistics and one detail row per request.
- **CI/CD pipeline** with a cross-platform GitHub Actions test matrix and automatic Windows executable build and publication.
- **Multi-agent governance** with seven specialized role definitions under `.agents/` (`tech-lead`, `software-architect`, `backend-dev`, `frontend-dev`, `ux-ui-designer`, `qa-engineer`, `security-engineer`).

## [1.0.0] - 2026-08-22

### Added

- Initial release with the concurrency test core and rate-limit policy detection.
