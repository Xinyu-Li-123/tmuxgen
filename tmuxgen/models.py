# tmuxgen/models.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal

ActionType = Literal["send", "keys", "sleep"]

@dataclass
class SendAction:
    type: Literal["send"] = "send"
    text: str = ""
    enter: bool = True  # press Enter after text

@dataclass
class KeysAction:
    type: Literal["keys"] = "keys"
    seq: List[str] = field(default_factory=list)  # e.g. ["Space","e","Space","q","s"]
    enter: bool = False

@dataclass
class SleepAction:
    type: Literal["sleep"] = "sleep"
    ms: int = 50  # small default

Action = SendAction | KeysAction | SleepAction

@dataclass
class Window:
    name: str
    dir: Optional[str] = None
    actions: List[Action] = field(default_factory=list)

@dataclass
class Session:
    name: str
    default_dir: str
    attach: bool = True
    focus_window: Optional[str] = None

@dataclass
class Config:
    session: Session
    env: Dict[str, str] = field(default_factory=dict)
    windows: List[Window] = field(default_factory=list)
