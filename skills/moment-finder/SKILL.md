---
name: moment-finder
description: Find clip moments in Vet's own GTA 6 recording. Use when the user gives a local file, or an allowlisted URL of their own channel, and wants highlights.
---

# Moment finder

Set `GTAVI_ROOT` to the repo root (`export GTAVI_ROOT="${CLAUDE_PLUGIN_ROOT}"` in Claude Code).

Local file (the default). `--own` is required and means the file is Vet's recording:

```bash
python3 "$GTAVI_ROOT/scripts/moments.py" /path/to/vet_stream.mp4 --own --top 8
```

Windows virtualenv: `"%GTAVI_ROOT%\.venv\Scripts\python.exe" "%GTAVI_ROOT%\scripts\moments.py" ...`

An allowlisted URL works only after Vet sets `confirmed` to true in `config/allowed_sources.json` and the URL is one of his channels. Any other URL is refused. Do not pass someone else's video "just to see."

The script writes `$CLIP_DESK_HOME/jobs/<id>/candidates.md` and a `manifest.json` with `source_owner`, `own_recording`, and `credit`. Signals: transcript (faster-whisper), loudness, and, when the source is an allowlisted YouTube VOD, the replay heatmap and chat. A missing signal is skipped, not faked.

Then:

1. Read `candidates.md` and show each candidate: number, start-end, length, why it scored, transcript line.
2. Drop spoilers for story moments in launch week, nudity, and anything that looks like a leak.
3. Recommend the best 3 and say what hook angle each suggests.
4. Next step: `clip-cutter` with `--pick <n>`.

The manifest credit is `VetTV` unless `--credit` set another line. That credit is for the post caption. Do not add a second creator.
