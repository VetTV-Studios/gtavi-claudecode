---
name: live-mode
description: Record an allowlisted VetTV live stream and cut chat spikes. Use only for Vet's own channel, when he gives that live URL or says to record his stream.
---

# Live mode

Set `GTAVI_ROOT` to the repo root (`export GTAVI_ROOT="${CLAUDE_PLUGIN_ROOT}"` in Claude Code).

```bash
python3 "$GTAVI_ROOT/scripts/live.py" "https://www.youtube.com/@VetTVHandheld/live" --minutes 60
```

Windows virtualenv: `"%GTAVI_ROOT%\.venv\Scripts\python.exe"`.

The URL has to match `config/allowed_sources.json`, and `confirmed` has to be true. The placeholders in that file are not confirmed. A Twitch login is read for chat only when that login is on the allowlist. Any other channel, including a bigger streamer's, is refused before yt-dlp runs. The script passes `--` before the URL.

Before starting:

1. Read the allowlist with Vet. If `confirmed` is false, do not flip it yourself. Ask him to confirm the channels are his.
2. Refuse leaks, pirated copies, and "play early" streams.

While it runs:

1. Review new clips under the job's `live/` folder. Skip spoilers and nudity.
2. For each keeper, run `hook-writer`, then `clip-cutter` if it still needs a vertical master, then `rule-check`.
3. Send one message with the best 1 to 3 local files and captions. The human posts. Nothing is uploaded.

When it stops: list what was recorded and what was cut. Logging happens after the human actually publishes.
