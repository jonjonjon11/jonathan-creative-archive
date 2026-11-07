# Motion, traces, and shape: a paper-first lesson

**Module MOD-lissajous-motion-001 · version 1.0.1 · corrected draft, pending human acceptance**

Original lesson text and tables: Jonathan’s Creative Archive, 2026. [CC BY 4.0](../../LICENSE). This is a mathematical activity, not a validated curriculum. No learner, screen-reader, device, or rendered-browser testing is claimed.

Use this file offline in a text or Markdown reader. The tables, three worked examples, five exercises, and solutions are all included. Printing is optional and untested. No account, animation, calculator, or internet connection is required for the table-based path. A suggested 30 minutes is a planning estimate, not a time limit.

## Learning goals

- Understand how two independent oscillating motions combine to create a composite trace
- Distinguish between model time, motion parameters (frequency and phase), and visual representation
- Recognize Lissajous curves as patterns produced by frequency and phase relationships
- Make predictions about shapes before viewing results
- Use coordinate values to check a shape prediction and explain why frequency ratio alone is not enough

## Read the settings carefully

The existing keys x_frequency and y_frequency mean repeat counts per 8 model seconds, not hertz. For a repeat count n, frequency is n/8 cycles per model second and period is 8/n model seconds. Ratios are always written x:y. Phase is added to the y angle; 90° advances y by one quarter of its own cycle. Coordinates have equal amplitude 1 model unit.

The JSON keeps the existing parameter key names for compatibility. The numerical lab has not changed. Its controls allow integer repeat counts 1–4 and phase 0–360° in 15° steps.

# Why This Matters

A repeated motion can look very different depending on how we record it. A point can move along a number line, leave a wave-shaped position-versus-time trace, or supply one coordinate of a two-dimensional drawing. These are different views of the same position data.

In this lesson, we pair a left-right rhythm with an up-down rhythm. At each shared time, their two positions give one point on an x-y graph. With a few settings, the point follows a line, circle, or sideways figure-eight. You can investigate with the tables below and a pencil, or simply read the ordered coordinates and describe them in words. Animation is optional.

These mathematical drawings belong to the Lissajous family. Oscillations also matter in sound and physical systems, but pairing two coordinates is not the same operation as adding two sounds. This lesson specifies positions directly. It does not simulate a musical instrument, planetary orbit, force, or measured object.

# One Motion at a Time

A complete oscillation returns to the same position and the same stage of motion. Going from the center to one end is only a quarter-cycle. In our first example, a point starts at the center, reaches the right end after 2 model seconds, crosses the center after 4, reaches the left end after 6, and returns to the center moving right after 8.

The amplitude is the largest distance from the center: 1 model unit. The period is the time for a complete cycle: 8 model seconds. Frequency counts complete cycles per unit time, so one cycle in 8 model seconds is 1/8 cycle per model second. The lab controls show repeat counts per 8-second window, not cycles per second. With two repeats in that window, the period is 4 model seconds and the frequency is 2/8.

A time trace puts time on the horizontal axis and position on the vertical axis. The point's physical-looking left-right movement becomes an up-down curve on that graph because the vertical axis represents position, not a second direction of travel. Label both axes to avoid mixing the views.

Our equation is x(t) = sin(2π × n_x × t / 8), where n_x is the repeat count and t is model time. The sine argument is an angle in radians. You do not need to calculate sine to start: the supplied tables give the required positions. All coordinates are model units, not measurements in metres.

# Two Motions Together

For every time, read both positions before plotting anything. The ordered pair (x, y) means move x units horizontally and y units vertically from the origin. Negative x means left; negative y means down. Time does not label either axis of the shape plot. Instead, time determines the order in which points are visited.

We write ratios as x:y. One horizontal repeat and two vertical repeats therefore means 1:2. Our y equation is y(t) = sin(2π × n_y × t / 8 + φ), where φ is the phase angle in radians. The lab displays this angle in degrees: 90° equals π/2 radians. Adding 90° advances y by one quarter of its own cycle; it does not delay when the clock starts.

When repeat counts match and phase is 0°, x equals y at every time. The path is the line segment y = x. With the same repeat counts, equal amplitudes, and phase 90°, the path is a unit circle. With x:y = 1:2 and phase 0°, the path has two side-by-side loops: a sideways figure-eight.

Phase matters as well as ratio. Keeping 1:2 but changing phase to 90° gives a retraced parabola segment, not a figure-eight. Exercise 5 checks why. No general petal-count rule is needed. A 360° phase increase restores the same position at every time; a 180° increase changes the sign of y and generally changes the path. Equal plot scales are necessary to display a circle without stretching it.

## Seven steps without animation

