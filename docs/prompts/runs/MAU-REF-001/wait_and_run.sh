#!/usr/bin/env bash
# Generate, crop, normalise and validate orthographic reference sheets for the Mauna low-detail
# buildings. Retries after each Codex usage-limit stop until every asset has a validated set.
# Usage: bash docs/prompts/runs/MAU-REF-001/wait_and_run.sh [first-wait-seconds] [max-attempts] [parallel]
set -u
cd "$(dirname "$0")/../../../.."
FIRST="${1:-0}"; MAX="${2:-10}"; PAR="${3:-2}"
D=docs/prompts/runs/MAU-REF-001
TOTAL=$(wc -l < $D/jobs.tsv)
echo "waiting ${FIRST}s (now $(date '+%H:%M'))"
[ "$FIRST" -gt 0 ] && sleep "$FIRST"

run_one() {
  id=$1; prompt=$2; src=$3
  src=${src%$'\r'}
  sheet="References/Mauna/Buildings/$id/LowDetail/${id}_low-detail_reference-sheet_v01.png"
  final="References/Mauna/Buildings/$id/LowDetail/${id}_low-detail_front_v04.png"
  [ -f "$final" ] && exit 0
  log="/tmp/codex-ref-$id.log"
  if [ ! -f "$sheet" ]; then
    codex exec --skip-git-repo-check -s workspace-write -C "$(pwd -W 2>/dev/null || pwd)" \
      -i "$src" - < "docs/prompts/runs/MAU-REF-001/$prompt" > "$log" 2>&1
  fi
  if [ ! -f "$sheet" ]; then
    if grep -qE "usage_limit_reached|hit your usage limit" "$log"; then
      echo "$id LIMIT: $(grep -oE 'try again at [^.]*' "$log" | head -1)"
      exit 255
    fi
    echo "$id SHEET-FAILED"; exit 0
  fi
  python docs/prompts/runs/MAU-REF-001/process_sheet.py "$id" 2>&1 | tail -1
}
export -f run_one

for a in $(seq 1 "$MAX"); do
  echo "=== attempt $a at $(date '+%H:%M')"
  xargs -P "$PAR" -L 1 bash -c 'run_one "$@"' _ < $D/jobs.tsv
  left=0
  while IFS=$'\t' read -r id rest; do
    [ -f "References/Mauna/Buildings/$id/LowDetail/${id}_low-detail_front_v04.png" ] || left=$((left + 1))
  done < $D/jobs.tsv
  echo "--- $left of $TOTAL without a validated set at $(date '+%H:%M')"
  if [ "$left" -eq 0 ]; then echo "ALL DONE at $(date '+%H:%M')"; exit 0; fi
  if [ "$a" -lt "$MAX" ]; then echo "sleeping 90m"; sleep 5400; fi
done
echo "STOPPED with $left left"
