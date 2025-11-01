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
    p.add_argument("-o", "--output", help="Write script to file (default: same folder as config with .sh extension)")
    p.add_argument("--executable", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--stdout", action="store_true", help="Write to stdout instead of file")
    args = p.parse_args(argv)

    try:
        cfg = load_config(args.config)
    except Exception as e:
        die(str(e))

    script = render_bash(cfg)

    # Determine output path
    if args.stdout:
        sys.stdout.write(script)
    else:
        out_path = args.output
        if not out_path:
            # Generate default output path in same folder as config
            config_path = os.path.abspath(args.config)
            config_dir = os.path.dirname(config_path)
            config_name = os.path.splitext(os.path.basename(config_path))[0]
            out_path = os.path.join(config_dir, f"{config_name}.sh")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(script)
        if args.executable:
            os.chmod(out_path, 0o755)
        print(f"Wrote {out_path}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