1. Choose the line, circle, or figure-eight example. Read its settings and prediction. You may work with words and numbers alone; drawing is optional.
2. Read one row of its table: t is model time; x and y are positions at that same time. The tables use integer times from 0 to 8. The rounded number 0.707107 is approximately √2/2; it is between 0 and 1, not a new maximum.
3. For a time trace, put time from 0 to 8 on a horizontal axis and position from −1 to 1 on a vertical axis. Plot the table's (t, x) pairs. Make a second trace using (t, y). Label the axes so time is not confused with x-position.
4. For the shape plot, use two equal-scale axes from −1 to 1. Plot (x, y), not (t, y). For example, the figure-eight row at t=1 means move about 0.707107 units right and 1 unit up. In words, that point is at the top of the right loop.
5. Follow points in increasing time order and add arrows, or read the ordered coordinates aloud. Connect only as a rough sketch: straight segments between sparse samples are not the exact continuous curve. The equations and explanations establish the exact shape. For the circle, go top, right, bottom, left, top. For the line, return over the same segment. For the figure-eight, visit the right loop and then the left.
6. Check the t=4 row before guessing that a cycle is complete. The line is crossing the center, the circle is at the bottom, and the figure-eight is crossing into its left loop. Compare with t=0 and the direction of motion. A matching position alone does not prove a complete repeat.
7. Answer the five exercises before reading the solutions. Explain one result in your own words. If you use the optional lab later, keep Still mode on and compare its numeric readout with your table; no Play action is required.

## Example 1: The Straight Diagonal Line

Both motions complete one cycle in 8 model seconds. Their phase offset is 0°.

**Prediction:** The point retraces a straight line segment from (−1, −1) to (1, 1), with positive slope.

1. At t=0: x = 0 and y = 0; the point starts at the center moving toward positive coordinates.
2. At t=2: x = 1 and y = 1; both coordinates reach their maximum.
3. At t=4: x = 0 and y = 0; the point crosses the center, moving toward negative coordinates.
4. At t=6: x = −1 and y = −1; both coordinates reach their minimum.
5. At t=8: x = 0 and y = 0; one complete oscillation is finished.

The same sine value supplies both coordinates, so x always equals y. Turning back at the ends changes the direction of travel, not the line into the opposite diagonal.

x(t) = sin(2πt / 8)
y(t) = sin(2πt / 8)
Therefore y = x, with −1 ≤ x ≤ 1.

Values rounded to six decimal places; zero is exact at the listed crossings. Rounded 0.707107 represents √2/2.

Each row reads “time in model seconds; x-position; y-position.” The same numbers are available as ordered sentences immediately after the table.

| t | x | y |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 0.707107 | 0.707107 |
| 2 | 1 | 1 |
| 3 | 0.707107 | 0.707107 |
| 4 | 0 | 0 |
| 5 | -0.707107 | -0.707107 |
| 6 | -1 | -1 |
| 7 | -0.707107 | -0.707107 |
| 8 | 0 | 0 |

- At t=0: x=0, y=0.
- At t=1: x=0.707107, y=0.707107.
- At t=2: x=1, y=1.
- At t=3: x=0.707107, y=0.707107.
- At t=4: x=0, y=0.
- At t=5: x=-0.707107, y=-0.707107.
- At t=6: x=-1, y=-1.
- At t=7: x=-0.707107, y=-0.707107.
- At t=8: x=0, y=0.

Optional lab check: set x repeats to 1, y repeats to 1, and phase to 0°. Keep Still mode on and set time to 0, 2, 4, 6, and 8; compare the position readout with the table. The paper calculation does not require the lab.

## Example 2: The Perfect Circle

Both motions oscillate at the same frequency, but the y-motion starts a quarter-cycle (90°) ahead of the x-motion.

**Prediction:** A unit circle traversed clockwise as model time increases, with positive y upward. It is not retraced back and forth in one cycle.

1. At t=0: x = 0 and y = 1; start at the top of the circle.
2. At t=2: x = 1 and y = 0; reach the rightmost point.
3. At t=4: x = 0 and y = −1; reach the bottom, not the leftmost point.
4. At t=6: x = −1 and y = 0; reach the leftmost point.
5. At t=8: x = 0 and y = 1; return to the top after one clockwise circuit.

With θ = 2πt/8, the coordinates are sin(θ) and cos(θ). The identity sin²(θ) + cos²(θ) = 1 keeps the point exactly one model unit from the origin. Both amplitudes are 1; unequal amplitudes would generally give an ellipse instead.

Let θ = 2πt / 8. Then x = sin(θ) and y = sin(θ + π/2) = cos(θ).
x² + y² = sin²(θ) + cos²(θ) = 1.

