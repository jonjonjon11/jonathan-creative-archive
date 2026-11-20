# Peace Execution Kit (Tonight-Ready)

This kit is designed for immediate action without depending on external reports or new datasets.

## Quick start (15 minutes)

```bash
cd peace_execution_kit
bash scripts/start_tonight.sh
```

Then follow:
- `plans/in_repo_tonight.md`
- `plans/outside_repo_tonight.md`
- `docs/ios_ai_repo_workflow.md`
- `sim-lab/README.md`

## What this kit gives you now

- A concrete tonight plan for work **inside** the project workspace.
- A concrete tonight plan for work **outside** the workspace (calls/emails/coordination).
- Templates for outreach, meeting execution, decisions, risks, and weekly metrics.
- A 100-day implementation board scaffold.
- A browser-based simulation lab scaffold for:
  - atom exploration (zoom, cross-section clip, transparency, timescale)
  - basic jet-engine concept visualization (stages, flow speed, cutaway controls)

## Suggested order tonight

1. Run `scripts/start_tonight.sh`
2. Fill `ops/stakeholder_list.csv` with real names
3. Send 5 outreach messages from `templates/outreach_message.txt`
4. Host a 30-minute kickoff using `templates/kickoff_agenda.md`
5. Log decisions in `ops/decision_log.csv`
6. Publish first internal milestone list in `ops/implementation_board.md`

## Run the simulation lab

```bash
cd peace_execution_kit
bash scripts/run_sim_lab.sh
```

Then open:
- `http://localhost:8080/sim-lab/atoms/`
- `http://localhost:8080/sim-lab/engine/`

## Run full integrated site

```bash
cd peace_execution_kit
bash scripts/run_site.sh
```

Then open:
- `http://localhost:8080/`

