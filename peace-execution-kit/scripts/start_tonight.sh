#!/usr/bin/env bash
set -euo pipefail

echo "== Peace Execution Kit: Tonight Bootstrap =="
echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo

required=(
  "plans/in_repo_tonight.md"
  "plans/outside_repo_tonight.md"
  "ops/implementation_board.md"
  "ops/decision_log.csv"
  "ops/risk_register.csv"
  "ops/stakeholder_list.csv"
  "ops/weekly_metrics.csv"
  "templates/outreach_message.txt"
  "templates/pilot_invitation_email.txt"
  "templates/kickoff_agenda.md"
  "templates/partner_mou_outline.md"
)

missing=0
for f in "${required[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "[MISSING] $f"
    missing=$((missing + 1))
  else
    echo "[OK] $f"
  fi
done

echo
if [[ $missing -gt 0 ]]; then
  echo "Bootstrap incomplete: $missing required files are missing."
  exit 1
fi

echo "Bootstrap complete."
echo
echo "Next:"
echo "1) Fill 5 rows in ops/stakeholder_list.csv"
echo "2) Assign owners in ops/implementation_board.md"
echo "3) Send 5 outreach messages from templates/outreach_message.txt"
echo "4) Schedule one kickoff call using templates/kickoff_agenda.md"