Values rounded to six decimal places; zero is exact at the listed crossings. Rounded 0.707107 represents √2/2.

Each row reads “time in model seconds; x-position; y-position.” The same numbers are available as ordered sentences immediately after the table.

| t | x | y |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 0.707107 | 0.707107 |
| 2 | 1 | 0 |
| 3 | 0.707107 | -0.707107 |
| 4 | 0 | -1 |
| 5 | -0.707107 | -0.707107 |
| 6 | -1 | 0 |
| 7 | -0.707107 | 0.707107 |
| 8 | 0 | 1 |

- At t=0: x=0, y=1.
- At t=1: x=0.707107, y=0.707107.
- At t=2: x=1, y=0.
- At t=3: x=0.707107, y=-0.707107.
- At t=4: x=0, y=-1.
- At t=5: x=-0.707107, y=-0.707107.
- At t=6: x=-1, y=0.
- At t=7: x=-0.707107, y=0.707107.
- At t=8: x=0, y=1.

Optional lab check: choose Circle, keep Still mode on, and compare the readout at 0, 2, 4, 6, and 8 model seconds. Use equal horizontal and vertical scales on paper.

## Example 3: The Figure-Eight

The x:y repeat-count ratio is 1:2. Horizontal motion completes one cycle and vertical motion completes two in 8 model seconds. Phase is 0°.

**Prediction:** A sideways figure-eight with one loop on the right and one on the left, meeting at the origin.

1. At t=0: x = 0 and y = 0; start at the crossing.
2. At t=1: x ≈ 0.707107 and y = 1; reach the top of the right loop.
3. At t=2: x = 1 and y = 0; reach the rightmost point.
4. At t=3: x ≈ 0.707107 and y = −1; reach the bottom of the right loop.
5. At t=4: x = 0 and y = 0; finish the right loop. The y-motion has completed one cycle, while x has completed half a cycle.
6. From t=4 to t=8: x is negative between the endpoints, so the point traces the left loop. It reaches (−1, 0) at t=6 and returns to (0, 0) at t=8.

For 0 < t < 4, x is positive, placing the first loop on the right. For 4 < t < 8, x is negative, placing the second on the left. Over all 8 model seconds, y completes two full cycles. The center crossing at t=4 is not a full repeat of the motion: the point heads into the other loop.

Let θ = 2πt / 8. Then x = sin(θ) and y = sin(2θ).
y² = 4x²(1 − x²). The x:y ratio is 1:2 and phase is 0°; both settings matter.

Values rounded to six decimal places; zero is exact at the listed crossings. Rounded 0.707107 represents √2/2.

Each row reads “time in model seconds; x-position; y-position.” The same numbers are available as ordered sentences immediately after the table.

| t | x | y |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 0.707107 | 1 |
| 2 | 1 | 0 |
| 3 | 0.707107 | -1 |
| 4 | 0 | 0 |
| 5 | -0.707107 | 1 |
| 6 | -1 | 0 |
| 7 | -0.707107 | -1 |
| 8 | 0 | 0 |

- At t=0: x=0, y=0.
- At t=1: x=0.707107, y=1.
- At t=2: x=1, y=0.
- At t=3: x=0.707107, y=-1.
- At t=4: x=0, y=0.
- At t=5: x=-0.707107, y=1.
- At t=6: x=-1, y=0.
- At t=7: x=-0.707107, y=-1.
- At t=8: x=0, y=0.

Optional lab check: choose Figure-eight, keep Still mode on, and compare integer times from 0 through 8 with the table. At t=4 both positions are zero; at t=2 the x-position is at its maximum.

## Five exercises

Try each prompt before reading the solution section.

### Exercise 1

**Make a prediction:** If both motions have the same frequency and start together (phase offset = 0°), describe the shape you expect to see. Draw a rough sketch or explain in words why that shape makes sense.

### Exercise 2

**Calculate:** Suppose x = sin(θ) and y = cos(θ), with θ = 2πt/8. Verify that x² + y² = 1. What shape does this describe, and where is the point at t=4 model seconds?

### Exercise 3

**Predict and check:** Set x repeats to 1, y repeats to 2, and phase to 0°. Predict the shape. Use the table or optional lab to locate the point at t=2 and t=4. How many full y cycles have elapsed by t=4?

### Exercise 4

**Explore phase:** Keep both repeat counts at 1. Predict the paths at 0°, 45°, 90°, 135°, 180°, 270°, and 360°. Which are lines or circles? Does a 180° phase increase always leave the same path?

### Exercise 5

