# String harmonics: a paper-first companion

Version 1.0.0 · 2026-11-09 · Original archive contribution · [CC BY 4.0](../../LICENSE)

How can a string have several repeating patterns when neither end can move? Work through three examples, then try five questions. Read the numbers and descriptions, or sketch them if you wish. No instrument, sound, animation, calculator, account or programming is required. A suggested 20–30 minutes is a planning estimate, not a time limit.

**Starting knowledge:** multiplication and division, fractions such as one half, and signed numbers. Metres (m) measure length, seconds (s) measure time, and hertz (Hz) means cycles per second. The optional equation uses sine and cosine, but the main path supplies their needed values.

**By the end:** identify fixed nodes, relate a mode number to wavelength and frequency, distinguish a string's spatial pattern from its motion over time, and explain one limit of the model.

This is an AI-assisted learning draft with numerical and content checks, not a validated curriculum. Educator, learner, print-layout and assistive-technology review remain pending. Text-only availability does not establish accessibility compliance.

## What this adds, and what already existed

The archive's [Cloud City v7 record](../project-map.md#cloud-city-v7) already describes a standing-wave lab alongside other browser lessons. Its exact source and current hosted behavior were not inspected for this contribution. This companion is new original writing, not recovery of that lab, and does not claim the topic was absent from Jonathan's earlier work.

The [motion lesson](motion-trace-shape.md) pairs two coordinates to make a Lissajous curve. Here we study displacement at many positions along one string. Lumen's [octave activity](../../tools/lumen-commons/README.md) is another related starting point. These activities can complement each other without sharing one physical model.

## 1. Make the model precise

Imagine a uniform, flexible string of length L, held fixed at both ends. The string is under constant tension. Displacements and slopes are small; bending stiffness, damping and changes in tension are neglected. We examine one transverse normal mode at a time, not the complete sound of a real instrument. Wave speed v is constant in this ideal model. These assumptions and the fixed-end modes are supported by references SW-01 and SW-02 below.

The horizontal position x runs from 0 at the left end to L at the right end. Displacement y tells how far that piece of string is above or below its straight equilibrium position. A **node** stays at zero displacement throughout the vibration. Both fixed ends are nodes. An **antinode** is a position with the largest oscillation amplitude in that mode. It is a location, not a crest travelling along the string.

A **wavelength** is the length of one full spatial repeat of the corresponding travelling waves. Each arch between adjacent nodes spans half a wavelength. If n such arches fit into length L, then:

- L = n × wavelength / 2, so wavelength = 2L / n.
- Frequency = wave speed / wavelength, so f_n = n × v / (2L).
- n is a positive integer. The first mode, n = 1, is the fundamental or first harmonic. The second harmonic is the first overtone.

The allowed frequencies are spaced by f_1, but that does not require every mode to be present or equally strong. A pluck usually involves a mixture whose amplitudes depend on how the string is displaced. We do not model that mixture here (SW-03).

## 2. Three worked examples

### Example 1: fit the first three patterns

Use an invented ideal string with **L = 0.60 m** and **v = 120 m/s**. These are chosen model values, not measurements. First compute 2L = 1.20 m. One half-wavelength fills the string in mode 1, so its wavelength is 1.20 m. Its frequency is 120 / 1.20 = 100 Hz.

For mode 2, two half-wavelengths fill the same length: wavelength = 1.20 / 2 = 0.60 m and frequency = 120 / 0.60 = 200 Hz. For mode 3, wavelength = 1.20 / 3 = 0.40 m and frequency = 120 / 0.40 = 300 Hz.

| Mode n | Wavelength (m) | Frequency (Hz) | Internal nodes | All nodes, including ends (m) |
| --- | --- | --- | --- | --- |
| 1 | 1.20 | 100 | 0 | 0, 0.60 |
| 2 | 0.60 | 200 | 1 | 0, 0.30, 0.60 |
| 3 | 0.40 | 300 | 2 | 0, 0.20, 0.40, 0.60 |

Without the table: the first pattern has one arch, no internal node and two endpoint nodes. The second has two arches meeting at the midpoint, with three nodes altogether. The third has three arches separated at 0.20 m and 0.40 m, with four nodes altogether. Neighboring arches have opposite displacement signs at a non-flat snapshot of a single mode. A sketch may exaggerate height; label it as such.

