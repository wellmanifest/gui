#!/usr/bin/env bash
# Ensure unsupported runtime execution never masquerades as a passing test.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for command in test testql; do
  if output="$(cd / && bash "$root/project.sh" "$command" 2>&1)"; then
    status=0
  else
    status=$?
  fi
  [[ "$status" -eq 2 ]] || { echo "GUI-TEST-STATUS: $command returned $status, expected unavailable (2)" >&2; exit 1; }
  [[ "$output" == *"GUI-TESTQL-UNAVAILABLE:"* ]] || { echo "GUI-TEST-STATUS: unavailable diagnostic missing" >&2; exit 1; }
  [[ "$output" != *"assertions passed"* && "$output" != *"suite loaded"* ]] || { echo "GUI-TEST-STATUS: unexecuted tests claimed success" >&2; exit 1; }
done
echo "ok: GUI test entrypoint reports unavailable runtime"