**Challenge: same ratio, different shape.** Keep x repeats at 1 and y repeats at 2, but change phase from 0° to 90°. With θ = 2πt/8, use sin(2θ + π/2) = cos(2θ) and cos(2θ) = 1 − 2sin²(θ). Find y in terms of x. Predict the shape and its positions at t=0, 2, 4, 6, and 8. All these settings are available in the lab.

## Solutions and explanations

### Solution 1

The path is the positive-slope segment y = x from (−1, −1) to (1, 1). Reversing travel along this same segment does not change its slope. At t=4 in the one-repeat example, the point is at the center; the minimum occurs at t=6.

**What to notice:** For this equal-amplitude model, equal repeat counts and zero phase give y = x. A 180° phase offset instead gives y = −x.

### Solution 2

The identity sin²(θ) + cos²(θ) = 1 gives a circle of radius 1 model unit. At t=4, θ = π, so (x, y) = (0, −1). Equal axis scales show the circle without stretching it.

**What to notice:** Equal repeat counts, equal amplitudes, and a 90° offset produce a circle in this model.

### Solution 3

The figure-eight has side-by-side loops. At t=2 the point is (1, 0), and at t=4 it is (0, 0). The y-motion completes one full cycle by t=4 and two by t=8. The x-motion completes half a cycle by t=4 and one by t=8.

**What to notice:** A return to the same position need not mean the full motion has repeated. At the central crossing, the point can be heading into a different loop.

### Solution 4

At 0° and 360°, the line is y = x. At 180°, the line is y = −x. At 90° and 270°, the path is the same unit circle, but the direction of travel is opposite. At 45° and 135°, the paths are ellipses with different orientations. A 180° phase increase reflects y to −y and does not always preserve the path; 0° and 180° are a counterexample. A 360° increase restores the same positions at the same times.

**What to notice:** Distinguish the set of visited points, the order of traversal, and the position at a particular time. Equal-looking paths do not imply identical motions.

### Solution 5

Since x = sin(θ), y = cos(2θ) = 1 − 2x², with −1 ≤ x ≤ 1. This is a downward-opening parabola segment, retraced as x oscillates, not a figure-eight. The five positions are (0, 1), (1, −1), (0, 1), (−1, −1), and (0, 1). The frequency ratio stays 1:2 while the phase changes the shape.

**What to notice:** A ratio alone does not fix a Lissajous shape. Derive coordinates or a curve equation instead of using an unsupported rule for counting petals.

## Sources and reuse

The following pages were inspected on 2026-11-07. They support definitions and identities, not learner outcomes. All teaching prose, examples, and coordinate tables here are original; no source prose or diagrams are bundled. Linked sources retain their own licenses. Two references share OpenStax authorship and are not independent confirmations.

- [University Physics Volume 1, §15.1: Simple Harmonic Motion](https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion). Defines sinusoidal position, amplitude, period, frequency, and phase for oscillatory motion Foundation for the mathematical model used in this lesson

- [Lissajous Curve — from MathWorld](https://mathworld.wolfram.com/LissajousCurve.html). Explains the mathematics of Lissajous curves, frequency ratios, parametric equations, and common shapes Comprehensive mathematical reference

- [Lissajous Curves](https://mathshistory.st-andrews.ac.uk/Curves/Lissajous/). Documents the parametric sine-curve family and historical work by Bowditch and Lissajous. Historical context, not evidence of educational effectiveness. Replaces an unverified historical title in module version 1.0.0.

- [Precalculus, 7.2: Sum and Difference Identities](https://math.libretexts.org/Bookshelves/Precalculus/Precalculus_1e_%28OpenStax%29/07%3A_Trigonometric_Identities_and_Equations/7.02%3A_Sum_and_Difference_Identities). The sine and cosine angle-sum identities support the phase-shift and double-angle derivations. Derive cos(2θ) = cos²(θ) − sin²(θ) = 1 − 2sin²(θ) using the cosine-sum and Pythagorean identities. The worksheet examples are original.

## Optional lab and contribution review

For optional interaction, see the [lab instructions](../../tools/motion-trace-shape/README.md). A source preview on GitHub does not execute the HTML lab. Downloading the repository keeps local links together.

For a review outside this archive, copy this lesson, its [canonical record](../../data/modules.json), the [model](../../tools/motion-trace-shape/src/core.js), and the [review handoff](../reviews/motion-lesson-corrections.md) with the license. Work locally and return findings voluntarily. No external contact, account creation, or upload is needed. Do not collect learner-identifying information. No reviewer or educator endorsement is implied.

Suggested attribution: “Motion, Traces, and Shape, Jonathan’s Creative Archive, 2026,” with a link to [the archive](https://github.com/jonjonjon11/jonathan-creative-archive), the license, and a description of any changes.
