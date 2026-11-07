# Knowledge Module Schema v1.0

A modular, portable format for educational content in the Knowledge Commons. Each module is self-contained, preserves its license and sources, and can grow incrementally toward a comprehensive curriculum.

## Module Record (JSON)

```json
{
  "schema_version": "1.0",
  "module": {
    "id": "MOD-motion-trace-shape-001",
    "version": "1.0.0",
    "title": "Motion, Traces, and Shape: Discovering Patterns in Repeating Motion",
    "subtitle": "How two oscillating coordinates combine to create lines, circles, and figure-eights",
    "license": "CC BY 4.0",
    "license_uri": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "Jonathan's Creative Archive, 2026",
    "authors": ["Archive Contributors"],
    "last_reviewed": "2026-11-07",
    "review_status": "verified_calculations_pending_learner_evidence",
    
    "learning_objectives": [
      "Understand how two independent oscillating motions combine to create a composite trace",
      "Distinguish between model time, motion parameters (frequency and phase), and visual representation",
      "Recognize Lissajous curves as patterns produced by frequency and phase relationships",
      "Make predictions about shapes before viewing results"
    ],
    
    "prerequisites": [
      {
        "id": "PREREQ-basic-functions",
        "title": "Basic functions and graphing",
        "description": "Ability to read a graph with x and y axes, understand that a function maps inputs to outputs"
      },
      {
        "id": "PREREQ-sine-cosine",
        "title": "Sine and cosine functions (optional)",
        "description": "Helpful but not required; the lesson can be learned from direct observation first"
      }
    ],
    
    "expected_level": "beginner",
    "time_estimate_minutes": 30,
    "accessibility_level": "partial",
    
    "content": {
      "introduction": {
        "plain_text": "# Why This Matters\n\nWhen two things oscillate at different rates or start at different times, their combined effect can create beautiful, predictable patterns. This happens everywhere: in music (different frequencies combine into chords), in physics (planetary orbits, wave interference), and in art (from patterns in nature to designed graphics). By understanding how two simple back-and-forth motions combine, you unlock a lens for seeing order in complexity.",
        "estimated_reading_minutes": 2
      },
      
      "core_lesson": {
        "sections": [
          {
            "title": "Section 1: One Motion at a Time",
            "content": "# One Motion at a Time\n\nStart with a single oscillating motion:\n- Imagine a point moving left and right at a steady rhythm.\n- Time passes from left to right on a horizontal axis.\n- The vertical position shows how far left (negative) or right (positive) the point is.\n- The smooth up-and-down curve is called a sinusoid, the shape of simple harmonic motion.\n\n## Key Idea\nThe same motion can be shown three ways:\n1. **As a moving point**: see the position now\n2. **As a time trace**: see the history of positions\n3. **As equations**: x(t) = sin(2πft + φ), where t is time, f is frequency, and φ is phase\n\nEach view reveals something different, but they all describe the same motion.",
            "estimated_reading_minutes": 3,
            "key_terms": ["oscillation", "sinusoid", "frequency", "phase", "amplitude"]
          },
          {
            "title": "Section 2: Combining Two Motions",
            "content": "# Combining Two Motions\n\nNow add a second oscillation in a perpendicular direction:\n- One motion goes left-right (x-coordinate)\n- The other motion goes up-down (y-coordinate)\n- Both start at the same time\n- At every instant, the combined point has one x-position and one y-position\n\n## The Shape That Emerges\nWhen these two motions occur together, the path they trace out depends on:\n1. **The frequency ratio**: how many times one oscillates compared to the other\n2. **The phase offset**: whether they start together or one starts ahead\n\nThese ratios are called Lissajous curves (pronounced \"lee-suh-ZHU\"), named after the mathematician who studied them.\n\n## Three Important Cases\n- **Same frequency, no offset**: straight diagonal line\n- **Same frequency, quarter-cycle offset**: perfect circle\n- **2:1 frequency ratio, together**: figure-eight or infinity symbol",
            "estimated_reading_minutes": 4,
            "key_terms": ["Lissajous curve", "frequency ratio", "phase offset", "composite motion"]
          }
        ]
      },
      
      "worked_examples": [
        {
          "title": "Example 1: The Diagonal Line",
          "scenario": "Both motions oscillate at the same frequency. They start at the same time.",
          "parameters": {
            "x_frequency": 1,
            "y_frequency": 1,
            "phase_offset_degrees": 0
          },
          "prediction": "A straight diagonal line from lower-left to upper-right",
          "explanation": "When both coordinates reach their peaks and valleys at exactly the same time, they move in lockstep. The ratio is 1:1.",
          "mathematical_form": "x(t) = sin(t), y(t) = sin(t) → y = x (the equation of a line)"
        },
        {
          "title": "Example 2: The Circle",
          "scenario": "Both motions oscillate at the same frequency, but one starts a quarter-cycle (90°) ahead.",
          "parameters": {
            "x_frequency": 1,
            "y_frequency": 1,
            "phase_offset_degrees": 90
          },
          "prediction": "A perfect circle",
          "explanation": "The phase offset causes the motions to be out of sync. When x is at zero, y reaches its peak. This quarter-cycle delay traces a circle.",
          "mathematical_form": "x(t) = sin(t), y(t) = sin(t + π/2) = cos(t) → x² + y² = 1 (circle equation)"
        },
        {
          "title": "Example 3: The Figure-Eight",
          "scenario": "The y-motion oscillates twice as fast as the x-motion. Both start together.",
          "parameters": {
            "x_frequency": 1,
            "y_frequency": 2,
            "phase_offset_degrees": 0
          },
          "prediction": "An infinity symbol or figure-eight",
          "explanation": "While the x-motion completes one cycle, y completes two. This 1:2 frequency ratio (with zero phase offset) creates a figure-eight.",
          "mathematical_form": "x(t) = sin(t), y(t) = sin(2t). The ratio 2:1 defines the shape."
        }
      ],
      
      "exercises": [
        {
          "id": "EXE-001",
          "difficulty": "beginner",
          "prompt": "Sketch or predict: if both motions have the same frequency and start together, what do you expect to see? Why?",
          "solution_guidance": "The answer is a diagonal line. Since both coordinates reach their maximums and minimums simultaneously, the combined point traces a straight path. You might sketch a line from the lower-left corner to the upper-right corner.",
          "key_insight": "When frequencies match and phase is zero, the point moves along a single diagonal."
        },
        {
          "id": "EXE-002",
          "difficulty": "beginner",
          "prompt": "Predict what happens if the up-down motion starts 90° (a quarter-cycle) later than the left-right motion, and both have the same frequency.",
          "solution_guidance": "The answer is a circle. The phase offset causes the vertical motion to reach maximum when the horizontal motion is at zero, and vice versa. This creates a circular path.",
          "key_insight": "Phase offset changes the shape without changing the frequencies."
        },
        {
          "id": "EXE-003",
          "difficulty": "intermediate",
          "prompt": "If the left-right motion repeats once per 8-second cycle and the up-down motion repeats twice in the same 8 seconds, what shape might you expect? (Hint: think about how many times the up-down motion completes for each left-right cycle.)",
          "solution_guidance": "The answer is a figure-eight or infinity symbol. A 1:2 frequency ratio means while the x-coordinate completes one oscillation, the y-coordinate completes two. The shape depends also on phase; starting together gives a different figure-eight than starting offset.",
          "key_insight": "Frequency ratios are integers; common ratios like 1:1, 1:2, 2:3 create recognizable families of shapes."
        },
        {
          "id": "EXE-004",
          "difficulty": "intermediate",
          "prompt": "Experiment: Set x-frequency to 3, y-frequency to 2, and phase offset to 0°. Draw or predict the resulting shape. Why does changing the frequency ratio to 2:3 create a different pattern than 1:2?",
          "solution_guidance": "The result is a more complex 3-pointed or flower-like shape. Each frequency ratio produces its own family of curves. The 3:2 ratio means the x-motion oscillates faster, creating more 'petals' or loops.",
          "key_insight": "Higher frequency ratios produce more-complex Lissajous curves with more lobes or petals."
        },
        {
          "id": "EXE-005",
          "difficulty": "advanced",
          "prompt": "Given the equations x(t) = sin(2πt) and y(t) = sin(2πt + π/4), determine whether the resulting shape is a circle or an ellipse. Explain your reasoning using the phase offset.",
          "solution_guidance": "The answer is an ellipse (not a perfect circle). The phase offset is π/4 radians or 45°, not 90°. Only a 90° (π/2 radian) offset produces a circle. A 45° offset rotates and slightly elongates the circle into an ellipse.",
          "key_insight": "Small deviations from a 90° phase offset still produce near-circles but technically ellipses."
        }
      ],
      
      "interactive_experiences": [
        {
          "title": "Motion → Trace → Shape Interactive Lab",
          "type": "browser-based_simulation",
          "format": "Standalone HTML (offline capable)",
          "file_path": "tools/motion-trace-shape/Motion-Trace-Shape.html",
          "description": "Adjust frequencies and phase interactively. See the two separate motions, their time traces, and the resulting shape in real time.",
          "how_to_use": "1. Download the HTML file. 2. Open in any modern browser. 3. Choose a preset (Line, Circle, Figure-Eight). 4. Use Play, Step, or the time slider. 5. Modify repeat counts or phase to make predictions.",
          "capabilities": ["adjustable parameters", "pause-play-step controls", "time slider", "time-trace visualization", "shape visualization", "parameter export"],
          "accessibility_notes": "Keyboard controls, reduced-motion support, text labels on all visuals, high-contrast colors. Real device testing pending.",
          "verification": "18 numerical tests, 14 UI tests, and static checks passed. Real-browser rendering not verified in build environment."
        }
      ],
      
      "text_only_path": "Complete understanding is possible from the prose descriptions, worked examples, and equations, without animation. Readers should independently work through the three examples and five exercises with pencil and paper.",
      
      "visual_aids": [
        {
          "description": "Three separate panels showing (1) two moving points on number lines, (2) their position-versus-time traces stacked vertically, and (3) the resulting shape in the x-y plane",
          "accessible_text": "A diagram with three columns:\nLeft: A horizontal number line from -1 to +1 showing a circle at a position (the x-coordinate). Below it, a similar line showing a diamond at a position (the y-coordinate).\nMiddle: Two stacked graphs. The top shows position vs. time for the x-coordinate (a sine wave). The bottom shows position vs. time for the y-coordinate (another sine wave, possibly offset).\nRight: A square coordinate system with axes from -1 to +1 on both sides, showing the traced path of the combined point (e.g., a line, circle, or figure-eight)."
        }
      ],
      
      "sources_and_references": [
        {
          "id": "SRC-REF-001",
          "type": "academic_textbook",
          "authors": ["OpenStax"],
          "title": "University Physics Volume 1, §15.1: Simple Harmonic Motion",
          "url": "https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion",
          "accessed": "2026-11-07",
          "relevance": "Defines sinusoidal position, amplitude, period, and phase for oscillatory motion",
          "scope": "Foundation for the mathematical model"
        },
        {
          "id": "SRC-REF-002",
          "type": "reference",
          "title": "Wolfram MathWorld: Lissajous Curve",
          "url": "https://mathworld.wolfram.com/LissajousCurve.html",
          "accessed": "2026-11-07",
          "relevance": "Explains Lissajous curves, frequency ratios, phase relationships, and common shapes",
          "scope": "Terminology and mathematical background"
        }
      ],
      
      "license_and_attribution": {
        "content_license": "CC BY 4.0",
        "attribution": "Motion → Trace → Shape Module, Jonathan's Creative Archive, 2026",
        "modifications": "None in this version; original implementation by Archive Contributors"
      },
      
      "scientific_claims": {
        "model_status": "established_mathematics",
        "model_scope": "Analytical sinusoidal functions describing periodic motion",
        "not_included": "Real physical forces, friction, energy, quantum effects, or any measurement in real-world units",
        "distinction": "This lesson demonstrates a mathematical model. It does not simulate actual physical systems; it shows the mathematical patterns that certain physical systems may approximate.",
        "uncertainty": "No experimental data, margins of error, or real-world validation is claimed."
      },
      
      "accessibility_and_limitations": {
        "verified_features": [
          "Keyboard navigation and controls",
          "Reduced-motion system preference support",
          "High-contrast text colors (4.5:1 ratio verified)",
          "Semantic HTML with visible labels and focus",
          "Standalone offline HTML (no external dependencies)"
        ],
        "unverified_features": [
          "Real mobile or touch-screen use",
          "Screen-reader compatibility and testing",
          "Zoom behavior at various levels",
          "Rendering in all browsers"
        ],
        "device_testing_status": "Chromium launch blocked in build environment; no real device testing completed",
        "assistive_technology_status": "Designed with screen-reader intent but not tested with actual assistive technology"
      }
    },
    
    "contribution_opportunities": [
      {
        "task_id": "CONTRIB-motion-001",
        "title": "Test and document real-browser rendering and interaction",
        "description": "Download the HTML file and test it in Firefox, Safari, Chrome, and on a mobile device if possible. Record screenshots, note any rendering issues, and verify that the time slider, buttons, and parameter controls work as expected. Test with a screen reader if you have access.",
        "scope": "Read-only; document findings in a test report. Do not modify the HTML.",
        "time_estimate": "1-2 hours",
        "acceptance_criteria": "A test report (text or Markdown) documenting which browsers were tested, what rendered correctly, what controls worked, and any issues found"
      },
      {
        "task_id": "CONTRIB-motion-002",
        "title": "Add one more worked example or exercise",
        "description": "The module includes three worked examples and five exercises. Add a fourth worked example (e.g., a 3:1 frequency ratio or a specific phase offset challenge) or a sixth exercise at the advanced level. Keep the format consistent: title, scenario, parameters, prediction, explanation, and mathematical form. Source any equations or references.",
        "scope": "Write and test independently; submit for review before merging.",
        "time_estimate": "1-2 hours",
        "acceptance_criteria": "The new example/exercise follows the existing format, includes a correct solution, and is supported by a reference or derivation"
      },
      {
        "task_id": "CONTRIB-motion-003",
        "title": "Improve the text-only accessibility path",
        "description": "Create a detailed, text-only narrative that a person could follow (with pencil, paper, and the interactive HTML) to understand Lissajous curves without relying on animations. Include clear step-by-step instructions, predictions, and explanations of what patterns emerge.",
        "scope": "Write and test with the interactive HTML; submit for review.",
        "time_estimate": "2-3 hours",
        "acceptance_criteria": "A clear prose narrative (500-1000 words) that a reader could follow independently to understand the core concepts"
      }
    ]
  }
}
```

## Rationale

This schema balances:

1. **Completeness**: Every lesson includes objectives, prerequisites, worked examples, exercises, sources, and limitations.
2. **Portability**: Standalone JSON with embedded text; no large binaries or external hosting required.
3. **Accountability**: Explicit license, sources, verification status, and unverified claims are separate.
4. **Accessibility**: Includes text-only paths, visual descriptions, and accessibility considerations tied to evidence.
5. **Growth**: Contribution opportunities guide how the next person improves the lesson.

## Validation Checklist

When adding a module:

- [ ] ID is unique and stable
- [ ] Learning objectives are clear and testable
- [ ] At least three worked examples with solutions
- [ ] At least five exercises with solution guidance
- [ ] All scientific claims distinguish model from reality
- [ ] All formulas and references are checked
- [ ] Limitations and unverified features are explicit
- [ ] At least one interactive or text-based experience
- [ ] License and attribution are clear
- [ ] At least one contribution opportunity is documented
- [ ] All links validate (or are marked as requiring connection)
