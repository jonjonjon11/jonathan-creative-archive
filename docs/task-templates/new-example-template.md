# New Worked Example Template

Use this template to add a new worked example to the Motion → Trace → Shape module.

## Instructions

1. Review the three existing worked examples in `data/modules.json` (search for `"worked_examples"`)
2. Choose a frequency ratio or phase offset not yet demonstrated
3. Work through the mathematics yourself
4. Test your example in the interactive lab at `tools/motion-trace-shape/Motion-Trace-Shape.html`
5. Write your example using this template
6. Submit via pull request

---

## New Worked Example

Replace everything below with your example. Keep the JSON structure exactly as shown.

```json
{
  "id": "EXE-LJ-004",
  "title": "[Your Example Title]",
  "difficulty": "beginner OR intermediate OR advanced",
  "scenario": "[Brief description of the setup: frequencies, phase offset, what makes it interesting]",
  "parameters": {
    "x_frequency": [integer 1-4],
    "y_frequency": [integer 1-4],
    "phase_offset_degrees": [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345],
    "time_window_seconds": 8
  },
  "prediction": "[What shape or pattern do you expect to see? Be specific.]",
  "step_by_step": [
    "[At time t=0: describe the starting positions of x and y]",
    "[At time t=[some moment]: describe what's happening]",
    "[At time t=[another moment]: describe the progression]",
    "[Conclude with how the pattern completes]"
  ],
  "explanation": "[Why does this combination of parameters produce this shape? Explain the relationship between frequency ratio and phase offset.]",
  "mathematical_form": "[Equations: x(t) = ..., y(t) = ..., and any derived relationships like x² + y² = ... if applicable]",
  "verification": "[How can someone test this in the interactive lab? Example: 'Set x cycles to 1, y cycles to 3, phase offset to 45°, and press Play.']"
}
```

---

## Choosing Your Example

### Suggested Frequency Ratios
- **1:2** (already done: figure-eight)
- **1:3** — Creates a three-lobed shape
- **2:3** — Creates a six-pointed pattern
- **3:2** — Similar to 2:3 but reversed
- **3:4** — Creates a more complex shape
- **4:3** — Another interesting ratio
- **5:2** or **5:3** — High ratios create intricate patterns

### Suggested Phase Offsets (for same frequencies)
- **45°** — Creates an ellipse (between line and circle)
- **135°** — Another ellipse orientation
- **225°** — Yet another orientation

### Educational Value

Choose an example that:
- Teaches something new that isn't covered by the existing three examples
- Shows a clear pattern or progression
- Helps learners see how frequency ratio and phase work together
- Is testable in the interactive lab

---

## Verification Checklist

Before submitting, verify:

- [ ] I have tested my example in the interactive lab
- [ ] The mathematical equations are correct
- [ ] The prediction matches what I observed
- [ ] The step-by-step explanation is clear and accurate
- [ ] The JSON structure is valid (no syntax errors)
- [ ] The example teaches something not already covered
- [ ] The explanation is accessible to beginners
- [ ] The verification instructions are clear enough for someone else to test

---

## Example of a Good New Example

Here's a complete example to show you the format:

```json
{
  "id": "EXE-LJ-004",
  "title": "The Three-Lobed Flower: 1:3 Frequency Ratio",
  "difficulty": "beginner",
  "scenario": "The x-motion oscillates once while the y-motion oscillates three times. Both start together (phase offset = 0°). This creates a shape with three distinct lobes.",
  "parameters": {
    "x_frequency": 1,
    "y_frequency": 3,
    "phase_offset_degrees": 0,
    "time_window_seconds": 8
  },
  "prediction": "A three-lobed or three-pointed shape, similar to a flower or cloverleaf. The three lobes appear symmetrically around the center.",
  "step_by_step": [
    "At t=0: both x and y start at the center (0, 0)",
    "As t increases: x moves slowly right while y oscillates quickly up-down-up-down-up",
    "At t≈2.67: x reaches its rightmost point (+1) and y completes 1 full cycle, returning to 0",
    "As t continues: x moves back left while y oscillates 2 more times",
    "By t=8: x completes one cycle and y completes three, creating a symmetric three-lobed pattern"
  ],
  "explanation": "The 1:3 frequency ratio means y oscillates three times for every one oscillation of x. This creates three distinct lobes because y's quick oscillations are 'sampled' at three different x-positions (right, center, and left). The resulting shape is symmetric and resembles a flower.",
  "mathematical_form": "x(t) = sin(2π · 1 · t / 8) = sin(πt / 4)\ny(t) = sin(2π · 3 · t / 8) = sin(3πt / 4)\nThe frequency ratio 3:1 determines the three-lobed structure.",
  "verification": "In the interactive lab: Set x cycles to 1, y cycles to 3, phase offset to 0°. Press Play. You should see the point trace a symmetric three-lobed shape."
}
```

---

## Submitting Your Example

1. Fork or clone the repository
2. Edit `data/modules.json`
3. Find the `"worked_examples"` array (around line 1800)
4. Add your new example to the array (don't forget the comma after the previous example)
5. Run validation:
   ```bash
   python3 -m json.tool data/modules.json > /dev/null
   ```
   (This checks for JSON syntax errors)
6. Commit and open a pull request
7. In the PR description, reference the task: "Addresses TASK-motion-add-example"

---

## Questions?

If you're unsure about something:
- Re-read the existing worked examples
- Test your idea in the interactive lab first
- Check the references (Wolfram MathWorld, OpenStax)
- Ask in the repository issues

Thank you for expanding the Motion → Trace → Shape lesson!
