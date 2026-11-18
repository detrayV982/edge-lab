#!/bin/sh
# Undoes week 7: goes back to main at the saved base commit and deletes the week-7 branch. Use --dry-run to only print.
BASE=$(cat "$(dirname "$0")/backup/base_commit.txt")
run() { if [ "$1" = "--dry-run" ]; then shift; echo "would run: $*"; else "$@"; fi; }
MODE="$1"
cd "$(dirname "$0")/.." || exit 1
run $MODE git checkout main
run $MODE git reset --hard "$BASE"
run $MODE git branch -D week-7
echo "Python packages: reinstall from autopilot/backup/pip_freeze_before.txt if needed"
