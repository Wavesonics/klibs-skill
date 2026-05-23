# find-kotlin-lib

A [Claude Code](https://claude.com/claude-code) skill / plugin that searches
[klibs.io](https://klibs.io) — JetBrains' directory of Kotlin Multiplatform
libraries — from natural-language requests.

Ask things like *"is there a KMP library for parsing TOML?"* or
*"find me a Kotlin image-loading library that works on iOS"* and Claude will
translate the request into klibs.io queries, run them, and recommend the best
matches with version, license, and platform info.

## How it works

The skill bundles a small Python script (`search.py`) that calls the public
klibs.io backend at `https://api.klibs.io/search/projects`. Claude picks the
search terms, applies platform filters when relevant, and synthesizes a ranked
recommendation from the returned JSON.

Valid platform filters: `androidJvm, common, js, jvm, native, wasm`
(`native` covers iOS / macOS / Linux / Windows KMP native targets).

## Repository layout

```
find-kotlin-lib/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest (for plugin install)
├── skills/
│   └── find-kotlin-lib/
│       ├── SKILL.md             # Skill instructions for Claude
│       └── search.py            # Bundled klibs.io search script
├── requirements.txt
├── LICENSE
└── README.md
```

## Requirements

- Python 3.9+
- `requests` (`pip install -r requirements.txt`)

## Install — as a Claude Code plugin (recommended)

Use the `/plugin` command inside Claude Code to install from this repository,
or load it locally during development:

```bash
git clone https://github.com/Wavesonics/find-kotlin-lib.git
claude --plugin-dir ./find-kotlin-lib
```

Once installed, invoke explicitly with `/find-kotlin-lib:find-kotlin-lib` or
just describe what you're looking for — the description in `SKILL.md` triggers
Claude to use it.

Run `claude plugin validate ./find-kotlin-lib` before publishing changes.

## Install — as a standalone skill

Drop the inner skill folder into your Claude Code skills directory. Either
symlink (so edits land in this repo):

```bash
git clone https://github.com/Wavesonics/find-kotlin-lib.git ~/Code/find-kotlin-lib
ln -s ~/Code/find-kotlin-lib/skills/find-kotlin-lib ~/.claude/skills/find-kotlin-lib
```

…or copy the skill folder directly:

```bash
cp -r find-kotlin-lib/skills/find-kotlin-lib ~/.claude/skills/find-kotlin-lib
```

Project-scoped install: put it under `.claude/skills/find-kotlin-lib/` inside
the project instead.

Restart Claude Code — skills are scanned at session start. Standalone install
invokes as `/find-kotlin-lib` (no namespace).

## Usage

Once installed, just ask:

> Is there a Kotlin multiplatform library for SQLite?

…or invoke the skill directly:

```
/find-kotlin-lib:find-kotlin-lib something for talking to gRPC from KMP
```

## Running the script directly

```bash
python3 skills/find-kotlin-lib/search.py "image loading" --limit 5
python3 skills/find-kotlin-lib/search.py "settings" --platforms common,native
python3 skills/find-kotlin-lib/search.py ktor --packages   # Maven packages instead of projects
```

Output is compact JSON on stdout.

## License

MIT — see [LICENSE](LICENSE).
