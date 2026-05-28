#!/usr/bin/env bash
# week-scope.sh — resolve the current ISO week and the default since-date
# (most recent past Friday strictly before today) for presentation harvest.
#
# Usage:
#   eval "$(scripts/week-scope.sh)"                  # load vars into shell
#   scripts/week-scope.sh                             # print to stdout
#   scripts/week-scope.sh --since 2026-05-01          # override since date
#   scripts/week-scope.sh --week 19                   # override ISO week
#
# Outputs four shell variable assignments (safe to eval):
#   HARVEST_WEEK        ISO week number (integer, no leading zero), e.g. 20
#   HARVEST_WEEK_LABEL  directory-safe label, e.g. week-20
#   HARVEST_SINCE       cutoff YYYY-MM-DD (defaults to most recent past Friday)
#   HARVEST_UNTIL       today as YYYY-MM-DD
#
# "Most recent past Friday" means the last Friday strictly before today.
# If today IS Friday, we go back 7 days so the full current week is captured.
# Use --since to backfill a missed week or pin an exact window.

set -euo pipefail

OVERRIDE_SINCE=""
OVERRIDE_WEEK=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since) OVERRIDE_SINCE="$2"; shift 2 ;;
    --week)  OVERRIDE_WEEK="$2";  shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

TODAY=$(date +%Y-%m-%d)
TODAY_DOW=$(date +%u)   # 1=Monday … 7=Sunday (ISO 8601)

# --- ISO week ---
if [[ -n "$OVERRIDE_WEEK" ]]; then
  HARVEST_WEEK="$OVERRIDE_WEEK"
else
  HARVEST_WEEK=$(date +%-V)   # GNU date: strip leading zero
fi
HARVEST_WEEK_LABEL="week-${HARVEST_WEEK}"

# --- since date ---
if [[ -n "$OVERRIDE_SINCE" ]]; then
  HARVEST_SINCE="$OVERRIDE_SINCE"
else
  # Friday = DOW 5.  Days back to the most recent Friday strictly before today:
  #   days_back = (DOW - 5 + 7) % 7
  #   but that yields 0 when today IS Friday, so force 7 in that case.
  DAYS_BACK=$(( (TODAY_DOW - 5 + 7) % 7 ))
  [[ "$DAYS_BACK" -eq 0 ]] && DAYS_BACK=7
  HARVEST_SINCE=$(date -d "${TODAY} - ${DAYS_BACK} days" +%Y-%m-%d)
fi

HARVEST_UNTIL="$TODAY"

printf 'HARVEST_WEEK=%s\n'        "$HARVEST_WEEK"
printf 'HARVEST_WEEK_LABEL=%s\n'  "$HARVEST_WEEK_LABEL"
printf 'HARVEST_SINCE=%s\n'       "$HARVEST_SINCE"
printf 'HARVEST_UNTIL=%s\n'       "$HARVEST_UNTIL"
