# tmuxgen/loader.py
from __future__ import annotations
import os
from typing import Any, Dict, List

# tomllib is stdlib in Python 3.11+. For 3.8–3.10, install tomli and swap import.
try:
    import tomllib  # type: ignore
except Exception:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from .models import (
    Config, Session, Window, SendAction, KeysAction, SleepAction, Action
)

def _expand_env(s: str) -> str:
    # Expand ${ENV} and ~
    return os.path.expanduser(os.path.expandvars(s))

def _normalize_dir(path: str | None, base: str) -> str:
    if not path or path == ".":
        return _expand_env(base)
    p = _expand_env(path)
    if os.path.isabs(p):
        return p
    return os.path.normpath(os.path.join(_expand_env(base), p))

def _parse_action(raw: Dict[str, Any]) -> Action:
    t = raw.get("type")
    if t == "send":
        return SendAction(text=str(raw.get("text", "")), enter=bool(raw.get("enter", True)))
    if t == "keys":
        seq = raw.get("seq") or []
        if not isinstance(seq, list):
            raise ValueError("keys action requires an array `seq`")
        return KeysAction(seq=[str(x) for x in seq], enter=bool(raw.get("enter", False)))
    if t == "sleep":
        return SleepAction(ms=int(raw.get("ms", 50)))
    raise ValueError(f"Unknown action type: {t}")

def load_config(path: str) -> Config:
    with open(path, "rb") as f:
        data = tomllib.load(f)

    s = data.get("session") or {}
    name = s.get("name")
    default_dir = s.get("default_dir")
    if not name or not default_dir:
        raise ValueError("[session.name] and [session.default_dir] are required")

    session = Session(
        name=name,
        default_dir=default_dir,
        attach=bool(s.get("attach", True)),
        focus_window=s.get("focus_window") or None,
    )

    env = data.get("env") or {}

    windows_raw: List[Dict[str, Any]] = data.get("windows") or []
    if not windows_raw:
        raise ValueError("At least one [[windows]] entry is required")

    windows: List[Window] = []
    for w in windows_raw:
        wname = w.get("name")
        if not wname:
            raise ValueError("Each window needs a `name`")
        acts = [ _parse_action(a) for a in (w.get("actions") or []) ]
        windows.append(Window(name=wname, dir=w.get("dir"), actions=acts))

    # Resolve dirs relative to session.default_dir
    base = session.default_dir
    for w in windows:
        w.dir = _normalize_dir(w.dir, base)

    # Final expansion for session base as well
    session.default_dir = _expand_env(session.default_dir)

    return Config(session=session, env=env, windows=windows)
