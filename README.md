<div align="center">

<img src="docs/logo.png" width="300" alt="gtavi-claudecode logo">

<h1 align="center">gtavi-claudecode</h1>

<p align="center"><b>VetTV fork.</b> Cut Vet's own GTA 6 stream recordings into 9:16 drafts for Shorts, Reels, and X.</p>

<p align="center">Unofficial fan project. Not affiliated with Rockstar Games, Take-Two, or Anthropic.<br>Upstream pin: <a href="https://github.com/Bodila51/gtavi-claudecode/commit/dd95d393c6f74fe2ac14b0239f8826691e5dcb0e">Bodila51/gtavi-claudecode@dd95d39</a>. See <a href="SECURITY.md">SECURITY.md</a>.</p>

</div>

This fork does not search for other people's streams, does not download them, and does not upload or schedule posts. Clips stay on disk as drafts. A person publishes them by hand.

Other-creator clipping is how a VetTV channel took a copyright strike. The scripts refuse that path unless a URL is on the confirmed allowlist, and the allowlist ships turned off.

## Confirm your channels first

`config/allowed_sources.json` is seeded with placeholders:

- `https://www.youtube.com/@VetTVHandheld`
- `https://x.com/The_VetX`
- a Twitch login of `REPLACE_WITH_VETS_TWITCH_LOGIN`, which is ignored

`confirmed` is `false`. Remote URLs are refused until you check that every entry is an account you own, edit anything that is wrong, and set `confirmed` to `true`. Leave it false if you only cut local files.

A local recording is accepted only when you mark it as yours:

```bash
python3 "$GTAVI_ROOT/scripts/moments.py" /path/to/vet_stream.mp4 --own --top 8
```

`--own` means "this file is my recording." The job manifest then stores `source_owner: "VetTV"`, `own_recording: true`, and a credit. `check.py` fails clips that do not have that mark or an allowlisted URL.

You can pass the same fields in a JSON manifest instead of `--own`:

```json
{"own_recording": true, "source_owner": "VetTV", "credit": "VetTV"}
```

## Run the scripts

The scripts are plain Python. They do not need Claude Code.

```bash
export GTAVI_ROOT="/path/to/gtavi-claudecode"   # repo root
export CLIP_DESK_HOME="/path/to/gtavi-jobs"     # where jobs/ is written; defaults to the current directory
```

Inside Claude Code you can point the same variable at the plugin directory:

```bash
export GTAVI_ROOT="${CLAUDE_PLUGIN_ROOT}"
```

Windows, from a virtualenv created in the repo root (note `Scripts\python.exe`, not `Scripts\python`):

```bat
set GTAVI_ROOT=C:\path\to\gtavi-claudecode
set CLIP_DESK_HOME=C:\path\to\gtavi-jobs
"%GTAVI_ROOT%\.venv\Scripts\python.exe" "%GTAVI_ROOT%\scripts\moments.py" C:\path\to\vet_stream.mp4 --own --top 8
```

Without a virtualenv, `py -3` is the Windows launcher. On Linux and macOS the commands use `python3`.

```bash
python3 "$GTAVI_ROOT/scripts/moments.py" /path/to/vet_stream.mp4 --own --top 8 --max-minutes 240
python3 "$GTAVI_ROOT/scripts/cut.py" "$CLIP_DESK_HOME/jobs/<id>" --pick 2 --layout react --cam auto --title "Hidden garage" --captions word
python3 "$GTAVI_ROOT/scripts/check.py" "$CLIP_DESK_HOME/jobs/<id>/edits/clip_2.mp4" --caption "Hidden garage"
python3 "$GTAVI_ROOT/scripts/live.py" "https://www.youtube.com/@VetTVHandheld/live" --minutes 60
```

`live.py` records only after the URL passes the allowlist. It passes `--` before the URL to yt-dlp.

Captions use **Archivo Black** when that font is installed (it is on the VetTV Linux machines). Otherwise the cutter tries Anton, Bebas Neue, Liberation Sans, then Noto Sans. With no fontconfig (typical on Windows) it looks for those font files and, if none are there, uses Arial Black or Arial. It does not ask for Archivo Black unless the font was actually found.

## Install

This repo does not run `sudo apt` or `pip install -U`. Install ffmpeg yourself from your OS packages. It must include ffprobe. Then, if you want the Python packages:

```bash
python3 -m pip install --require-hashes -r "$GTAVI_ROOT/requirements.txt"
```

Pinned directs: `faster-whisper==1.2.1`, `numpy==2.5.5`, `requests==2.34.2`, `opencv-python-headless==5.1.0.95`, `yt-dlp==2026.10.26`. Hashes for those and their dependencies are in `requirements.txt`. Transcription is CPU-only here. A 12-minute video is on the order of 5 minutes with the `small` Whisper model. Use `--max-minutes` or pre-trim a long stream.

The YuNet face model for `--cam auto` is vendored and hash-checked. Manual `--cam x:y:w:h` does not need it. See `SECURITY.md`.

## What you can ask an agent to do

| Skill | What it does |
|---|---|
| `setup` | Creates the page folder. It does not install packages. |
| `moment-finder` | Scores moments in your own recording. |
| `live-mode` | Records an allowlisted live URL of yours and cuts chat spikes. |
| `clip-cutter` | Renders a 1080x1920 draft with captions and a hook. |
| `hook-writer` | Three hook options for your own footage. |
| `rule-check` | Fails bad specs, banned phrases, missing credit, or a source that is not yours. |
| `questions-to-posts` | Clusters public questions and your comments into HOW TO drafts. No video download. |
| `secrets-map` | Hidden-spot notes taken from your own transcripts. |
| `cheat-codes` | Reported cheat carousel from the checked list. Not Rockstar-official until you verify it in game. |
| `playbook` | Daily routine for your own recordings and official news. |
| `learning-loop` | Scoreboard from numbers you paste. No payout scraper. |

Nothing in this table uploads.

## Rules

No leaks, no "play early" or "free download" posts, no piracy, no mod menus, no money glitches, no "AI gameplay" passed off as real, no fake news, and no pretending to be Rockstar. Do not clip other creators. Credit on your own drafts is the `credit` field (`VetTV` unless you set another line).

MIT license. Upstream copyright remains with Bodila51. The YuNet file is Apache-2.0.
