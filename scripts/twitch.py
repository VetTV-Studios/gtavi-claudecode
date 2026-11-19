"""Anonymous Twitch chat for an allowlisted channel.

irc_chat() reads chat as a justinfan nick with no password and no API key.
It connects only when the login is in config/allowed_sources.json.
There is no stream search and no Twitch web client id.
"""
import json
import random
import re
import socket
import ssl
import sys
import threading
import time

from allowlist import twitch_login_allowed

try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

_LOGIN = re.compile(r"[a-z0-9_]{1,25}")


def _parse_privmsg(line):
    """'@tags :user!user@user.tmi.twitch.tv PRIVMSG #chan :text' -> (user, text) or None"""
    tags = ""
    if line.startswith("@"):
        tags, _, line = line.partition(" ")
    if " PRIVMSG " not in line:
        return None
    prefix, _, rest = line.partition(" PRIVMSG ")
    user = prefix.lstrip(":").split("!")[0]
    for t in tags.lstrip("@").split(";"):
        if t.startswith("display-name=") and t[13:]:
            user = t[13:]
    _, _, text = rest.partition(" :")
    return user, text.strip()


def irc_chat(channel, out_path, stop_event=None, host="irc.chat.twitch.tv", port=6697):
    """Append {t, user, text} JSON lines to out_path until stop_event is set.

    Refuses any channel that is not on the VetTV allowlist. Uses TLS (6697) and
    falls back to plain 6667 only if that TLS connection fails.
    """
    ok, why = twitch_login_allowed(channel)
    if not ok:
        sys.exit(f"refusing Twitch chat: {why}")
    channel = channel.lower().lstrip("#")
    if not _LOGIN.fullmatch(channel):
        sys.exit("refusing Twitch chat: invalid login")
    stop_event = stop_event or threading.Event()
    use_tls = True
    with open(out_path, "a", encoding="utf-8", buffering=1) as out:
        while not stop_event.is_set():
            sock = None
            try:
                raw = socket.create_connection((host, port if use_tls else 6667), timeout=15)
                sock = ssl.create_default_context().wrap_socket(raw, server_hostname=host) if use_tls else raw
                sock.settimeout(5)
                sock.sendall(f"NICK justinfan{random.randint(10000, 99999)}\r\n".encode())
                sock.sendall(f"JOIN #{channel}\r\n".encode())
                buf = b""
                while not stop_event.is_set():
                    try:
                        data = sock.recv(4096)
                    except socket.timeout:
                        continue
                    if not data:
                        break
                    buf += data
                    *lines, buf = buf.split(b"\r\n")
                    for ln in lines:
                        s = ln.decode("utf-8", "replace")
                        if s.startswith("PING"):
                            sock.sendall(("PONG" + s[4:] + "\r\n").encode())
                            continue
                        m = _parse_privmsg(s)
                        if m and m[1]:
                            out.write(json.dumps({"t": time.time(), "user": m[0], "text": m[1]}, ensure_ascii=False) + "\n")
            except (OSError, ssl.SSLError) as ex:
                if use_tls and not isinstance(ex, socket.timeout):
                    use_tls = False
            finally:
                if sock:
                    try:
                        sock.close()
                    except OSError:
                        pass
            stop_event.wait(3)
