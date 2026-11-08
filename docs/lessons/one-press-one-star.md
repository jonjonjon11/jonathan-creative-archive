# One press, one star

**A small offline Python programming exercise · CC BY 4.0 · AI-assisted draft; learner and educator review pending**

Make a pretend character collect a star for each confirmed press in an invented input trace. You will learn how a variable remembers a score, a list stores events, a loop visits them, and a condition decides whether to award a point. This is a text-only game rule, not a playable platformer or a live keyboard/hardware interface. All inputs are synthetic.

Read [Switch input foundations](switch-input-foundations.md) first for the four debounce rules. You can follow the tables on paper without installing anything. To run the finished code, obtain this repository, have Python 3.8 or newer installed, and open a terminal at the repository root. No additional packages, account, internet connection, device, or patient data are needed. The commands below use `python3`; on Windows with the Python launcher, replace that with `py -3`.

## 1. Predict the score before running

A raw observation is not a press event. The input filter begins with accepted state `false` and waits for an opposite-state candidate to last at least 20 ms **among the observed samples**. A return to the accepted state cancels the candidate. A confirmed release is needed before another press can be confirmed.

The complete [two-press fixture](../../tools/switch-input-lab/fixtures/synthetic-two-presses.json) contains these observations. “Candidate since” is its value **after** processing each row. A dash means no pending candidate.

| Time (ms) | Observed pressed | Accepted pressed after row | Candidate since (ms) | Event |
| --- | --- | --- | --- | --- |
| 0 | false | false | — | none |
| 5 | true | false | 5 | none |
| 8 | false | false | — | none |
| 12 | true | false | 12 | none |
| 20 | false | false | — | none |
| 25 | true | false | 25 | none |
| 35 | true | false | 25 | none |
| 45 | true | true | — | press |
| 50 | true | true | — | none |
| 60 | false | true | 60 | none |
| 66 | true | true | — | none |
| 70 | false | true | 70 | none |
| 90 | false | false | — | release |
| 100 | false | false | — | none |
| 120 | true | false | 120 | none |
| 125 | false | false | — | none |
| 130 | true | false | 130 | none |
| 149 | true | false | 130 | none |
| 150 | true | true | — | press |
| 170 | true | true | — | none |
| 190 | false | true | 190 | none |
| 210 | false | false | — | release |

For example, the candidate at 120 ms is canceled at 125 ms. The next begins at 130 ms. At 149 ms only 19 ms have elapsed; at 150 ms, exactly 20 ms have elapsed. The later 170 ms held observation adds no event.

Predict the final star count. Would counting every `true` observation give the same answer? Write down your reasoning before continuing.

## 2. Run the finished example

```sh
python3 tools/switch-input-lab/star_counter.py tools/switch-input-lab/fixtures/synthetic-two-presses.json
```

Expected output:

```text
One press, one star: synthetic text-only game
45 ms: total stars = 1
150 ms: total stars = 2
Final stars: 2
Only confirmed sampled press events award points; releases and held states do not.
Educational simulation; no hardware or clinical validation.
```

Two accepted presses produce two stars. There are twelve raw `true` observations, so awarding a star for every such observation would wrongly give twelve stars for this exercise's rule. The filter instead emits four events: press at 45 ms, release at 90 ms, press at 150 ms, release at 210 ms. Only the two press events earn stars.

## 3. Read the game rule line by line

Open [star_counter.py](../../tools/switch-input-lab/star_counter.py) in a text editor. Its function `collect_stars` validates the reward, calls the existing input simulator, and uses this loop. The simulator's implementation is in [switch_input.py](../../tools/switch-input-lab/switch_input.py); there is only one copy of that algorithm.

```python
    stars = 0
    collections = []
    for event in result["events"]:
        if event["event"] == "press":
            stars = stars + stars_per_press
            collections.append({"timestamp_ms": event["timestamp_ms"], "stars": stars})
```

