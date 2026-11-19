---
name: clip-cutter
description: Cut a picked moment from Vet's own job into a 1080x1920 draft with word-by-word captions and a hook. Use after moment-finder, or when the user says "cut it" or "make the clip".
---

# Clip cutter

Set `GTAVI_ROOT` to the repo root (`export GTAVI_ROOT="${CLAUDE_PLUGIN_ROOT}"` in Claude Code).

```bash
python3 "$GTAVI_ROOT/scripts/cut.py" "$CLIP_DESK_HOME/jobs/<id>" --pick <n> --layout fill|blur|facecam|react --hook "TEXT"
```

Windows virtualenv: `"%GTAVI_ROOT%\.venv\Scripts\python.exe"`.

- `fill`: crop the game video to fill the frame.
- `blur`: full video centered over a blurred copy.
- `facecam` or `react`: Vet's own camera plus the game. `react` is his face on top, not another streamer's. `--cam auto` or `--cam x:y:w:h`.

Captions use Archivo Black when fontconfig has it, then Anton, Bebas Neue, Liberation Sans, or Noto Sans.

Before running:

1. Get 3 hook options from `hook-writer` and use the best one.
2. Confirm the job manifest is his own recording (`source_owner` `VetTV`). If it is not, stop. Do not cut it.

After running:

1. The draft is `jobs/<id>/edits/clip_<n>.mp4` plus a `.json` sidecar with credit and source. Check 1080x1920, hook in the first seconds, readable captions.
2. Run `rule-check`. Fix and re-cut until it passes.
3. Prefer 7 to 30 seconds. End on the payoff.
4. Show the human the local file and the caption. Do not upload.
