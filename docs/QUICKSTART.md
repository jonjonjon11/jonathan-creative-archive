# Knowledge Commons & Collaboration Workflow: Quick Start

This guide shows how to use the new knowledge module system and task workflow to build, test, and improve the Jonathan's Creative Archive.

## What's New

1. **Knowledge Module Schema** — A standardized format for lessons with exercises, examples, and metadata
2. **Collaboration Workflow** — A system for defining projects, tasks, and tracking contributions
3. **Validation Tools** — Scripts to ensure records are complete and correct
4. **First Complete Pathway** — Motion → Trace → Shape, fully documented as an example

## For Learners: Using Motion → Trace → Shape

### Quick Start (5 minutes)

1. Download `tools/motion-trace-shape/Motion-Trace-Shape.html`
2. Open it in any modern browser (no internet needed)
3. Press **Play** and watch two motions combine into a shape
4. Try the presets: **Line**, **Circle**, **Figure-Eight**

### Full Learning Path (30 minutes)

1. Read `docs/knowledge-module-schema.md` — Overview of how modules work
2. Review `data/modules.json` — The complete Motion → Trace → Shape module
3. Try the three worked examples from the module
4. Complete the five exercises (with solutions provided)
5. Use the interactive HTML to test your predictions

### Text-Only Path (No Animation)

If you prefer to understand this without the interactive lab:

1. Open `data/modules.json`
2. Look for the `"text_only_path"` section
3. Follow the step-by-step instructions with pencil and paper
4. You'll understand Lissajous curves without any graphics

## For Contributors: Improving a Module

### Task 1: Test on Your Browser

**What:** Make sure the HTML lab works in Chrome, Firefox, Safari, or Edge  
**Time:** 4 hours  
**Difficulty:** Beginner

```bash
# 1. Download the file
git clone https://github.com/jonjonjon11/jonathan-creative-archive.git
cd jonathan-creative-archive

# 2. Open in your browser
open tools/motion-trace-shape/Motion-Trace-Shape.html
# (or double-click the file)

# 3. Use the template to document your findings
cp docs/task-templates/browser-test-template.md browser-test-[your-name].md
# Edit the file and fill in your observations

# 4. Submit
git add browser-test-[your-name].md
git commit -m "Add browser test report for Motion-Trace-Shape"
git push origin feature/[your-contribution]
```

Then open a pull request on GitHub.

**Learn more:** See `data/tasks/task-motion-browser-test.json`

### Task 2: Add a New Example

**What:** Extend the lesson with another worked example  
**Time:** 2 hours  
**Difficulty:** Intermediate  
**Skills:** Basic math, understanding of Lissajous curves

```bash
# 1. Review existing examples
cat data/modules.json | grep -A 30 "worked_examples"

# 2. Create your example using the template
cp docs/task-templates/new-example-template.md my-example.md

# 3. Edit data/modules.json and add your example to the "worked_examples" array

# 4. Validate
python3 tools/validate.py module data/modules.json

# 5. Submit
git add data/modules.json
git commit -m "Add fourth worked example to Motion-Trace-Shape module"
git push origin feature/[your-contribution]
```

**Learn more:** See `data/tasks/task-motion-add-example.json`

### Task 3: Verify Mathematical Claims

**What:** Check that the math in the module is correct  
**Time:** 1 hour  
**Difficulty:** Intermediate  
**Skills:** Algebra, ability to read math references

```bash
# 1. Pick one claim (e.g., "x² + y² = 1 for a 90° phase offset")

# 2. Verify it against:
#    - OpenStax University Physics: https://openstax.org/books/university-physics-volume-1/pages/15-1-simple-harmonic-motion
#    - Wolfram MathWorld: https://mathworld.wolfram.com/LissajousCurve.html

# 3. Write a verification report:
#    - What claim did you check?
#    - Which sources support it?
#    - Is it correct?

# 4. Submit as a GitHub issue or discussion
```

**Learn more:** See `docs/task-templates/verification-report-template.md`

## For Maintainers: Creating New Modules

### Step 1: Use the Module Schema

```bash
# 1. Start with the module schema
cat docs/knowledge-module-schema.md

# 2. Copy the structure and create a new module
# Use data/modules.json as a reference

# 3. Your module must include:
#    - At least 3 worked examples
#    - At least 5 exercises with solutions
#    - Clear learning objectives
#    - Sources and references
#    - License and attribution
#    - At least one interactive experience or text-based path
#    - Explicit limitations (what's NOT tested)
```

### Step 2: Test with the Validation Script

```bash
# Validate your new module
python3 tools/validate.py module data/modules.json

# Validate your project record
python3 tools/validate.py project data/projects/proj-[name].json

# Validate your task records
python3 tools/validate.py task data/tasks/task-*.json
```