**Check:** multiplying each wavelength by its frequency gives the same 120 m/s. Higher mode number changes the wavelength and frequency, not the speed on this unchanged string. The second harmonic is an octave above the fundamental because its frequency is doubled; this does not make every pair of successive harmonics an octave.

### Example 2: a flat instant does not make every point a node

Keep the same string and select mode 2 with a maximum displacement of **A = 1 mm**. Its frequency is 200 Hz, so one period is 1/200 s = 0.005 s = 5 ms. One millisecond (ms) is 0.001 s. Start with the left arch at maximum positive displacement and the right arch at maximum negative displacement.

The following table gives actual displacement in millimetres at five chosen positions. The time column advances by one quarter of this mode's period.

| Time (ms) | y at x=0 m (mm) | y at x=0.15 m (mm) | y at x=0.30 m (mm) | y at x=0.45 m (mm) | y at x=0.60 m (mm) |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | -1 | 0 |
| 1.25 | 0 | 0 | 0 | 0 | 0 |
| 2.50 | 0 | -1 | 0 | 1 | 0 |
| 3.75 | 0 | 0 | 0 | 0 | 0 |
| 5.00 | 0 | 1 | 0 | -1 | 0 |

Read it in words: the point at 0.15 m goes from +1 mm, through zero, to -1 mm, through zero, and back to +1 mm. The point at 0.45 m does the opposite. The three nodes stay at zero in every row. At 1.25 ms the entire ideal string is momentarily straight, but most points are moving through equilibrium. A single photograph cannot establish that a point is a node.

**Optional equation check:** y(x,t) = A sin(nπx/L) cos(2πf_n t), using t in seconds. A is the maximum displacement of this standing mode, not the amplitude of each constituent travelling wave. For n = 2 at the five positions above, the sine factors are 0, 1, 0, -1, 0. At the five times, the cosine factors are 1, 0, -1, 0, 1. Multiply a position factor, a time factor and A to recover each entry. The formula applies at all positions; the table is a sparse set of samples.

### Example 3: change length rather than mode

Now shorten the model string to **L = 0.30 m**, keeping wave speed at **120 m/s**, and use its fundamental. The new wavelength is 2 × 0.30 = 0.60 m. The new fundamental frequency is 120 / 0.60 = 200 Hz. Its only nodes are its new endpoints, 0 and 0.30 m.

That equals the original string's second-harmonic frequency, but the systems and patterns differ. The original 0.60 m string had a node at 0.30 m inside it; in the shortened string that position is an endpoint. Say what changed before comparing frequency alone. In a physical model, keeping the same tension and linear mass density would keep v unchanged (SW-02); cutting or retuning a real instrument can involve other changes.

## 3. Try five questions

Read the hints only when helpful. Drawing is optional. The solutions follow in a separate section.

1. **The next pattern.** For the original 0.60 m string at 120 m/s, find mode 4's wavelength, frequency, internal-node count and all node positions. Hint: divide the length into four equal arches.
2. **A frequency match.** A second ideal string has length 1.20 m and wave speed 120 m/s. Which mode has frequency 200 Hz? Hint: first find that string's fundamental; do not copy its mode number from the original string.
3. **Change the height.** For Example 2, increase A from 1 mm to 2 mm while retaining the ideal small-displacement model and all other parameters. What are y at x=0.15 m and x=0.45 m at t=0? What are the frequency and period? Hint: separate the multiplier A from the time factor.
4. **Read a snapshot carefully.** At 1.25 ms in Example 2, is x=0.15 m a node? Would halving the speed of an optional animation change the model's 200 Hz? Hint: compare several model times; distinguish model time from viewing time.
5. **Check the analogy.** Someone says, “The three arches of mode 3 show three possible paths for an electron, and its 300 Hz is that atom's natural musical note.” Identify two unsupported jumps. Hint: ask what y represents and what an atomic orbital represents. Read the boundary note below if this is new vocabulary.

## 4. Solutions and reasons

