---
name: learning-loop
description: Log posts Vet actually published and learn from numbers he pastes, using scoreboard.csv and learning.md. Use after a post goes out, at 12/24/72 hour reads, or for the daily or weekly review.
---

# Learning loop

Files in the page folder: `scoreboard.csv` (one row per post), `learning.md` (Wins, Losses, Current Rules), `log.md`.

There is no payout ledger in this fork. Do not estimate earnings and do not scrape campaign sites.

## Rules

1. Real numbers only. Ask the human to paste metrics. If a number is not available, leave it blank. Never guess.
2. Log a post when the human says it went out: post_id, date, time, platform, pillar, format, hook, length_sec, credit, test_name.
3. Reads at 12h, 24h, and 72h fill views_12h, views_24h, views_72h, then likes, shares, replies, saves, followers_at_read.
4. One test per day. Change one variable only (hook style, length, posting time, caption length, still vs clip). Name it in `test_name`.
5. No verdict under 24 hours. Prefer the 72h read if the post is still moving.

## Daily (evening)

Best and worst post, one lesson written as a rule. Append to `learning.md`. Pick tomorrow's one test.

## Weekly

Top 3 and bottom 3 posts, median views by pillar, by time slot, and by platform. Double down on what is above median. Rework what stayed below median for a full week. Update the page's `playbook.md` with what changed. Send the human a short summary.

The footage behind every row is Vet's own, or an official news post. Do not add a row for someone else's clip.