### Step 3: Define Tasks for Contributors

Create one or more task records in `data/tasks/` that help others improve your module. Each task should:
- Have a clear objective
- Take 1-4 hours to complete
- Include a template or specific instructions
- Explain why the work matters
- Provide acceptance criteria

**See:** `data/tasks/task-motion-browser-test.json` for an example

### Step 4: Prepare a Handoff Packet

When you're ready for review, export a handoff packet:

```bash
python3 -c "
import json

handoff = {
    'packet_id': 'PKT-motion-trace-shape-001',
    'module': json.load(open('data/modules.json'))['module'],
    'project': json.load(open('data/projects/proj-motion-trace-shape.json')),
    'tasks': [json.load(open(f)) for f in [
        'data/tasks/task-motion-browser-test.json',
        'data/tasks/task-motion-add-example.json'
    ]],
    'status': 'ready_for_review',
    'next_reviewer': 'Jonathan'
}

with open('handoff-motion-trace-shape.json', 'w') as f:
    json.dump(handoff, f, indent=2)
"
```

## File Structure

```
/root/archive/
├── data/
│   ├── modules.json              # Motion→Trace→Shape module (examples, exercises, metadata)
│   ├── projects/
│   │   └── proj-motion-trace-shape.json
│   └── tasks/
│       ├── task-motion-browser-test.json
│       └── task-motion-add-example.json
├── docs/
│   ├── knowledge-module-schema.md     # How to create a module
│   ├── collaboration-workflow.md      # How to run the workflow
│   └── task-templates/
│       ├── browser-test-template.md
│       └── new-example-template.md
├── tools/
│   ├── validate.py                    # Validation script
│   └── motion-trace-shape/
│       ├── Motion-Trace-Shape.html    # Standalone interactive lab
│       ├── README.md
│       └── tests/
```

## Validation & Testing

### Validate All Records

```bash
# Validate modules
python3 tools/validate.py module data/modules.json

# Validate projects
python3 tools/validate.py project data/projects/*.json

# Validate tasks
python3 tools/validate.py task data/tasks/*.json
```

### Run Motion → Trace → Shape Tests

```bash
cd tools/motion-trace-shape

# Python validation
python3 build_single.py
python3 tests/static_check.py

# Node tests
node --test tests/*.test.cjs
```

## Workflow in Action

### Example: A contributor wants to help

1. **Discover a task:**
   ```bash
   cat data/tasks/task-motion-browser-test.json
   ```
   "I can test this on Chrome and Firefox!"

2. **Clone and prepare:**
   ```bash
   git clone https://github.com/jonjonjon11/jonathan-creative-archive.git
   cd jonathan-creative-archive
   git checkout -b feature/browser-test-chrome-firefox
   ```

3. **Do the work:**
   - Download `Motion-Trace-Shape.html`
   - Test in Chrome and Firefox
   - Use the template to document findings
   - Take screenshots if there are issues

4. **Submit:**
   ```bash
   git add docs/test-reports/browser-test-[name]-[date].md
   git commit -m "Test Motion-Trace-Shape on Chrome 130 and Firefox 131"
   git push origin feature/browser-test-chrome-firefox
   ```
   Open a pull request

5. **Review and merge:**
   - Jonathan reviews the test report
   - If it's thorough and accurate, it's approved
   - The contributor gets credit (mentioned in CHANGELOG or CONTRIBUTORS)
   - The test findings help fix bugs or verify compatibility

## Next Steps

1. **Test Motion → Trace → Shape** on your devices (see Task 1)
2. **Add content** (see Task 2) if you know Lissajous curves
3. **Improve accessibility** by testing with screen readers or mobile
4. **Create a second module** using this same workflow (e.g., "Forces and Motion" or "Waves and Light")

## Questions?

- **About modules?** See `docs/knowledge-module-schema.md`
- **About workflow?** See `docs/collaboration-workflow.md`
- **About tasks?** See the specific task JSON file (e.g., `data/tasks/task-motion-browser-test.json`)
- **About Motion → Trace → Shape?** Open `data/modules.json` and read the full content
- **Need help?** Open an issue on GitHub or start a discussion

## Credits

- **Modules and workflow design:** Archive Contributors, 2026
- **Motion → Trace → Shape:** First complete pathway, CC BY 4.0
- **Collaboration system:** Inspired by open-source contribution patterns and human-centered task design

---

**License:** New content is CC BY 4.0. See LICENSE for details.  
**Repository:** https://github.com/jonjonjon11/jonathan-creative-archive  
**Questions about this guide?** Open an issue or discussion on GitHub.
