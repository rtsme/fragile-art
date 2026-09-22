#!/usr/bin/env bash
# Wait out a Codex usage-limit reset, then run the MAU-FINAL-001 jobs (remaining ships + building
# fixes), retrying until every target exists. Usage: bash <this> [first-wait-seconds] [max-attempts]
set -u
cd "$(dirname "$0")/../../../.."
FIRST="${1:-0}"; MAX="${2:-6}"; D=docs/prompts/runs/MAU-FINAL-001
echo "waiting ${FIRST}s (now $(date '+%H:%M'))"; [ "$FIRST" -gt 0 ] && sleep "$FIRST"
for a in $(seq 1 "$MAX"); do
  echo "=== attempt $a at $(date '+%H:%M')"
  cat $D/jobs.tsv | xargs -P 2 -L 1 bash -c '
    id=$0; p=$1; out=$2; ref=$3; out=${out%$'"'"'\r'"'"'}; ref=${ref%$'"'"'\r'"'"'}
    [ -f "Concepts/Mauna/$out" ] && exit 0
    codex exec --skip-git-repo-check -s workspace-write -C "$(pwd -W 2>/dev/null || pwd)" \
      -i "Concepts/Mauna/$ref" -i Concepts/Mauna/Shared/MAU-EMB-001/MAU-emblem_ref_v01.png \
      - < "docs/prompts/runs/MAU-FINAL-001/$p" > "/tmp/codex-final-$id.log" 2>&1
    if [ -f "Concepts/Mauna/$out" ]; then echo "$id saved"
    elif grep -qE "usage_limit_reached|hit your usage limit" "/tmp/codex-final-$id.log"; then echo "$id LIMIT"; exit 255
    else echo "$id FAILED"; fi'
  left=0
  while IFS=$'\t' read -r id p out ref; do out=${out%$'\r'}; [ -f "Concepts/Mauna/$out" ] || left=$((left+1)); done < $D/jobs.tsv
  echo "--- $left job(s) left"
  [ "$left" -eq 0 ] && { echo "ALL DONE at $(date '+%H:%M')"; exit 0; }
  [ "$a" -lt "$MAX" ] && { echo "sleeping 90m"; sleep 5400; }
done
echo "STOPPED with $left left"
