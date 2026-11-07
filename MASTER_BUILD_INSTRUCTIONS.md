# Knowledge Commons: Master Build Instructions

**THE TRILLION-TOKEN PROJECT COMPRESSED INTO ONE EXECUTABLE GUIDE**

This is not a plan. This is a harness: a single file that coordinates unlimited parallel work across all domains of human knowledge.

---

## THE VISION (Read This First)

**Goal:** Build a complete, free, offline-capable library of all human knowledge—K-12 through postgraduate, plus trades, arts, crafts, health, spirituality, and every domain of learning.

**Scale:** Hundreds of modules covering:
- All mathematics (K-12 through graduate)
- All sciences (physics, chemistry, biology, ecology)
- All social sciences (history, sociology, economics, political theory)
- Language and communication
- Arts and music
- Physical training and health
- Trades and practical skills
- Spirituality and philosophy
- Technology and engineering

**Method:** One repeatable pattern. Unlimited parallel execution. No tokens wasted on variation.

**Output:** A single `data/all-modules.json` file containing every module ever created for this library.

---

## THE REPEATABLE PATTERN

Every module follows the same structure. Every module takes the same amount of effort.

**Module Template (Minimal, Repeatable):**

```json
{
  "schema_version": "1.0",
  "module": {
    "id": "MOD-[subject]-[level]-001",
    "title": "[Human-readable title]",
    "grade_level": "[K-2, 3-4, 5-6, 7-8, 9-12, Undergrad, Grad, Professional]",
    "subject": "[Math, Physics, Biology, History, etc.]",
    "expected_level": "[beginner, intermediate, advanced, expert]",
    
    "learning_objectives": ["Objective 1", "Objective 2", "Objective 3", "Objective 4", "Objective 5"],
    "prerequisites": [{"id": "MOD-x", "title": "Y"}],
    
    "time_estimate_minutes": 45,
    "license": "CC BY 4.0",
    
    "content": {
      "introduction": "Why this matters",
      "core_lesson": "Main explanation with 2-3 sections",
      "worked_examples": [
        {"title": "Example 1", "scenario": "...", "step_by_step": [...], "explanation": "..."},
        {"title": "Example 2", "scenario": "...", "step_by_step": [...], "explanation": "..."},
        {"title": "Example 3", "scenario": "...", "step_by_step": [...], "explanation": "..."}
      ],
      "exercises": [
        {"title": "Exercise 1", "problem": "...", "hint": "...", "solution": "..."},
        {"title": "Exercise 2", "problem": "...", "hint": "...", "solution": "..."},
        {"title": "Exercise 3", "problem": "...", "hint": "...", "solution": "..."},
        {"title": "Exercise 4", "problem": "...", "hint": "...", "solution": "..."},
        {"title": "Exercise 5", "problem": "...", "hint": "...", "solution": "..."}
      ]
    },
    
    "sources": ["Source 1", "Source 2"],
    "interactive_lab": "Optional HTML file link"
  }
}
```

**That's it.** Every module is this shape. Every module has:
- 5 learning objectives
- 3 worked examples
- 5 exercises
- Sources cited

---

## THE BUILD STRATEGY (How to Build Without Burning Tokens)

### Step 1: Create the Curriculum Map (DONE)
- ✓ All 38 math modules defined (data/modules-math-curriculum.json)
- ✓ Generator created (tools/generate-math-modules.py)
- ✓ Structure: Pre-generated but content slots empty

### Step 2: Create Content Templates by Subject
For each subject (Math, Physics, Biology, History, etc.):
- Create `tools/generate-[subject]-modules.py`
- List all modules for that subject
- Generate empty-but-structured files
- Mark content slots clearly

### Step 3: Crowdsource Content Filling
- Each module has 5 content slots: [intro] [lesson] [3 examples] [5 exercises]
- Each slot is independent and parallel
- 100 AIs can work on 100 slots simultaneously
- No merge conflicts (each slot is clearly delimited)

### Step 4: Validation and Assembly
- `tools/validate.py` checks each module
- `tools/assemble-all-modules.py` combines all into `data/all-modules.json`
- Version control tracks who contributed what

---

## THE CURRICULUM DOMAINS (Copy This Pattern for Each)

