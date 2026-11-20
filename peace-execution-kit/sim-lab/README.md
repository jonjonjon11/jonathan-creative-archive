# Sim Lab

Browser-based interactive demos that run without a build step.

## Run locally

```bash
cd /root/peace_execution_kit
bash scripts/run_sim_lab.sh
```

Open:
- `http://localhost:8080/sim-lab/atoms/`
- `http://localhost:8080/sim-lab/atoms/hydrogen-replay.html`
- `http://localhost:8080/sim-lab/engine/`

## Demos

- `atoms/`: educational atom viewer with:
  - element selection
  - zoom
  - transparency (see-through)
  - cross-section clipping
  - timescale/speed control
  - hydrogen replay lesson (Same Starting Frame: 1s vs 2p(z), slice controls, save/restore)
- `engine/`: conceptual jet-engine stage visualization with:
  - stage toggles
  - flow speed
  - cutaway mode
  - pause/play

These are educational visualizations, not validated engineering or quantum solvers.

