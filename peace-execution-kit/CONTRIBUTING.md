# Contributing to Peace Execution Kit

Thanks for helping improve this project.

## Contribution flow
1. Pick one scoped task from `OPEN_TASKS.md`.
2. State your acceptance check in your PR description.
3. Keep changes focused and file-local where possible.
4. Verify locally before opening PR.

## Local run
```bash
cd peace-execution-kit
bash scripts/run_site.sh
```
Then open `http://localhost:8080/`.

## Required acceptance checks
- Route still loads from `peace-execution-kit/index.html`.
- No broken links from the main journey:
  - Financing -> Source trace -> Courtyard -> Hydrogen replay.
- Mobile viewport remains usable (phone width).

## Labels to include in PR title
Use one prefix:
- `[data]` source, baselines, ledgers, citations
- `[ui]` layout, accessibility, interaction clarity
- `[sim]` atom/engine/lesson behavior
- `[docs]` documentation and contributor guidance

## Safety and evidence rules
- Do not present placeholder values as verified facts.
- Keep `published` vs `custom` assumptions clearly separated.
- Add source links for factual claims when available.