- `stars = 0` creates the starting score. The assignment stores a value; it is not an equation asserting that the score stays zero.
- `collections = []` creates an empty list. Each later entry records when a star was awarded and the resulting total.
- `for event in result["events"]:` visits each confirmed event in order. The square-bracket expression looks up the `events` field of a dictionary, a collection of named values.
- `if event["event"] == "press":` compares the event's name with `press`. The double equals sign checks equality. It does not assign a new name.
- `stars = stars + stars_per_press` reads the old score, adds the reward and stores the new score. The default reward is one.
- `collections.append(...)` adds a dictionary containing the event timestamp and current score to the list.

Indented lines belong to the surrounding loop or condition. Removing the `if` and moving its indented body directly into the loop would award points for releases too. That would implement a different rule.

Trace the four events by hand: starting score 0 → press gives 1 → release keeps 1 → press gives 2 → release keeps 2.

## 4. Change one value and predict again

Predict the score if each press earns two stars. Run:

```sh
python3 tools/switch-input-lab/star_counter.py tools/switch-input-lab/fixtures/synthetic-two-presses.json --stars-per-press 2
```

The totals become 2 at 45 ms and 4 at 150 ms; the final score is 4. The event times do not change. This option changes the function's reward argument rather than the input filter. Rewards must be whole numbers from 1 to 100.

For a code-edit exercise, make a personal copy of `star_counter.py` **in the same directory**, naming it `my_star_counter.py`, and change the parser's `default=1` to `default=2`. Run that copy without the option. It now starts with the two-star reward. Keep the original intact so that you can compare it and reproduce the published tests. Remove your copy before running the archive-wide inventory check, which intentionally reports unregistered files. No code edit is needed just to use the CLI option.

## 5. Challenge the rule

Answer before reading the solutions. Times below are milliseconds; use the default 20 ms interval and one-star reward unless stated otherwise.

1. Start accepted `false`. Observe `true` at 0, 20, 30 and 1000. How many stars, and when?
2. Start accepted `true`. Observe `true` at 0 and 20. Should the initial state earn a star? What if false at 30 and 50 is followed by true at 60 and 80?
3. Start accepted `false`. Observe true at 0 and 20, false at 30, true at 35 and 55. Is there a second star?
4. Start accepted `false`. Observe true at 10 and 1000. Compare that with a trace that also observes false at 500. What can the first trace fail to reveal?
5. Predict the result of the original two-press fixture when `stars_per_press` is 3. Does the release at 210 ms change the total?

### Solutions

1. One star at 20 ms. Later held observations do not produce additional press events.
2. No startup star: an assumed initial state is not a confirmed change. A release is confirmed at 50 ms and a new press at 80 ms, earning one star at 80 ms.
3. No. The false observation at 30 ms starts a release candidate, but true at 35 ms cancels it. The accepted state never became false, so there is no new confirmed press. The only star is at 20 ms.
4. The sparse pair earns one star at 1000 ms because the observed sequence meets the interval rule. With false at 500 ms, the first candidate is canceled; true at 1000 ms only starts a new, unfinished candidate, so there are no stars. The first trace cannot rule out that intervening release. A passing result does not prove physical continuity, accuracy about a person's intention, or suitability for a real input device.
5. Three stars at 45 ms and six total at 150 ms. The final release does not change the six-star total.

## 6. Check and extend

```sh
python3 -B -m unittest discover -s tools/switch-input-lab/tests -p 'test_*.py' -v
python3 tools/switch-input-lab/star_counter.py tools/switch-input-lab/fixtures/synthetic-two-presses.json --json
```

The JSON output includes the collections, all confirmed input events and model limitations. The program prints results and does not save files or contact a service. Tests check specific code behavior and this lesson's example, not whether a beginner finds it understandable. For a next exercise, invent a third press/release cycle, predict the result, and make the example into a test. Do not feed the simulator personal or patient traces.

The programming pattern can support discussion of game input and state machines. This particular debounce threshold and model are teaching choices, not recommended settings for a keyboard, controller, assistive switch or any person. There has been no hardware, clinical, screen-reader, learner or educator validation. Sources for the input concept are recorded in the [foundation lesson](switch-input-foundations.md) and [source notes](../../tools/switch-input-lab/sources.json); the game rule and invented observations are original work.
