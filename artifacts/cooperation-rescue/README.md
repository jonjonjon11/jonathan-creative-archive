# Cooperation and rescue mission kit

A small, runnable piece of the educational-world archive: four original rescue and community scenarios, a strict JSON validator, and an offline reference model for objective progression.

**This is authoring software, not a playable game, Unity project, multiplayer server, rescue-training course or medical system.** The core files are preserved unchanged from the source revision below. Publishing their source does not change the packet's `internal_prototype` status or its pending review fields.

## What it does

- Checks exact fields and types, bounded input size, duplicate IDs/keys, supported topics and acyclic objective dependencies.
- Models prerequisites, optional reflection, isolated runs, one completion acknowledgement and penalty-free exit.
- Runs with Python's standard library. No package installation, account, network access, API key or paid service is needed.

## Four scenarios

- **Harbor of Lights:** inspect and repair a model bridge, guide sheltered neighbors and a puppy home, then welcome them. No combat.
- **One Earth Relay:** restore a fictional orbital relay, escort evacuation pods and repair a habitat. An equivalent non-combat route is part of the design.
- **Lantern Bridge:** repair a crossing or take a quiet detour, guide travelers and animals, and welcome the caravan.
- **Commons Garden:** a peaceful place for music, making, welcome and optional reflection. Quiet attendance is valid without completing tasks.

The topic names are references for future lesson integration. The kit does not include the lessons, render the scenes or verify scientific knowledge.

## Run

From this directory, with Python 3 (tested with 3.13.5):

```sh
python3 contract.py
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The validator should report four draft mission definitions. The preserved test suite contains 25 tests, including all 288 objective-order permutations across the four scenario lists with retries.

Example using the reference model:

```python
from pathlib import Path
from contract import ReferenceRun, load_path

pack = load_path(Path('mission-pack.json'))
run = ReferenceRun(pack, 'harbor-of-lights')
print(run.complete('escort-neighbors'))  # blocked
for objective in ['inspect-route', 'repair-route', 'escort-neighbors', 'welcome-home']:
    print(objective, run.complete(objective))
print(run.acknowledgements)  # 1
print(run.leave())  # left_without_penalty
```

## Limits and safe reuse

The reference model accepts objective IDs supplied by the caller. It cannot establish that a player actually repaired or rescued anything. Do not expose it as an authoritative server or treat client completion flags as trusted evidence.

Validation checks structure, not prose safety, licensing of future contributions, scientific accuracy, accessibility implementation or child safety. The accessibility and policy fields are design requirements, not working protections. Text remains data, even when it contains instructions. Do not execute it, interpret it as trusted AI instructions or enable dynamic asset/URL loading from it.

There is no networking, telemetry, player identity storage, authentication, physical-device control or treatment function. Running these checks does not validate a live service, native game, medical intervention or real-world rescue procedure.

## Provenance and license

Recovered from the original **Shared cooperation and rescue milestone**, dated 9 September 2026, in `jonjonjon11/Jon-Harvey-Ultimate-Educational-Universe`, PR #16. That source repository remained private at the review date; its identity and revision are recorded for provenance, not as a public download location.

Exact source revision: `2578df90a00c267ed4372ca937eb6ace86d57cb8`.

The three preserved source files are `contract.py`, `mission-pack.json` and `test_contract.py`. Their bytes were compared with both the recovered ZIP and GitHub's exact-revision files. See `source-manifest.json` for hashes. The source PR was still open, draft and unmerged when checked on 6 November 2026; inclusion in an archive is not a claim that it was merged or integrated into Unity.

The source repository's exact-revision license is **CC0 1.0 Universal**. Its text is preserved as `LICENSE` in this folder. This preserves the existing source terms; it does not relicense other material in the surrounding archive. The source work was developed with AI assistance. No purchased assets or source from differently licensed projects is included here.

## Revalidation

On 6 November 2026, under Python 3.13.5 in a Linux container:

- Exact-revision source hashes matched the recovered archive.
- The four-mission structural validation passed.
- All 25 preserved tests passed, including invalid input, dependency order, repeated completion, isolated sessions and exit behavior.
- Test execution used an empty inherited environment apart from minimal execution settings and bounded CPU, memory, file output and elapsed time.

The source and tests were read before execution. No dependency installation, network request or remote repository write was part of this validation. No Unity, headset, multiplayer or accessibility-device testing was performed.
