# Privacy Policy

_Last updated: 2026-05-22_

`klibs-skill` (the "Plugin") is a Claude Code plugin that searches
[klibs.io](https://klibs.io) for Kotlin Multiplatform libraries. This document
describes how the Plugin handles data.

## Summary

The Plugin does not collect, store, or transmit any personal data. It does not
include analytics, telemetry, advertising, tracking, or any third-party SDKs.
The Plugin is fully open source — see the repository for verification.

## What the Plugin does

When you invoke the Plugin, the Claude Code agent runs the bundled
`search.py` script on your local machine. The script makes a single outbound
HTTPS request per search:

- **Endpoint:** `https://api.klibs.io/search/projects` (or
  `https://api.klibs.io/search/packages`)
- **Method:** `GET`
- **Query parameters:** the search terms you (or Claude on your behalf) chose,
  plus optional `limit`, `page`, and `platforms` filters

The response — a JSON list of library metadata — is printed to standard output
and used by Claude to compose its reply. Nothing is written to disk, cached,
or sent anywhere else.

## What the Plugin does not do

- It does not contact any server other than `api.klibs.io`.
- It does not send your prompts, code, files, environment variables, or any
  other context to the Plugin author or any third party.
- It does not collect telemetry, usage statistics, crash reports, or
  identifiers of any kind.
- It does not require authentication and does not handle credentials.

## Third-party services

The Plugin queries the public klibs.io backend, which is operated by
JetBrains. The query terms you submit are sent to that backend as part of the
HTTPS request, and standard web-server logging (IP address, timestamp, request
URL) may apply on their side. The Plugin author has no relationship with
JetBrains and no access to those logs.

For information on how JetBrains handles data, see the
[JetBrains Privacy Policy](https://www.jetbrains.com/legal/docs/privacy/privacy/).

## Source code

The Plugin's full source is available at
<https://github.com/Wavesonics/klibs-skill>. You can audit the script at
[`skills/find/search.py`](skills/find/search.py) to verify the behavior
described above.

## Contact

For questions about this policy, open an issue at
<https://github.com/Wavesonics/klibs-skill/issues>.
