# tmuxgen/cli.py
from __future__ import annotations
import argparse
import os
import sys
from .loader import load_config
from .renderers.bash import render_bash
from .utils import die

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate a Bash tmux setup script from TOML.")
    p.add_argument("config", help="Path to tmux-session.toml")
    p.add_argument("-o", "--out", help="Write script to file (default: stdout)")
    p.add_argument("--executable", action=argparse.BooleanOptionalAction, default=True)
    args = p.parse_args(argv)

    try:
        cfg = load_config(args.config)
    except Exception as e:
        die(str(e))

    script = render_bash(cfg)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(script)
        if args.executable:
            os.chmod(args.out, 0o755)
        print(f"Wrote {args.out}")
    else:
        sys.stdout.write(script)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
