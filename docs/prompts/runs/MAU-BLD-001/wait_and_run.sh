#!/usr/bin/env bash
# Wait for the Codex usage-limit reset, then run the Mauna building batch, retrying after each
# limit stop until every building has a concept (or the attempt budget runs out).
# Usage: bash docs/prompts/runs/MAU-BLD-001/wait_and_run.sh [first-wait-seconds] [max-attempts]
set -u
cd "$(dirname "$0")/../../../.."
FIRST_WAIT="${1:-0}"
MAX_ATTEMPTS="${2:-8}"
TOTAL=$(wc -l < docs/prompts/runs/MAU-BLD-001/jobs.tsv)
echo "waiting ${FIRST_WAIT}s for the Codex reset ($(date '+%H:%M') now)"
[ "$FIRST_WAIT" -gt 0 ] && sleep "$FIRST_WAIT"
for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "=== attempt $attempt at $(date '+%H:%M')"
  bash docs/prompts/runs/MAU-BLD-001/run_batch.sh 2 | grep -Ev "skipped \(exists\)"
  have=$(ls Concepts/Mauna/Buildings/*/ -d 2>/dev/null | wc -l)
  echo "--- $have of $((TOTAL + 1)) buildings have a concept folder"
  if [ "$have" -ge "$((TOTAL + 1))" ]; then echo "ALL DONE at $(date '+%H:%M')"; exit 0; fi
  [ "$attempt" -lt "$MAX_ATTEMPTS" ] && { echo "sleeping 90m before retry"; sleep 5400; }
done
echo "STOPPED after $MAX_ATTEMPTS attempts; $have of $((TOTAL + 1)) done"
