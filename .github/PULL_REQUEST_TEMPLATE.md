# Pull Request

## Description

Summarize the change and the problem it solves. Link the related issue when applicable.

Fixes #

## Type of change

- [ ] New feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Refactor without behavior change (`refactor`)
- [ ] Documentation (`docs`)
- [ ] Style, QSS, or UI (`style`)
- [ ] Tests (`test`)
- [ ] CI/CD, build, or packaging (`chore`)

## How was it tested?

Describe the validation performed. Include commands and relevant output.

- [ ] **Automated tests:** `python -m unittest discover tests` passes.
- [ ] **Local UI:** `python main.py` was run; both themes, the minimum window size, and the affected screens were checked.
- [ ] **Real request run:** requests were sent to an authorized endpoint; live table insertion and metric updates were verified.
- [ ] **Packaging:** `python scripts/build_executavel.py` produced a working `dist/ValidadorRateLimit.exe`.

## Visual evidence

Attach screenshots or a short GIF for UI changes. Include the theme and window size. Redact tokens, cookies, internal hostnames, and customer data.

## Checklist

- [ ] The change follows the Clean Architecture and SOLID rules in [`CONTRIBUTING.md`](https://github.com/felipevenas/rate-limit-validator/blob/main/CONTRIBUTING.md).
- [ ] Domain and application layers remain independent of PySide6 and network I/O.
- [ ] New or changed behavior is covered by tests.
- [ ] QSS remains centralized in `src/presentation/styles/tema.py`; no inline widget styling was added.
- [ ] Dark mode, light mode, and the minimum window size were verified for UI changes.
- [ ] No secrets, credentials, personal data, or unauthorized target endpoints are included.
- [ ] Documentation and [`CHANGELOG.md`](https://github.com/felipevenas/rate-limit-validator/blob/main/CHANGELOG.md) are updated when needed.
- [ ] The change was tested only against systems I own or am authorized to test.

## Additional context

Add deployment notes, trade-offs, follow-up work, or anything reviewers should know.
