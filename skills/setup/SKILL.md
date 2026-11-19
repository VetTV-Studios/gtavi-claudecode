---
name: setup
description: First-run setup for the VetTV GTA 6 clip desk. Use when the user says "set up" or "start", or when the page folder does not exist yet. Does not install packages.
---

# Setup

Do the work yourself. Ask the human only what is listed here. Do not run `sudo apt`, `brew install`, `winget install`, or `pip install`. If ffmpeg or a Python package is missing, stop and name the command the human can run. The approved pip command is `python3 -m pip install --require-hashes -r "$GTAVI_ROOT/requirements.txt"`. Never `pip install -U`.

`GTAVI_ROOT` is the repository root. In Claude Code, `export GTAVI_ROOT="${CLAUDE_PLUGIN_ROOT}"` is enough. Jobs go under `CLIP_DESK_HOME` (or the current directory).

## 1. Check tools (do not install them)

Check `ffmpeg -version`, `ffprobe -version`, and `python3 -c "import faster_whisper, numpy, cv2"`. Report what is missing. Stop there if the human has not installed it.

## 2. Ask at most 4 questions, in ONE numbered message

1. Page name and handle (@).
2. Platforms (for example X, Instagram Reels, TikTok, YouTube Shorts).
3. Niche angle (one lane: tips and hidden spots, fast news, funny moments, cars and customization).
4. Time zone.

If the human already gave an answer, do not ask it again. Skip the message if all four are known.

## 3. Show the plan, ask ONE "yes"

List the folder you will create and the files in it, then ask for a single "yes". After the yes, create (in the current directory, in a folder named after the page):

- `playbook.md` (copy from `$GTAVI_ROOT/skills/playbook/references/playbook.md` and fill the [BRACKETED] fields with the answers)
- `facts.md` (verified facts only, each with an official source link)
- `idea-bank.md`, `watchlist.md`, `log.md`
- `scoreboard.csv` with this header line only:
  `post_id,date,time,platform,pillar,format,hook,length_sec,credit,views_12h,views_24h,views_72h,likes,reposts_or_shares,replies_or_comments,saves_or_bookmarks,followers_at_read,test_name,notes`
- `learning.md` with headings Wins, Losses, Current Rules
- `takedowns.md`
- folders `media/official`, `media/raw`, `media/edits`

`media/raw` is for Vet's own recordings only. Do not put anyone else's video there.

## 4. Finish

Tell the human, in 3 lines: where the folder is, that installs were not run by this skill, and the next step (put a local recording through `moment-finder` with `--own`). Remind them that clips stay local drafts and that nothing is uploaded.
