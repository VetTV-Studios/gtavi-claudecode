---
name: rule-check
description: Check a finished VetTV draft for format, credit, ownership, and banned phrases before the human posts it. Use before every publish decision.
---

# Rule check

Set `GTAVI_ROOT` to the repo root (`export GTAVI_ROOT="${CLAUDE_PLUGIN_ROOT}"` in Claude Code).

```bash
python3 "$GTAVI_ROOT/scripts/check.py" "$CLIP_DESK_HOME/jobs/<id>/edits/clip_<n>.mp4" --caption "text"
```

Windows virtualenv: `"%GTAVI_ROOT%\.venv\Scripts\python.exe"`.

The sidecar `clip_<n>.json` next to the MP4 is required. The script fails when:

- the frame is not about 1080x1920 at about 30 fps, or audio is missing, or the length is outside the default 7 to 60 seconds
- `credit` is empty (this is the check restored after upstream commit `2aee0c6` removed it)
- `source_owner` is not `VetTV`, the file is not a local recording marked `own_recording`, and the URL is not on the confirmed allowlist
- the hook or caption contains leak, play early, free download, mod menu, money glitch, AI gameplay, or the other banned phrases

An optional `--campaign rules.md` can add hashtags, a mention, or a tighter length. There is no campaign finder in this fork. Do not go looking for paid clipping campaigns.

Then:

1. Show PASS or FAIL per check.
2. On FAIL, fix the cause and re-run. A failed ownership check means the clip is not ours. Delete the draft. Do not hunt for a credit line to paste over someone else's footage.
3. Read the caption yourself. No invented facts, no "official" wording.
4. After a pass, send the human the local file, caption, and credit, and wait for "yes". The human posts it. Never auto-upload.