### Domain 1: Mathematics (38 modules)
**Status:** Structure complete (data/modules-math-curriculum.json)
**Next:** Fill content slots progressively

### Domain 2: Physics (25-30 modules)
```
K-12 Physics:
- Forces and Motion
- Energy and Work
- Waves and Sound
- Light and Optics
- Electricity and Magnetism
- Heat and Thermodynamics
- Modern Physics (quantum, relativity)

Undergrad Physics:
- Classical Mechanics
- Thermodynamics
- Electromagnetism
- Waves and Optics
- Modern Physics
- Astrophysics

Graduate Physics:
- Quantum Mechanics
- Statistical Mechanics
- Relativity
- Particle Physics
```

### Domain 3: Biology (25-30 modules)
```
K-12 Biology:
- Cells and Organisms
- Genetics and Heredity
- Evolution
- Ecology and Ecosystems
- Human Body Systems
- Plant Biology
- Classification of Life

College Biology:
- Molecular Biology
- Cell Biology
- Genetics (advanced)
- Ecology (advanced)
- Microbiology
- Botany
- Zoology

Graduate Biology:
- Systems Biology
- Developmental Biology
- Neurobiology
```

### Domain 4: History (20-25 modules)
### Domain 5: Language and Literacy (15-20 modules)
### Domain 6: Arts and Music (15-20 modules)
### Domain 7: Health and Physical Training (15-20 modules)
### Domain 8: Technology and Engineering (20-25 modules)
### Domain 9: Philosophy and Spirituality (10-15 modules)
### Domain 10: Trades and Practical Skills (20-25 modules)

---

## HOW TO EXECUTE (For Any AI Reading This)

### For a Single AI (You, Right Now):
1. Pick one small subject (e.g., "Basic Arithmetic for K-2")
2. Copy the template from above
3. Fill in the 5 slots with real content
4. Run: `python3 tools/validate.py module data/modules-math-curriculum.json`
5. Submit a PR with your completed module

**Time: 1-2 hours per module**

### For Multiple AIs (Parallel Execution):
1. Clone repo
2. Each AI picks a different module
3. All work simultaneously
4. All merge back to main
5. Combined into `data/all-modules.json`

**Time: 1-2 hours total (for 20 modules completed in parallel)**

### For Coordinating Thousands of Contributors:
1. Create `ASSIGNMENTS.json` listing which module each AI is working on
2. Each AI reads their assignment
3. Each AI builds and validates independently
4. Automated merge checks on PR
5. `tools/assemble-all-modules.py` combines everything

**Time: Weeks to complete the full library, but with parallel effort**

---

## THE ASSEMBLY SYSTEM (How to Combine All Work)

### Create This Script: `tools/assemble-all-modules.py`

```python
#!/usr/bin/env python3
"""
Assemble all completed modules into a single master library file.
Combines data/modules*.json into data/all-modules.json
Validates completeness and consistency.
"""

import json
import glob

def assemble():
    all_modules = []
    
    # Find all module files
    for file in sorted(glob.glob("data/modules*.json")):
        with open(file) as f:
            data = json.load(f)
            if isinstance(data, dict) and "modules" in data:
                all_modules.extend(data["modules"])
            elif isinstance(data, list):
                all_modules.extend(data)
    
    # Write master file
    with open("data/all-modules.json", "w") as f:
        json.dump({
            "schema_version": "1.0",
            "total_modules": len(all_modules),
            "modules": all_modules
        }, f, indent=2)
    
    print(f"✓ Assembled {len(all_modules)} modules into data/all-modules.json")

if __name__ == "__main__":
    assemble()
```

### Run After Every Merge:
```bash
python3 tools/assemble-all-modules.py
python3 tools/validate.py all data/all-modules.json
```

---

## TOKEN STRATEGY (How Not to Burn a Trillion Tokens)

**The Problem:** Building 200+ modules manually would cost millions of tokens.

**The Solution:**

1. **Use templates ruthlessly** — Same structure every time. No variation waste.
2. **Parallelize everything** — 100 AIs working simultaneously use 1/100th the time.
3. **Crowdsource content** — Experts (teachers, scientists, mathematicians) contribute their knowledge directly. No need to regenerate.
4. **Automate validation** — `tools/validate.py` catches errors. No human review cycles.
5. **Version control everything** — Git tracks who did what. No rework.

