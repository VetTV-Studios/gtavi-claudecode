---
name: playbook
description: Run the daily VetTV GTA 6 routine from the own-stream playbook. Use when the user says "daily routine", "what do I do today", "run the page", asks about the kickoff, content pillars, posting slots, or safety rules.
---

# Playbook

1. Read `$GTAVI_ROOT/skills/playbook/references/playbook.md`. If the page folder has its own `playbook.md`, read that one instead (it is the customized copy). In Claude Code, `GTAVI_ROOT` may be `${CLAUDE_PLUGIN_ROOT}`.
2. If the page folder does not exist, run the `setup` skill first.
3. Find where the page is: the kickoff day (section 17) or the normal daily schedule (section 9). Check `log.md` and `scoreboard.csv`.
4. Run the day:
   - Official sources first (section 5). Record each verified fact with its link in `facts.md`.
   - Clip only Vet's own recordings: `moment-finder`, then `clip-cutter`, with hooks from `hook-writer`. `live-mode` only for an allowlisted VetTV URL.
   - Gate every clip with `rule-check`.
   - Log and learn with `learning-loop`.
5. Send the human ONE message with the exact caption, the local media path, and the credit for each draft. They reply "yes" if they want to publish it themselves. Never upload, never call a social API, never schedule a post from this repo.
6. End the day with the short report (section 16): what was drafted, what the human published, one lesson, tomorrow's test.

Hard rules: no leaks, no "play early", no piracy, no GTA Online money or AFK bots, no invented facts or numbers, no other creators' footage, no earnings promises. Anything outside the normal mix needs the human's yes first.
