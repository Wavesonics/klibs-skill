# klibs-skill

A [Claude Code](https://claude.com/claude-code) plugin that searches
[klibs.io](https://klibs.io) — JetBrains' directory of Kotlin Multiplatform
libraries — from natural-language requests.

The plugin is named **`klibs`**, with a single skill named **`find`**.
Invocation: `/klibs:find`.

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
klibs-skill/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name: "klibs")
├── skills/
│   └── find/
│       ├── SKILL.md         # Skill instructions for Claude (name: "find")
│       └── search.py        # Bundled klibs.io search script
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
git clone https://github.com/Wavesonics/klibs-skill.git
claude --plugin-dir ./klibs-skill
```

Once installed, invoke as `/klibs:find` — or just describe what you're looking
for and the skill's description will trigger Claude to use it automatically.

Run `claude plugin validate ./klibs-skill` before publishing changes.

## Install — as a standalone skill

Drop the inner skill folder into your Claude Code skills directory. The
directory name you choose becomes the slash-command name:

```bash
git clone https://github.com/Wavesonics/klibs-skill.git ~/Code/klibs-skill
ln -s ~/Code/klibs-skill/skills/find ~/.claude/skills/klibs-find
```

…or copy directly:

```bash
cp -r klibs-skill/skills/find ~/.claude/skills/klibs-find
```

Project-scoped install: put it under `.claude/skills/klibs-find/` inside your
project instead.

Restart Claude Code — skills are scanned at session start. Invoke as
`/klibs-find` (or whatever directory name you chose).

## Usage

Once installed, just ask:

> Is there a Kotlin multiplatform library for SQLite?

…or invoke the skill directly:

```
/klibs:find something for talking to gRPC from KMP
```

## Running the script directly

```bash
python3 skills/find/search.py "image loading" --limit 5
python3 skills/find/search.py "settings" --platforms common,native
python3 skills/find/search.py ktor --packages   # Maven packages instead of projects
```

Output is compact JSON on stdout.

## Privacy

The plugin collects no data and sends nothing to any server other than the
public klibs.io backend (`api.klibs.io`). See [PRIVACY.md](PRIVACY.md) for
full details.

## License

MIT — see [LICENSE](LICENSE).
