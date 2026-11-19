---
name: questions-to-posts
description: Turn repeated questions from public Reddit threads and from comments on Vet's own posts into HOW TO drafts. Use when the user asks what people are asking. Does not download video.
---

# Questions to posts

Finds questions people keep asking, checks `facts.md`, and drafts HOW TO posts from verified facts only. This is research. It is not a source of footage.

## Command

Set `GTAVI_ROOT` to the repo root (`export GTAVI_ROOT="${CLAUDE_PLUGIN_ROOT}"` in Claude Code). Run from the page folder (where `facts.md` lives):

```bash
python3 "$GTAVI_ROOT/scripts/questions.py" --subs GTA6,GTA,GrandTheftAutoV --days 3 --comments comments.txt --out questions.md
```

Windows virtualenv: `"%GTAVI_ROOT%\.venv\Scripts\python.exe"`.

- `--comments comments.txt`: comments pasted from Vet's own posts, one per line. This path works with no network.
- `--facts facts.md` (default), `--ideas idea-bank.md` (default), `--top 25`, `--min-count 1`.
- Public Reddit JSON is optional, one request per second. If Reddit blocks it, use the comments file and run again.

## What you get

- `questions.md`: clusters, each with a question, a count, and either `answer found in facts.md` or `UNANSWERED`.
- A HOW TO draft per answered cluster.
- Unanswered clusters appended to `idea-bank.md` as research tasks.

## After the run

1. Read each draft. Fix step order. Keep the wording true to the fact.
2. Unanswered clusters need an official source in `facts.md` before they can be drafted again.
3. Show the human the draft. They post it. Do not upload.

## Rules

1. Facts only from official sources, or from Vet's own verified session, logged in `facts.md` with the link.
2. Never invent steps, numbers, dates, or menu names.
3. No leaks, rumors, piracy, exploits, or "play early," even if people ask.
4. Do not quote or name Reddit users. If a draft refers to a find from Vet's own stream, credit the page.
5. Never imply the page is Rockstar. Use "GTA 6".
6. Keep all-caps to the hook line only.
