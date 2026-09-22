#!/usr/bin/env bash
# Resume the Mauna building concept batch. Skips any building whose v01 PNG already exists, so it
# is safe to re-run after a Codex usage-limit stop. Usage (from the FragileArt root):
#   bash docs/prompts/runs/MAU-BLD-001/run_batch.sh [parallel-jobs, default 2]
set -u
cd "$(dirname "$0")/../../../.."
JOBS="${1:-2}"
LOGDIR="${TMPDIR:-/tmp}"
xargs -P "$JOBS" -L 1 bash -c '
  id=$0; p=$1; r=$2; v=${3:-v01}; v=${v%$'"'"'\r'"'"'}; r=${r%$'"'"'\r'"'"'}
  out="Concepts/Mauna/Buildings/$id/${id}_concept_${v}.png"
  if [ -f "$out" ]; then echo "$id skipped (exists)"; exit 0; fi
  codex exec --skip-git-repo-check -s workspace-write -C "$(pwd -W 2>/dev/null || pwd)" \
    -i Concepts/Mauna/Buildings/MAU-BLD-CMD-001/MAU-BLD-CMD-001_concept_v01.png \
    -i Concepts/Mauna/Shared/MAU-EMB-001/MAU-emblem_ref_v01.png \
    -i "$r" - < "$p" > "'"$LOGDIR"'/codex-$id.log" 2>&1
  rc=$?
  if [ -f "$out" ]; then echo "$id saved"
  elif grep -qE "usage_limit_reached|hit your usage limit" "'"$LOGDIR"'/codex-$id.log"; then
    echo "$id LIMIT: $(grep -oE "try again at [^.]*" "'"$LOGDIR"'/codex-$id.log" | head -1); stopping batch"
    exit 255
  else echo "$id FAILED (exit $rc)"; fi
' < docs/prompts/runs/MAU-BLD-001/jobs.tsv
echo "done: $(ls Concepts/Mauna/Buildings/*/*_concept_v01.png | wc -l) building concepts on disk (incl. the Exchange)"
