#!/usr/bin/env bash
# Run the MAU-MISC-001 batch (missiles, satellites, environment and prop kits), retrying after each
# Codex usage-limit stop until every target exists.
# Usage: bash docs/prompts/runs/MAU-MISC-001/wait_and_run.sh [first-wait-seconds] [max-attempts] [parallel]
set -u
cd "$(dirname "$0")/../../../.."
FIRST="${1:-0}"; MAX="${2:-8}"; PAR="${3:-2}"
D=docs/prompts/runs/MAU-MISC-001
TOTAL=$(wc -l < $D/jobs.tsv)
echo "waiting ${FIRST}s (now $(date '+%H:%M'))"
[ "$FIRST" -gt 0 ] && sleep "$FIRST"

run_one() {
  id=$1; prompt=$2; out=$3; ref1=$4; terran=$5
  out=${out%$'\r'}; ref1=${ref1%$'\r'}; terran=${terran%$'\r'}
  if [ -f "Concepts/Mauna/$out" ]; then exit 0; fi
  log="/tmp/codex-misc-$id.log"
  codex exec --skip-git-repo-check -s workspace-write -C "$(pwd -W 2>/dev/null || pwd)" \
    -i "Concepts/Mauna/$ref1" \
    -i Concepts/Mauna/Shared/MAU-EMB-001/MAU-emblem_ref_v01.png \
    -i "$terran" \
    - < "docs/prompts/runs/MAU-MISC-001/$prompt" > "$log" 2>&1
  if [ -f "Concepts/Mauna/$out" ]; then
    echo "$id saved"
  elif grep -qE "usage_limit_reached|hit your usage limit" "$log"; then
    echo "$id LIMIT: $(grep -oE 'try again at [^.]*' "$log" | head -1)"
    exit 255
  else
    echo "$id FAILED"
  fi
}
export -f run_one

for a in $(seq 1 "$MAX"); do
  echo "=== attempt $a at $(date '+%H:%M')"
  xargs -P "$PAR" -L 1 bash -c 'run_one "$@"' _ < $D/jobs.tsv
  left=0
  while IFS=$'\t' read -r id p out rest; do
    out=${out%$'\r'}
    [ -f "Concepts/Mauna/$out" ] || left=$((left + 1))
  done < $D/jobs.tsv
  echo "--- $left of $TOTAL left"
  if [ "$left" -eq 0 ]; then echo "ALL DONE at $(date '+%H:%M')"; exit 0; fi
  if [ "$a" -lt "$MAX" ]; then echo "sleeping 90m"; sleep 5400; fi
done
echo "STOPPED with $left left"
