"""PreToolUse hook: block Bash commands that break the team rules in CLAUDE.md.

Claude Code sends the tool call as JSON on stdin. Exit code 2 blocks the call and
the message on stderr is shown to Claude, so every block says why.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

PROTECTED = ("main", "master")


def current_branch() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def reason_to_block(command: str) -> str | None:
    if re.search(r"\bgit\b.*\bcommit\b", command) and \
            re.search(r"co-authored-by:|claude-session:", command, re.IGNORECASE):
        return ("Commit messages in this repo must not contain Co-Authored-By or "
                "Claude-Session trailer lines. Remove them and commit again.")

    for push in re.findall(r"\bgit\s+push\b[^;&|]*", command):
        args = push.split()[2:]
        if any(a in ("--force", "-f") or (a.startswith("-") and not a.startswith("--")
                                          and "f" in a) for a in args):
            return ("Force-push is not allowed. Use --force-with-lease on your own "
                    "branch only if you really must rewrite it.")
        targets = [a.split(":")[-1] for a in args if not a.startswith("-")][1:]
        if any(t in PROTECTED for t in targets) or \
                (not targets and current_branch() in PROTECTED):
            return ("Do not push to main directly. Push a feature branch and open a PR.")
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    command = (payload.get("tool_input") or {}).get("command", "")
    reason = reason_to_block(command)
    if reason:
        print(f"Blocked by .claude/hooks/block_forbidden.py: {reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