1. **Mode 4:** wavelength = 1.20 / 4 = **0.30 m**; frequency = 120 / 0.30 = **400 Hz**. There are **3 internal nodes** and **5 nodes including the ends**, at **0, 0.15, 0.30, 0.45, 0.60 m**. Four arches each occupy 0.15 m, half the wavelength. There are n-1 internal nodes and n+1 total nodes for these fixed-end modes.
2. **Mode 4 again, on a different string:** fundamental = 120 / (2 × 1.20) = **50 Hz**. Since 200 / 50 = **4**, the requested mode is **n = 4**, with wavelength **0.60 m**. On the original string, 200 Hz was mode 2. A frequency by itself does not identify a mode without the system's parameters.
3. **+2 mm and -2 mm; still 200 Hz and 5 ms.** Multiplying the displacement changes the height and leaves the zero positions and time factor unchanged. This amplitude independence belongs to the stated linear idealization. It is not a rule for every real instrument at every amplitude.
4. **No, and no.** At x=0.15 m the displacement is +1 mm at t=0 and -1 mm at t=2.50 ms, so that position does not remain at zero. Slower presentation changes how long you watch; the model still makes 200 cycles per model second. If the underlying model parameters changed instead, frequency would need to be recalculated.
5. **The plotted quantity and the claimed sound have changed without a model connecting them.** String displacement is not electron position probability or an electron trajectory. The exercise's chosen 300 Hz describes this string mode; it supplies no atomic spectral calculation. Assigning a musical tone to atomic data requires an explicit mapping and does not establish an intrinsic note.

## 5. Where the atomic analogy stops

An atomic orbital is a quantum wavefunction. Its squared magnitude, |ψ|², gives a position probability density. It is not a drawn route followed by an electron or the transverse displacement of a material string. Nodes and allowed states provide a useful comparison of mathematical ideas, but the governing equations and physical interpretations differ (SW-04).

Nothing here computes orbitals, atomic energy levels or emission spectra. A musical mapping of data is a design choice, as discussed in the archive's [music chapter](../../chapters/04-music-and-expression.md). This lesson also does not predict timbre, loudness, hearing safety or how a particular instrument behaves.

## Sources, provenance and reuse

The following pages were opened and inspected on **2026-11-09**. References support the stated model and distinctions, not educational effectiveness. All teaching prose, chosen numbers, tables and questions above are original. No external diagrams, animations, articles or source code are copied into this lesson. Three references share OpenStax authorship; they are not three independent confirmations.

- **SW-01:** [OpenStax, University Physics Volume 1, 16.6: Standing Waves and Resonance](https://openstax.org/books/university-physics-volume-1/pages/16-6-standing-waves-and-resonance). Inspected the fixed-end discussion and equations 16.15–16.16: allowed wavelengths/frequencies, node boundary conditions, harmonic and overtone terminology. We use a separate A convention for the maximum standing-mode displacement.
- **SW-02:** [OpenStax, University Physics Volume 1, 16.3: Wave Speed on a Stretched String](https://openstax.org/books/university-physics-volume-1/pages/16-3-wave-speed-on-a-stretched-string). Inspected the constant-linear-density and small-slope assumptions and equation 16.8, v = sqrt(tension / linear mass density). This supports the held-speed condition in Example 3; learners need not calculate tension here.
- **SW-03:** [Daniel A. Russell, Penn State: The Vibration of a Fixed-Fixed String](https://www.acs.psu.edu/drussell/Demos/string/Fixed.html). Inspected “The natural modes” and the plucked-string discussion as independent support for fixed-end mode shapes and the distinction between a single mode and a mixture. The page reserves text/image reuse rights; this lesson links to it without importing its material.
- **SW-04:** [OpenStax, Chemistry 2e, 6.3: Development of Quantum Theory](https://openstax.org/books/chemistry-2e/pages/6-3-development-of-quantum-theory). Inspected “The Quantum–Mechanical Model of an Atom,” specifically probability amplitudes and |ψ|². Its earlier circular-wave discussion is historical context, not a literal electron-path model adopted here.

Suggested attribution: “String harmonics: a paper-first companion, Jonathan's Creative Archive Contributors, 2026, version 1.0.0, CC BY 4.0,” with this lesson's repository link and the [license link](https://creativecommons.org/licenses/by/4.0/). Say what you changed when adapting it. Linked sources retain their own rights.

## A small next contribution

Check one example independently, or explain one confusing sentence in a plain-text alternative. Keep the original and your revision, show the calculation and units, cite any source you use, and state what you did not test. An archive maintainer can review the proposed change; no outside reviewer or educator endorsement is implied. Sharing is optional, and learner-identifying information is unnecessary. See the [contribution guide](../../CONTRIBUTING.md).

The [dated review](../reviews/string-harmonics-2026-11-09.md) describes numerical checks and remaining limits. From the repository root, contributors who already have Python can run `python3 -B -m unittest discover -s tests -p 'test_string_harmonics_lesson.py'`. No code execution is needed to read or use this companion offline.
