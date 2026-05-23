---
name: find-kotlin-lib
description: Search klibs.io for Kotlin / Kotlin Multiplatform libraries from a natural-language description. Use when the user asks "is there a KMP library for X", "find me a Kotlin library that does Y", or names a capability and wants library suggestions with coordinates / platform support.
---

# find-kotlin-lib

Translate the user's natural-language request into one or more klibs.io queries, run them with the bundled `search.py`, then synthesize a short ranked recommendation.

## Tool

`search.py` lives next to this `SKILL.md`. It hits `https://api.klibs.io` and prints a compact JSON array.

Resolve the script path each session — it differs by install mode:

- **Plugin install**: `"$CLAUDE_PLUGIN_ROOT/skills/find-kotlin-lib/search.py"`
- **Standalone install**: `"$HOME/.claude/skills/find-kotlin-lib/search.py"` (or wherever the `.claude/skills/find-kotlin-lib/` dir lives — project-scoped installs put it under the project's `.claude/`).

Invocation:

```
python3 "<path-to-search.py>" "<query>" [--limit N] [--page N] [--platforms p1,p2] [--packages]
```

- `<query>` — keyword string. klibs.io does keyword + relevance ranking, not semantic search, so favor terse domain terms ("image loading", "sqlite", "http client") over full sentences.
- `--limit` — default 5. Bump to 10 if the first pass is thin.
- `--platforms` — comma-separated subset of `androidJvm, common, js, jvm, native, wasm`. `native` covers iOS / macOS / Linux / Windows KMP targets — there is no separate `ios` value.
- `--packages` — search Maven packages (groupId/artifactId) instead of projects. Use when the user already named a project and wants the specific artifact, or asks for "the gradle dependency for X".

Default mode (projects) returns: `name, description, scmLink, scmStars, licenseName, latestReleaseVersion, platforms, tags`.
Packages mode returns: `groupId, artifactId, description, scmLink, licenseName, latestVersion, platforms, targets`.

## How to query

1. **Extract 1–3 candidate queries** from the user's request. Try the most specific first, then a broader fallback if results are empty or off-topic. Examples:
   - "I need to render markdown in Compose Multiplatform" → `markdown compose`, then `markdown` as fallback.
   - "Something for talking to gRPC from KMP" → `grpc`.
   - "Local key-value storage that works on iOS too" → `settings key value` with `--platforms common,native`; fallback `preferences`.
2. **Apply `--platforms`** only when the user explicitly constrains targets (iOS, Android-only, web, server, etc.). Don't over-filter — many useful libs list `common` plus a subset.
3. **Run searches in parallel** when you have multiple candidate queries — one Bash call per query, batched in a single message.
4. If the first batch is empty or irrelevant, drop a keyword and retry. Do **not** burn more than ~3 query attempts before reporting what you found.

## How to respond

Recommend the top 1–3 hits. For each, give:

- Library name + `scmLink`
- One-line summary of what it does (paraphrase the description, don't dump it)
- Latest version, license, supported platforms
- Why it fits (or caveats — e.g. "no iOS support", "last release 2 years ago")

If the user is in a Gradle project, offer the dependency coordinate. Run a `--packages` search to get the exact `groupId:artifactId:version` rather than guessing.

If nothing relevant turns up after a couple of attempts, say so plainly and suggest the next-best avenue (Maven Central search, GitHub topics, etc.) rather than recommending a poor match.
