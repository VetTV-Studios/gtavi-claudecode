# Security

This fork clips Vet's own GTA 6 stream recordings into local draft Shorts, Reels, and X clips. It does not post, upload, or schedule anything. Finished files stay under `jobs/<id>/edits/` until a person publishes them by hand, outside this repo.

## Upstream pin

The fork is pinned to [Bodila51/gtavi-claudecode](https://github.com/Bodila51/gtavi-claudecode) commit `dd95d39` (`dd95d393c6f74fe2ac14b0239f8826691e5dcb0e`). That commit was reviewed before these changes. Pull later upstream commits only after a fresh review of the diff. Do not install the plugin from the upstream marketplace.

## Own footage only

`config/allowed_sources.json` ships with `confirmed: false` and placeholder entries for `youtube.com/@VetTVHandheld` and `x.com/The_VetX`. Those placeholders are not a confirmation that the accounts are Vet's. Remote URLs are refused until Vet checks every entry and sets `confirmed` to true.

- `moments.py` and `live.py` accept a URL only after that allowlist check. `yt-dlp` is invoked with `--` before the URL.
- A local file is accepted only with `--own`, or a manifest JSON whose `own_recording` is true and whose `source_owner` is `VetTV`.
- `check.py` fails a clip that has no creator credit, and fails a clip whose sidecar is not an allowlisted VetTV URL or a local file marked as Vet's own.
- `twitch.py` is an anonymous read-only chat client. It joins only an allowlisted login. The Twitch web client id, GraphQL stream search, and the Kick browser user-agent are gone (they lived in the removed stream-discovery code).

## Removed on purpose

These parts found or repackaged other creators' content, or sent caption text to unofficial translation endpoints:

- `scripts/streams.py`, `scripts/trends.py`, `scripts/payouts.py`, `scripts/translate.py`
- skills `stream-finder`, `trend-radar`, `twitch-reaction`, `campaign-finder`, `multilang`

`questions.py` still reads public Reddit JSON for topic ideas. It does not download video. The react layout in `cut.py` still works on Vet's own facecam footage.

## Dependencies and the face model

Install Python packages only with hashes:

```bash
python3 -m pip install --require-hashes -r requirements.txt
```

Do not run `pip install -U` against this file. The direct pins are `faster-whisper==1.2.1`, `numpy==2.5.5`, `requests==2.34.2`, `opencv-python-headless==5.1.0.95`, and `yt-dlp==2026.10.26` (base package, no `[default]` extra). Transitive pins are in the same file. `yt-dlp-ejs` is omitted because the default path is a local file.

YuNet (`models/face_detection_yunet_2023mar.onnx`) is the opencv_zoo file at commit `f12e12798e8314f7c074a6656816c048dcc95b7a`.

- SHA-256: `8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4`
- Size: 232589 bytes
- `facecam.py` checks that checksum before use and will not fall back to an unverified download.

The model is Apache-2.0. See `models/NOTICE` and `models/LICENSE`.
