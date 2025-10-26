from typing import Never
import sys

def die(msg: str) -> Never:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)
