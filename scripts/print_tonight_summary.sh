#!/usr/bin/env bash
set -euo pipefail

echo "== Tonight Summary =="
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

count_rows() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "0"
    return
  fi
  local lines
  lines=$(wc -l < "$file")
  if [[ "$lines" -le 1 ]]; then
    echo "0"
  else
    echo $((lines - 1))
  fi
}

stakeholders=$(count_rows "ops/stakeholder_list.csv")
decisions=$(count_rows "ops/decision_log.csv")
risks=$(count_rows "ops/risk_register.csv")
metrics=$(count_rows "ops/weekly_metrics.csv")

echo "Stakeholders logged: $stakeholders"
echo "Decisions logged:    $decisions"
echo "Risks logged:        $risks"
echo "Metrics defined:     $metrics"
echo

echo "Definition-of-done checks:"
[[ "$stakeholders" -ge 5 ]] && echo "[OK] >=5 stakeholders" || echo "[TODO] Add stakeholders to ops/stakeholder_list.csv"
[[ "$decisions" -ge 5 ]] && echo "[OK] >=5 decisions" || echo "[TODO] Add decisions to ops/decision_log.csv"
[[ "$risks" -ge 5 ]] && echo "[OK] >=5 risks" || echo "[TODO] Add risks to ops/risk_register.csv"
[[ "$metrics" -ge 10 ]] && echo "[OK] >=10 metrics" || echo "[TODO] Add metrics to ops/weekly_metrics.csv"

