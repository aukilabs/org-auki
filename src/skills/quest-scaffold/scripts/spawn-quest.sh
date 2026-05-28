#!/usr/bin/env bash
# spawn-quest.sh — spawn one Claude Code agent per repo in tmux for a quest.
#
# Usage:
#   spawn-quest.sh <quest-slug> <repo1> [repo2] [repo3] ...
#
# Example:
#   spawn-quest.sh greenland discovery auki-sdk park boosterapp
#
# Each repo gets its own tmux session named `quest-{slug}-{repo}`, with
# Claude Code launched in the repo's working tree. Attach with:
#   tmux attach -t quest-{slug}-{repo}
# Detach with Ctrl-b d (the session keeps running).
#
# Environment overrides:
#   CLAUDE_BIN     — full path to the claude binary (default: auto-detect)
#   REPOS_ROOT     — where repos live (default: $HOME/agents)
#   REAL_HOME      — home dir where ~/.claude/.credentials.json lives
#                    (default: the invoking user's passwd home, NOT $HOME,
#                    because Hermes-spawned shells often override $HOME to
#                    a profile dir that doesn't have the OAuth token)

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <quest-slug> <repo1> [repo2] [repo3] ..." >&2
  echo "Example: $0 greenland discovery auki-sdk park boosterapp" >&2
  exit 1
fi

SLUG="$1"; shift

# --- locate the claude binary ---
# Prefer an explicit override; otherwise probe PATH; otherwise probe the
# bundled-in-Cursor location (Tracy's setup); otherwise fail loudly.
if [ -n "${CLAUDE_BIN:-}" ]; then
  :  # honour the override
elif command -v claude >/dev/null 2>&1; then
  CLAUDE_BIN="$(command -v claude)"
elif [ -x "/home/ec2-user/.cursor-server/extensions/anthropic.claude-code-2.1.138-linux-x64/resources/native-binary/claude" ]; then
  CLAUDE_BIN="/home/ec2-user/.cursor-server/extensions/anthropic.claude-code-2.1.138-linux-x64/resources/native-binary/claude"
else
  cat >&2 <<EOF
error: claude binary not found.
  - install Claude Code CLI (https://docs.claude.com/claude-code), or
  - set CLAUDE_BIN=/full/path/to/claude when invoking this script.
EOF
  exit 1
fi

# --- locate the OAuth-credentialled home ---
REAL_HOME="${REAL_HOME:-$(getent passwd "$(whoami)" | cut -d: -f6)}"
if [ ! -f "$REAL_HOME/.claude/.credentials.json" ]; then
  echo "warn: $REAL_HOME/.claude/.credentials.json not found — agents will prompt for login on first launch." >&2
  echo "      Log in once via 'claude' in a normal shell, then re-run this script." >&2
fi

REPOS_ROOT="${REPOS_ROOT:-$REAL_HOME/agents}"

spawned=()
skipped=()

for repo in "$@"; do
  session="quest-${SLUG}-${repo}"
  repo_dir="${REPOS_ROOT}/${repo}"

  if [ ! -d "$repo_dir" ]; then
    echo "warn: $repo_dir does not exist, skipping $repo" >&2
    skipped+=("$repo (no repo dir)")
    continue
  fi

  if tmux has-session -t "$session" 2>/dev/null; then
    echo "info: session $session already exists, leaving it alone"
    skipped+=("$repo (session exists)")
    continue
  fi

  tmux new-session -d -s "$session" -c "$repo_dir" \
    "export HOME='$REAL_HOME'; '$CLAUDE_BIN'"

  spawned+=("$session")
done

echo ""
echo "Spawned: ${#spawned[@]} session(s)"
for s in "${spawned[@]}"; do
  echo "  tmux attach -t $s"
done
if [ ${#skipped[@]} -gt 0 ]; then
  echo "Skipped: ${skipped[*]}"
fi
echo ""
echo "All quest-${SLUG}-* sessions:"
tmux ls 2>/dev/null | grep "^quest-${SLUG}-" || echo "  (none)"
