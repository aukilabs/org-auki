#!/usr/bin/env bash
# relay-merge.sh — fan out a GitHub merge event to all quest tmux sessions.
#
# Designed to be invoked by a GitHub webhook handler (any webhook framework,
# any platform — Hermes, a tiny FastAPI/Flask app, a serverless function, etc.).
# Reads a GitHub PR webhook payload on stdin and broadcasts a formatted
# [orchestrator] message to every quest tmux session.
#
# Usage:
#   cat payload.json | QUEST_REPOS="quest-{slug}-repo-a quest-{slug}-repo-b ..." \
#                      GH_OWNER=[REDACTED - your GitHub org] \
#                      ./relay-merge.sh
#
# Wire-up: configure the webhook handler to invoke this script with the JSON
# payload piped to stdin. Whoever runs the orchestrator owns this glue —
# it's not specific to Hermes.

set -euo pipefail

payload=$(cat)

# Only fire on actual merges, not opens/closes/edits.
action=$(echo "$payload" | jq -r '.action // ""')
merged=$(echo "$payload" | jq -r '.pull_request.merged // false')
if [[ "$action" != "closed" || "$merged" != "true" ]]; then
  echo "skipping: action=$action merged=$merged" >&2
  exit 0
fi

repo=$(echo "$payload"     | jq -r '.repository.name')
pr_num=$(echo "$payload"   | jq -r '.pull_request.number')
title=$(echo "$payload"    | jq -r '.pull_request.title')
author=$(echo "$payload"   | jq -r '.pull_request.user.login')
body=$(echo "$payload"     | jq -r '.pull_request.body // ""' | head -c 500)
adds=$(echo "$payload"     | jq -r '.pull_request.additions')
dels=$(echo "$payload"     | jq -r '.pull_request.deletions')

GH_OWNER="${GH_OWNER:-[REDACTED - your GitHub org]}"

# Top-5 changed files via the GitHub API (payload doesn't include them).
files=$(gh api "repos/${GH_OWNER}/$repo/pulls/$pr_num/files" \
        --jq '[.[].filename] | .[0:5] | join(", ")' 2>/dev/null) || files="(file list unavailable)"
# Guard against gh succeeding-but-returning-error-json (e.g. test payloads with bogus PR numbers).
if [[ "$files" == *'"message":"Not Found"'* ]] || [[ -z "$files" ]]; then
  files="(file list unavailable)"
fi

message=$(cat <<EOF
[orchestrator] Merge to main in $repo: PR #$pr_num "$title"
Author: @$author
Files changed: $files (+$adds/-$dels)
PR body:
$body

If this unblocks work in your repo, pull main and proceed.
If not, append a Status-log entry to the Notion quest page confirming you
reviewed and skipped, then ignore.
EOF
)

# Fan out to every quest session, including the merging one.
for session in $QUEST_REPOS; do
  if tmux has-session -t "$session" 2>/dev/null; then
    # send-keys with literal text uses -l (literal mode) so backticks etc. don't expand.
    tmux send-keys -t "$session" -l "$message"
    tmux send-keys -t "$session" Enter
    echo "relayed to $session" >&2
  else
    echo "WARN: tmux session $session not found, skipping" >&2
  fi
done