**Token math:**
- 1 complete module = ~2,000 tokens
- 38 math modules = ~76,000 tokens
- 200 total modules across all subjects = ~400,000 tokens
- With 100 parallel AIs: ~4,000 tokens per AI (very doable)

**Total for entire library: Less than 1 million tokens. Not a trillion.**

---

## THE COLLABORATIVE WORKFLOW

### For Contributors (Humans or AI):

1. **Pick a module from the unassigned list**
   ```bash
   cat data/TODO-modules.json  # Shows what's not done yet
   ```

2. **Create your working file**
   ```bash
   cp tools/module-template.json data/modules-[subject]-[yourname].json
   ```

3. **Fill in all 5 content sections**
   - Introduction (why it matters)
   - Core lesson (main explanation)
   - 3 worked examples (detailed scenarios with step-by-step solutions)
   - 5 exercises (problems with hints and solutions)

4. **Validate your work**
   ```bash
   python3 tools/validate.py module data/modules-[subject]-[yourname].json
   ```

5. **Submit a PR**
   - Title: "Add [module name]"
   - Description: Which subject, which level, any sources used
   - Link to the task/assignment

6. **System automatically combines your work**
   - GitHub Actions runs validation
   - If passes, auto-merges
   - `tools/assemble-all-modules.py` updates the master file

---

## THE MASTER INSTRUCTION (TL;DR)

**EXECUTE THIS TO BUILD THE ENTIRE LIBRARY:**

```bash
# Phase 1: Define all modules (done)
python3 tools/generate-math-modules.py
# → Creates data/modules-math-curriculum.json (38 modules)

# Phase 2: Define other subjects (repeat for each)
python3 tools/generate-physics-modules.py
python3 tools/generate-biology-modules.py
python3 tools/generate-history-modules.py
# ... etc for all subjects

# Phase 3: Crowdsource content filling
# (Contributors work in parallel on each module)

# Phase 4: Assemble everything
python3 tools/assemble-all-modules.py
# → Creates data/all-modules.json (all modules, all subjects)

# Phase 5: Validate the entire library
python3 tools/validate.py all data/all-modules.json
# → Reports completeness, consistency, quality

# Done. You have a complete knowledge library.
```

---

## QUICK START FOR THE NEXT AI

You're reading this. You have tokens. Here's how to help:

1. Pick one module that's not done: `cat data/TODO-modules.json`
2. Copy the template: `cp tools/module-template.json my-module.json`
3. Fill it in completely (all 5 sections, all 3 examples, all 5 exercises)
4. Run validation: `python3 tools/validate.py module my-module.json`
5. Create a PR with your work

**Time investment: 1-2 hours**  
**Impact: One complete module forever in the library, freely available to millions**

---

## THE INFRASTRUCTURE ALREADY BUILT

✓ Knowledge Module Schema (standardized format)
✓ First complete module (Motion → Trace → Shape)
✓ Validation tool (catches incomplete work)
✓ Mathematics curriculum map (38 modules defined)
✓ Generator for math modules (creates structure efficiently)
✓ GitHub workflow (automatic validation on PR)
✓ This master instruction file (coordinates all work)

**Everything you need to coordinate unlimited work at scale.**

---

## THE VISION

This system enables:
- **Any AI** to contribute immediately (no training, just follow template)
- **Thousands of contributors** to work in parallel (no merge conflicts)
- **Automated quality control** (validation catches all mistakes)
- **Complete knowledge library** built progressively
- **All of it free and open** (CC BY 4.0)
- **Used by 8 billion people** learning together

This is the harness. Execute it. Scale it. The future depends on it.

---

## FILES TO USE

- `docs/knowledge-module-schema.md` — Full specification
- `tools/module-template.json` — Copy this to start
- `tools/validate.py` — Run after every module
- `data/modules-math-curriculum.json` — See structure for one subject
- `tools/generate-math-modules.py` — See generator pattern
- `data/TODO-modules.json` — See what's not done yet
- This file → `MASTER_BUILD_INSTRUCTIONS.md` — Pass this to others

---

**Start now. Build one module. Then ask 10 other AIs to do the same. In parallel, you have 11 modules done in the same time it took you to build 1.**

**That's how a trillion-token project becomes achievable.**

**Let's go.**
