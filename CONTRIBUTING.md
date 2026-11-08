# Contributing to Rate Limit Validator

Thank you for your interest in improving **Rate Limit Validator**. This guide explains the local setup, architecture rules, quality gates, and pull-request process used by the project.

## Golden rule

**Never run stress tests against systems you do not own or have explicit written authorization to test.** A concurrency tool can cause real outages. Contributions that make unauthorized or destructive testing easier will not be accepted.

## Prerequisites

- **Python 3.10–3.12** (validated by CI).
- **Git**.
- **Windows x64** for building and testing the packaged executable; Linux and macOS are supported for source development.
- A REST endpoint you control for manual validation.

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/felipevenas/rate-limit-validator.git
cd rate-limit-validator
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install development dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

`requirements-dev.txt` includes the runtime dependency, the test tooling, and PyInstaller.

### 4. Run the application and the test suite

```bash
python main.py
python -m unittest discover tests
```

## Branch and commit conventions

Use short-lived branches created from `main`. The repository uses Conventional Commits in English.

### Branch names

| Prefix | Use |
|---|---|
| `feat/<short-name>` | New capability |
| `fix/<short-name>` | Bug fix |
| `chore/<short-name>` | Maintenance, dependencies, tooling |
| `docs/<short-name>` | Documentation and governance |
| `style/<short-name>` | Visual/QSS changes without behavior change |
| `refactor/<short-name>` | Internal restructuring without behavior change |
| `test/<short-name>` | Test-only changes |

### Commit messages

```text
feat: add per-request header presets
fix: preserve row order after filtering
docs: document the cancellation flow
style: align metric cards on narrow windows
refactor: isolate CSV column mapping
test: cover 429 header fallbacks
chore: bump PySide6 minimum version
```

Keep the subject imperative, lowercase after the prefix, and under ~72 characters. Explain **why** in the body when the change is not obvious.

## Architecture rules

The project uses Clean Architecture and SOLID. The dependency direction is **presentation → application → domain**, with infrastructure implementing domain contracts.

### Domain (`src/domain/`)

- Keep entities and contracts free of PySide6, `urllib`, filesystem, and presentation imports.
- Enforce invariants in dataclasses (`ConfiguracaoRequisicao`, `PlanoTeste`) so invalid states cannot be constructed.
- Add new behavior through explicit contracts (`IClienteHttp`, `INotificadorProgresso`) rather than concrete dependencies.

### Application (`src/application/`)

- Own use-case orchestration, concurrency, cancellation, and progress notification.
- Do not render UI, write files, or open sockets directly.
- Keep the use case testable with mock implementations of the domain contracts.

### Infrastructure (`src/infrastructure/`)

- Implement domain contracts for HTTP transport and CSV persistence.
- Keep network and file-system details out of the domain and application layers.
- Preserve SSL certificate verification by default. Any opt-out must remain explicit and documented.

### Presentation (`src/presentation/`)

- Keep Qt widgets focused on rendering and user input. Business decisions belong in the use case.
- Communicate through Qt **Signals and Slots**; never mutate widgets from a worker thread.
- Centralize all QSS in [`src/presentation/styles/tema.py`](src/presentation/styles/tema.py). Do not add inline styles in widget constructors.
- Support both dark and light themes for every new visual component.
- The active entry point is `main.py` and the `_qt` modules. Legacy Tkinter modules are retained for reference; do not extend them for new features.

## Quality gates

Before opening a pull request, run:

```bash
python -m unittest discover tests
python scripts/build_executavel.py
```

| Gate | Required |
|---|---|
| Test suite | `python -m unittest discover tests` passes with no failures or errors |
| New behavior | Covered by a unit test in `tests/` |
| Architecture | No inward dependency violations or framework imports in `domain` |
| UI | Works in dark and light themes and remains usable at the minimum window size |
| Packaging | `python scripts/build_executavel.py` produces `dist/ValidadorRateLimit.exe` without critical warnings |

There is no linter or type checker in CI yet. Keep imports, naming, and formatting consistent with the surrounding code.

## Security and privacy rules

- Never commit real tokens, cookies, API keys, private endpoints, or customer data.
- Redact `Authorization`, `Cookie`, and other sensitive headers from screenshots, logs, and issues.
- Do not weaken TLS verification, certificate validation, or timeout handling without a documented security review.
- Do not add automatic retries or traffic amplification that could turn a validation run into an unintended denial-of-service.
- Report vulnerabilities through the private channel described in [`SECURITY.md`](SECURITY.md), never in a public issue.

## Pull request process

1. Create a branch from `main` using the naming convention above.
2. Make a focused change. Avoid unrelated refactors in the same pull request.
3. Add or update tests for every behavior change.
4. Update [`CHANGELOG.md`](CHANGELOG.md) under `Unreleased` when the change is user-visible.
5. Run the quality gates locally.
6. Open the pull request using the repository template. Describe the problem, the solution, how it was tested, and any visual evidence.
7. Address review feedback with new commits; do not force-push over an active review unless asked.

### Definition of Done

- [ ] The change solves a documented problem and stays within scope.
- [ ] Domain, application, infrastructure, and presentation boundaries are respected.
- [ ] Tests pass locally and cover the new behavior.
- [ ] Both themes and the minimum window size were checked for UI changes.
- [ ] No secrets, personal data, or unauthorized target endpoints are included.
- [ ] Documentation and `CHANGELOG.md` are updated when needed.
- [ ] The pull request template is complete and the CI workflow is green.

## Reporting bugs and requesting features

Use the GitHub issue templates:

- [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature request](.github/ISSUE_TEMPLATE/feature_request.md)

For security issues, follow [`SECURITY.md`](SECURITY.md) instead.
