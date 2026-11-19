"""VetTV source allowlist.

Remote clipping is off until config/allowed_sources.json has "confirmed": true
and the URL's channel is listed there. Local files are accepted only when the
job manifest says the recording is Vet's own.
"""
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from common import ytdlp_json

OWNER = "VetTV"
REPO = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO / "config" / "allowed_sources.json"
REMOTE_HOSTS = ("youtube.com", "youtu.be", "twitch.tv", "x.com", "twitter.com")


def load_allowlist(path=None):
    path = Path(path or CONFIG_PATH)
    if not path.is_file():
        return {"confirmed": False, "owner": OWNER, "channels": [], "twitch_logins": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a JSON object")
    return data


def _hostname(url):
    try:
        host = (urlparse(url).hostname or "").lower().rstrip(".")
    except ValueError:
        return ""
    if host.startswith("www.") or host.startswith("m."):
        host = host.split(".", 1)[1]
    return host


def host_allowed(url):
    host = _hostname(url)
    return any(host == base or host.endswith("." + base) for base in REMOTE_HOSTS)


def twitch_login_from_url(url):
    host = _hostname(url)
    if host != "twitch.tv":
        return None
    parts = [p for p in urlparse(url).path.split("/") if p]
    if not parts or parts[0].lower() in ("videos", "directory", "search"):
        return None
    login = parts[0]
    if login.startswith("#") or not _login_ok(login):
        return None
    return login.lower()


def _login_ok(login):
    login = (login or "").strip().lower().lstrip("#")
    return bool(login) and all(c in "abcdefghijklmnopqrstuvwxyz0123456789_" for c in login) and len(login) <= 25


def _channel_rules(cfg):
    """Path prefixes, @handles, and exact channel ids. Display names are not rules."""
    prefixes, handles, ids = [], [], []
    for ch in cfg.get("channels") or []:
        if not isinstance(ch, dict) or ch.get("placeholder") is True:
            continue
        raw = []
        for key in ("url", "handle"):
            val = ch.get(key)
            if isinstance(val, str):
                raw.append(val)
        for val in ch.get("match") or []:
            if isinstance(val, str):
                raw.append(val)
        ident = ch.get("id")
        if isinstance(ident, str) and ident.strip():
            ids.append(ident.strip().lower())
        for val in raw:
            val = val.strip()
            if not val:
                continue
            low = val.lower()
            if low.startswith("http://") or low.startswith("https://"):
                host = _hostname(val)
                path = urlparse(val).path or ""
                low = f"{host}{path}".rstrip("/")
            if low.startswith("@"):
                handle = low[1:]
                if handle:
                    handles.append(handle)
                continue
            if "/" in low:
                prefixes.append(low.rstrip("/"))
                tail = low.rstrip("/").split("/")[-1]
                if tail.startswith("@"):
                    handles.append(tail[1:])
            elif len(low) >= 6:
                handles.append(low.lstrip("@"))
    return prefixes, handles, ids


def _path_prefix_match(blob, prefix):
    """True only when blob is the channel path or a slash-separated child of it.

    `@VetTVHandheld-Clips` and `The_VetX_news` do not match the shorter names.
    """
    blob = (blob or "").lower().rstrip("/")
    prefix = (prefix or "").lower().rstrip("/")
    if len(prefix) < 4:
        return False
    return blob == prefix or blob.startswith(prefix + "/")


def _handle_segment(blob, handle):
    """Match /@handle as a whole path segment. A longer handle such as @name-clips does not match."""
    handle = (handle or "").lower().lstrip("@")
    if len(handle) < 2 or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_" for c in handle):
        return False
    blob = (blob or "").lower()
    token = "/@" + handle
    start = 0
    while True:
        i = blob.find(token, start)
        if i < 0:
            return False
        end = i + len(token)
        if end >= len(blob) or blob[end] == "/":
            return True
        start = i + 1


def _url_blob(url):
    host = _hostname(url)
    path = urlparse(url).path or ""
    return f"{host}{path}".lower()


def url_matches(url, cfg):
    if not host_allowed(url):
        return False
    blob = _url_blob(url)
    prefixes, handles, _ids = _channel_rules(cfg)
    if any(_path_prefix_match(blob, prefix) for prefix in prefixes):
        return True
    if any(_handle_segment(blob, handle) for handle in handles):
        return True
    login = twitch_login_from_url(url)
    return bool(login) and login in _twitch_logins(cfg)


def meta_matches(info, cfg):
    """Match channel URLs and exact ids. A display name that merely contains the handle does not count."""
    if not isinstance(info, dict):
        return False
    for key in ("webpage_url", "original_url", "channel_url", "uploader_url"):
        val = info.get(key)
        if isinstance(val, str) and val.strip() and url_matches(val, cfg):
            return True
    _prefixes, _handles, ids = _channel_rules(cfg)
    if not ids:
        return False
    for key in ("uploader_id", "channel_id"):
        val = info.get(key)
        if isinstance(val, str) and val.strip().lower() in ids:
            return True
    return False


def _twitch_logins(cfg):
    found = []
    for item in cfg.get("twitch_logins") or []:
        if isinstance(item, str):
            login = item
            placeholder = False
        elif isinstance(item, dict):
            placeholder = item.get("placeholder") is True
            login = item.get("login") or ""
        else:
            continue
        if placeholder:
            continue
        login = str(login).strip().lower().lstrip("#")
        if _login_ok(login):
            found.append(login)
    return found


def twitch_login_allowed(login, cfg=None):
    cfg = load_allowlist() if cfg is None else cfg
    if cfg.get("confirmed") is not True:
        return False, "allowlist is not confirmed (config/allowed_sources.json)"
    login = (login or "").strip().lower().lstrip("#")
    if not _login_ok(login):
        return False, "Twitch login is invalid"
    if login in _twitch_logins(cfg):
        return True, "Twitch login is allowlisted"
    return False, f"Twitch login {login} is not allowlisted"


def authorize_url(url):
    """Return yt-dlp metadata for an allowlisted URL. Exit before any network otherwise."""
    if not host_allowed(url):
        sys.exit(
            "refusing URL: only YouTube, Twitch, and X hosts can be considered, and only for "
            "allowlisted VetTV channels. Use a local recording of your own stream."
        )
    cfg = load_allowlist()
    if cfg.get("confirmed") is not True:
        sys.exit(
            "refusing URL: config/allowed_sources.json has confirmed set to false. "
            "Confirm every listed channel is yours and set confirmed to true, or pass a local file with --own."
        )
    info = ytdlp_json(url)
    if url_matches(url, cfg) or meta_matches(info, cfg):
        return info
    login = twitch_login_from_url(url)
    if login and twitch_login_allowed(login, cfg)[0]:
        return info
    sys.exit("refusing URL: it is not an allowlisted VetTV channel. Other creators' streams cannot be clipped.")


def clip_source_ok(meta):
    """Whether a cut.py sidecar describes Vet's own footage."""
    if not isinstance(meta, dict) or not meta:
        return False, "no sidecar metadata"
    owner = str(meta.get("source_owner", "")).strip()
    if owner != OWNER:
        return False, f"source_owner is {owner or 'empty'}; need {OWNER}"
    if meta.get("source_kind") == "local" and meta.get("own_recording") is True:
        return True, "local file marked as Vet's own recording"
    if meta.get("source_kind") == "url":
        cfg = load_allowlist()
        if cfg.get("confirmed") is not True:
            return False, "allowlist is not confirmed"
        url = str(meta.get("source_url") or "")
        if not url or not host_allowed(url):
            return False, "source URL host is not YouTube, Twitch, or X"
        if url_matches(url, cfg):
            return True, "source URL is allowlisted"
        probe = {
            "webpage_url": url,
            "channel_url": meta.get("channel_url") or "",
            "uploader_url": meta.get("uploader_url") or "",
            "channel": meta.get("source_channel") or "",
            "uploader": meta.get("source_channel") or "",
            "uploader_id": meta.get("uploader_id") or "",
            "channel_id": meta.get("channel_id") or "",
        }
        if meta_matches(probe, cfg):
            return True, "source channel is allowlisted"
        login = twitch_login_from_url(url)
        if login and twitch_login_allowed(login, cfg)[0]:
            return True, "Twitch login is allowlisted"
        return False, "source URL is not an allowlisted VetTV channel"
    return False, "source is not a marked local recording or an allowlisted URL"


def own_mark(own_flag, credit, manifest):
    """Build the job-manifest ownership fields. Local files must opt in."""
    recording = False
    owner = ""
    cred = ""
    if manifest:
        data = json.loads(Path(manifest).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            sys.exit("manifest must be a JSON object")
        if data.get("own_recording") is True:
            owner = str(data.get("source_owner", "")).strip()
            if owner != OWNER:
                sys.exit(f'manifest own_recording requires source_owner "{OWNER}"')
            recording = True
            cred = str(data.get("credit") or "").strip()
    if own_flag:
        recording = True
        owner = OWNER
        if credit:
            cred = credit.strip()
    if recording and not cred:
        cred = OWNER
    if recording:
        return {"own_recording": True, "source_owner": owner, "credit": cred}
    return {"own_recording": False, "source_owner": "", "credit": ""}
