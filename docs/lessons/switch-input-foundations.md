# Switch input foundations: observations, bounce, and reliable meaning

**Original educational lesson · CC BY 4.0 · AI-assisted draft; engineering and user review pending**

An accessible-input project should begin with the person and the action they want to perform. A switch is one possible input, not a solution for every body, ability, or preference. Before controlling anything real, we can study one small software problem: how do several electrical observations become one intended press?

This lesson includes the model, calculations, examples, exercises, and an [offline simulator](../../tools/switch-input-lab/README.md). You need no hardware, account, API key, internet connection, or patient data. The sample observations are invented. They do not measure a person or device, and the simulator is not a validated access device or medical product.

## Two states are not always one clean transition

Imagine a mechanical contact moving from open to closed. It can briefly make and break contact several times. Logic may detect those changes as several transitions even when someone intended one press. Texas Instruments' [SCEA094 application brief](https://www.ti.com/document-viewer/lit/html/SCEA094) describes this contact-bounce problem. Its actual duration depends on the physical system; there is no universal bounce time to assume.

We will use the words `pressed: true` and `pressed: false`. They describe logical states, not a required wiring arrangement. A real circuit might use a low voltage to represent a press; that mapping must be established separately. This lesson provides no wiring or power instructions.

A sample records an observation at a timestamp. One millisecond, written ms, is one thousandth of a second. A reading at 35 ms says what the modeled input was at 35 ms. It does not reveal every event between 25 ms and 35 ms. We distinguish the raw observed state, the current accepted state, and a candidate change still waiting for confirmation.

## An explicit rule that you can inspect

Start with an explicitly supplied accepted state, initially unpressed in our fixture. Choose a demonstration stability interval of 20 ms. This number is invented for teaching, not selected from a device measurement or recommended for a particular person.

1. When an observation equals the accepted state, cancel any candidate.
2. When it differs and no candidate exists, start a candidate at this observation's timestamp.
3. A later observation of that opposite state confirms a change when elapsed time is **at least** the interval.
4. Emit one press or release event at that confirming sample, then update the accepted state.

Elapsed time is later timestamp minus candidate-start timestamp. The rule uses time, not the number of readings. Arduino's [official Debounce example](https://github.com/arduino/arduino-examples/blob/main/examples/02.Digital/Debounce/Debounce.ino) is another example of elapsed-time software filtering. Our simulator has its own documented boundary and behavior; it does not reproduce that example exactly.

A confirmed change here means the observed sequence met this rule. It does not prove that the physical input stayed stable between observations. Holding a state produces no repeated events. A candidate unfinished at the last sample produces no event afterward: the program does not invent a future confirming reading.

## Three worked examples

### 1. Reach the boundary

The accepted state is false. Read true at 25 ms, true at 35 ms, and true at 45 ms. The first reading starts a candidate. At 35 ms, elapsed time is 35 − 25 = 10 ms, too short. At 45 ms, 45 − 25 = 20 ms. Equality meets the rule, so a press is emitted at 45 ms. A further true reading merely preserves the accepted state.

### 2. A return cancels the candidate

Start false. Read true at 5 ms, false at 8 ms, true at 12 ms, and false at 20 ms. The 5 ms candidate is canceled at 8 ms. The 12 ms candidate is canceled at 20 ms. We cannot add these separate intervals together. A new true sequence beginning at 25 ms and confirmed at 45 ms yields the fixture's press at 45 ms.

For release, read false at 60 ms, true at 66 ms, false at 70 ms, and false at 90 ms. The accepted state was true. The 60 ms release candidate is canceled at 66 ms. The new candidate begins at 70 ms; 90 − 70 = 20 ms confirms release at 90 ms.

### 3. Sparse samples leave uncertainty

Start false. Observe true at 10 ms, then true at 1000 ms. The algorithm emits a press at 1000 ms because 1000 − 10 = 990 ms exceeds 20 ms. Yet no observations describe the intervening 990 ms. A brief release could be hidden. Increasing the threshold alone does not resolve this missing information. A real design needs explicit sampling and fault requirements in addition to a debounce rule.

## Five exercises

Try each question before reading its answer. You may reason entirely in text; diagrams and animation are unnecessary.

1. Start false with a 20 ms interval. Observe true at 10, 29, and 30 ms. When is the press confirmed?
2. Start false. Observe true at 5, false at 24, true at 30, true at 49, and true at 50 ms. When is the press confirmed, and why not earlier?
3. Start true. Observe true at 0, false at 2, false at 22, and false at 100 ms. What events occur?
4. Six true samples occur at 0, 1, 2, 3, 4, and 5 ms, starting from accepted false. Does a 20 ms interval confirm a press? What if no more samples arrive?
5. Change the complete fixture's interval from 20 to 10 ms. Does this create a release event at 80 ms? Find the actual press and release times.

## Answers and reasoning

1. At 30 ms. The candidate starts at 10 ms; 29 − 10 = 19 ms is short, while 30 − 10 = 20 ms meets the boundary.
2. At 50 ms. The false reading at 24 ms cancels the first candidate. The next begins at 30 ms. Its 49 ms observation is only 19 ms later; 50 ms provides 20 ms.
3. One release at 22 ms, because 22 − 2 = 20 ms. The later false observation does not emit another release. The supplied initial true state is an assumption of this exercise.
4. No. Five milliseconds elapsed, even though several observations occurred. With no later confirming sample, no future event is inferred.
5. Press at 35 ms, release at 90 ms. The press candidate starts at 25 ms, giving 35 − 25 = 10 ms. The final release candidate starts at 70 ms, but the next sample is at 90 ms. There is no 80 ms observation, so the program does not emit an event at 80 ms.

## From a simulation to useful engineering

Filtering creates a trade-off: longer confirmation can reject some rapid changes but delay an accepted action. A short deliberate action may also be filtered out. A useful design must consider the intended user's choices, observed hardware behavior, sampling gaps, fatigue, error recovery, and the consequences of unintended actions. This toy model evaluates none of those in people or devices.

Run the included synthetic fixture and tests, then trace the state machine yourself. A bounded next contribution is to add another invented trace and explain a failure of the model's assumptions. Do not present a passing simulation as evidence of usability, safety, or restored mobility. User participation, appropriate engineering review, and authorized real-device evaluation are separate work.

Both technical sources were retrieved successfully and inspected on 2026-11-07. Their source material retains its own rights; this original lesson reproduces no diagrams, source prose, or code. The repository includes [source inspection notes](../../tools/switch-input-lab/sources.json), the complete implementation, and all test inputs.
