# Security Policy

Security is a first-class concern for a tool that sends authenticated traffic to production APIs. If you believe you have found a vulnerability in **Rate Limit Validator**, please report it privately so it can be assessed and fixed before public disclosure.

## Supported versions

Only the latest release on `main` receives active security updates.

| Version | Supported |
|---|---|
| `2.0.x` | :white_check_mark: |
| `< 2.0` | :x: |

## Reporting a vulnerability

**Do not open a public issue for a security vulnerability.**

Use GitHub's private vulnerability reporting:

1. Open a confidential report at [Private Vulnerability Reporting](https://github.com/felipevenas/rate-limit-validator/security/advisories/new).
2. Include the affected version, platform, reproduction steps, potential impact, and any proof of concept.
3. Redact real credentials, tokens, customer data, and private endpoints from all attachments.
4. The maintainers will acknowledge the report and respond within **48 business hours** with an assessment and mitigation plan.

Please allow a reasonable remediation window before publishing details. Credit will be given to researchers who follow coordinated disclosure, unless they prefer to remain anonymous.

## Security scope

The following areas are considered high priority for this project:

### Transport and TLS

- Weak or disabled certificate verification in `ClienteHttpUrllib`.
- Incorrect hostname validation, SSL context reuse, or timeout handling.
- Leakage of TLS errors that exposes internal hostnames or credentials.

### Credential handling

- Exposure of `Authorization`, `Cookie`, or other sensitive headers in the UI, logs, error dialogs, CSV reports, or screenshots.
- Persistence of request headers or bodies beyond the lifetime of the run.
- Inclusion of secrets in crash output or packaged artifacts.

### Unsafe load generation

- Defaults or UI behavior that could amplify traffic unintentionally.
- Cancellation or shutdown paths that leave worker threads sending requests.
- Concurrency limits that can be bypassed to exhaust local resources.

### Desktop packaging

- PyInstaller bundle tampering, missing assets, or DLL search-order issues.
- Insecure temporary files, update mechanisms, or release artifacts.
- Privilege escalation through the system tray, file dialogs, or external links.

### Dependency and supply chain

- Vulnerable versions of PySide6, pytest, PyInstaller, or GitHub Actions.
- Workflows that expose repository secrets to untrusted code.

## Out of scope

- Vulnerabilities in third-party APIs or infrastructure that users choose to test.
- Reports that require the user to run a modified local build with disabled security controls.
- Missing hardening features that are already documented as limitations in [`README.md`](README.md#known-limitations-mvp-trade-offs).
- Denial-of-service claims caused by intentionally running high concurrency against an endpoint without authorization.

## Resolution process

1. **Triage:** reproduce the report, confirm impact, and assign a severity.
2. **Containment:** prepare a fix on a private branch and identify affected versions.
3. **Remediation:** add a regression test and update the changelog.
4. **Release:** publish a patched release and a GitHub Security Advisory.
5. **Disclosure:** publish coordinated details after users have had a reasonable window to upgrade.

## Hardening guidance for users

- Validate the target and obtain authorization before running any concurrency test.
- Use test credentials with the narrowest possible scope.
- Keep TLS verification enabled; do not test production systems with real customer data.
- Review exported CSV files before sharing them; they contain request status, headers, and error details.
- Download releases only from the official repository and verify the artifact when required by your organization.
