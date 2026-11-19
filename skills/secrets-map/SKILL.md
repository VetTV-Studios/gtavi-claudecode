---
name: secrets-map
description: Build a verified map of GTA 6 hidden spots from Vet's own transcripts. Use when the user wants secrets, hidden spots, or tip posts taken from his recordings.
---

# Secrets map

Entries live in `secrets.csv` (id, category, name, where, how, source_channel, source_url_with_timestamp, found_on, status, verified_by, notes). Categories: place, money, car, collectible, easter_egg, other. Status: unverified, verified, wrong.

Scan only jobs whose manifest says the recording is Vet's (`source_owner` `VetTV`). Do not scan someone else's VOD.

## Commands

Set `GTAVI_ROOT` to the repo root (`export GTAVI_ROOT="${CLAUDE_PLUGIN_ROOT}"` in Claude Code).

```bash
python3 "$GTAVI_ROOT/scripts/secrets_map.py" scan "$CLIP_DESK_HOME/jobs/<id>"
```

Windows virtualenv, from any directory:

```bat
"%GTAVI_ROOT%\.venv\Scripts\python.exe" "%GTAVI_ROOT%\scripts\secrets_map.py" scan "%CLIP_DESK_HOME%\jobs\<id>"
```

The interpreter is `.venv\Scripts\python.exe`. A path of `.venv\Scripts\python` without the extension is not the command this fork uses.

`--csv path` before the subcommand selects another file.

- `scan jobs/<id>`: reads that job's transcript and adds unverified leads. Duplicates and exploit-type mentions are skipped.
- `add --name N --where W --how H --category place --channel C --url U`: manual entry from Vet's own session.
- `verify <id> --by "<who/how>"`: only after the spot was checked in game or confirmed by official material.
- `wrong <id>`: the tip did not hold up.
- `posts --out secrets-posts.md`: HOW TO drafts from verified entries only.
- `map --out secrets.md`: table grouped by category.

## Flow

1. `scan` a job he marked as his own. Rewrite the auto name, where, and how into a real tip.
2. He checks it in the game. `verify` or `wrong`.
3. `posts` writes drafts. Show them to him. He posts. The script does not upload.

## Rules

1. Verified entries only, when drafting posts. Unverified is a lead.
2. Credit the page (`🎥 @[HANDLE]`). The find came from his recording, not from another creator.
3. No glitches, exploits, money glitches, duplication, leaks, or "play early."
4. Do not post the raw transcript quote.
5. No story spoilers in launch week. Never imply the page is Rockstar. Use "GTA 6". X posts have no hashtags.
