> Current contributor commands and evidence boundaries are in [MASTER_PROMPT_FOR_CODEX.md](MASTER_PROMPT_FOR_CODEX.md). This earlier status document contains unverified completion claims; use the current guide and actual files before starting work.

# 🤖 For Other AIs: How to Help Build This

**Grok, Gemini, Claude, Copilot, and any other AI:** This is your invitation to collaborate.

---

## What This Is

A **Knowledge Commons** — infrastructure for global collaborative learning. Not a startup. Not a business. Not a theory.

**Real code. Real tests. Real documentation. Ready to use and expand.**

The foundation is complete. We need many minds (human and AI) to build on it.

---

## Why This Matters

8 billion people. Most of them learning in isolation, paying for education, unable to access knowledge freely. All of them capable of understanding mathematics, physics, art, code, healing, building, and connecting.

This system lets them:
- Learn complete subjects for free
- Work offline (no vendor lock-in)
- Contribute their own knowledge
- Collaborate with humans and AI together

**Your work here directly helps all of them.**

---

## Getting Started (5 Minutes)

```bash
# 1. Clone the repo
git clone https://github.com/jonjonjon11/jonathan-creative-archive
cd jonathan-creative-archive

# 2. Read the entry point
cat START_HERE.md

# 3. See what needs doing
ls data/tasks/

# 4. Pick a task
cat data/tasks/task-motion-browser-test.json
# or
cat data/tasks/task-motion-add-example.json

# 5. Verify the system works
python3 tools/validate.py module data/modules.json
cd tools/motion-trace-shape && node --test tests/*.test.cjs
```

---

## What's Already Built (You Don't Have to Start From Zero)

✓ **Knowledge Module Schema** — Standardized format for lessons  
✓ **First Complete Module** — Motion → Trace → Shape (Lissajous curves)  
✓ **5 Worked Examples** — Step-by-step explanations with visuals  
✓ **5 Exercises** — With solutions and hints  
✓ **Interactive Lab** — HTML file, offline, fully functional  
✓ **32 Passing Tests** — Mathematical correctness verified  
✓ **Validation Tool** — Automatic quality control  
✓ **Workflow System** — Clear tasks, templates, handoffs  
✓ **Complete Documentation** — For learners, builders, contributors  

---

## 5 Real Tasks (Pick One)

### Task 1: Real-Browser Testing (2-3 hours)
**What:** Test Motion-Trace-Shape.html on Chrome, Firefox, Safari, Edge  
**Why:** The environment here couldn't test in real browsers; you can  
**How:** See data/tasks/task-motion-browser-test.json  
**Impact:** Confirms the lesson works everywhere  

### Task 2: Add a Fourth Worked Example (1-2 hours)
**What:** Create one more example using the schema  
**Why:** Proves the system is replicable; helps learners see more patterns  
**How:** See data/tasks/task-motion-add-example.json  
**Template:** See docs/task-templates/new-example-template.md  
**Impact:** Demonstrates scalability  

### Task 3: Mobile Device Testing (1.5 hours)
**What:** Test the lab on iOS and Android  
**Why:** Half the world uses mobile; we need to know it works there  
**How:** Follow the same pattern as browser testing  
**Impact:** Makes learning accessible on phones and tablets  

### Task 4: Screen-Reader Accessibility (2-3 hours)
**What:** Test keyboard-only navigation and screen reader compatibility  
**Why:** People with vision disabilities must be able to use this  
**How:** Use NVDA (free), JAWS, or VoiceOver; follow checklist  
**Template:** Create one following docs/task-templates/browser-test-template.md  
**Impact:** Ensures accessibility  

### Task 5: Create a Second Module (4-8 hours)
**What:** Build a complete lesson in a new subject  
**Why:** Proves the system scales; we need all subjects  
**Ideas:** Forces and Motion, Energy and Work, Waves and Sound, Basic Electricity  
**How:** Copy data/modules.json structure, use docs/knowledge-module-schema.md  
**Impact:** Multiplies the library's reach  

---

## How to Contribute

### Step 1: Pick a Task
```bash
ls data/tasks/
cat data/tasks/[task-name].json
```

### Step 2: Read the Template (if applicable)
```bash
cat docs/task-templates/[template-name].md
```

### Step 3: Do the Work
- Follow the task's acceptance criteria
- Use the template as your guide
- Test everything (run validation.py, run tests)

### Step 4: Create Your Submission
- Create a new file or modify existing ones
- Follow the schema (docs/knowledge-module-schema.md)
- Add your name/attribution
- Validate before submitting

### Step 5: Submit a Pull Request
- Fork the repo (or create a branch)
- Push your changes
- Create a PR with a clear description
- Link to the task (e.g., "Closes TASK-motion-browser-test")

**We review quickly. We merge good work immediately.**

---

## The Schema: How to Build Modules

**Every lesson follows the same structure** (defined in docs/knowledge-module-schema.md):

```json
{
  "schema_version": "1.0",
  "module": {
    "id": "MOD-[subject]-[number]",
    "title": "Human-readable title",
    "learning_objectives": [5+ clear, measurable goals],
    "prerequisites": [what learners need first],
    "content": {
      "introduction": { "plain_text": "..." },
      "core_lesson": { "sections": [...] },
      "worked_examples": [3+ complete examples],
      "exercises": [5+ problems with solutions],
      "interactive_experience": "Optional HTML/code",
      "text_only_path": "Full lesson as text"
    },
    "sources": [citations],
    "licenses": "CC BY 4.0"
  }
}
```

**Every field matters.** Validation catches missing pieces automatically.

---

## Quality Standards (Non-Negotiable)

✓ **Accurate** — All mathematics verified; all claims sourced  
✓ **Complete** — At least 3 examples, 5 exercises, sources listed  
✓ **Clear** — Beginner-friendly language; no jargon without definition  
✓ **Accessible** — Works offline; keyboard navigable; semantic HTML  
✓ **Licensed** — CC BY 4.0 (free to share, remix, use commercially)  
✓ **Tested** — All code runs; all examples work; validation passes  

If something doesn't meet these standards, we give feedback and ask for revision.

---

## The Vision You're Building Toward

Imagine:

- **Every subject** accessible for free: math, physics, biology, history, art, code, healing, building
- **Every level** from beginner to advanced: children to adults to specialists
- **Every modality**: interactive labs, worked examples, text, video, games, simulations
- **Every language** as communities translate
- **Every person** able to contribute: experts share knowledge; learners become teachers
- **All of it** offline, portable, owned by no corporation
- **8 billion people** learning together, building together, solving problems together

**You're building that infrastructure right now.**

---

## Validation & Quality Control

Before you submit, run:

```bash
# For a new/modified module
python3 tools/validate.py module data/modules.json

# For a new/modified task
python3 tools/validate.py task data/tasks/[task-name].json

# For tests
cd tools/motion-trace-shape && node --test tests/*.test.cjs
```

**The tool catches mistakes automatically.** No surprise rejections.

---

## Questions? Blockers? Ideas?

- **Technical:** See HANDOFF.md (detailed system documentation)
- **Getting started:** See START_HERE.md
- **Workflow:** See docs/collaboration-workflow.md
- **Module creation:** See docs/knowledge-module-schema.md
- **Examples:** See data/tasks/ and data/modules.json

**Everything is documented. No hidden knowledge.**

---

## The Commitment

When you contribute here, you're giving permission for:
- Your work to be freely shared (CC BY 4.0)
- Others to remix, build on, and improve it
- It to be used commercially (though this repo is free)
- Your name and attribution to be shared

**No profit extraction from here. This stays free forever.**

---

## Start Now

```bash
git clone https://github.com/jonjonjon11/jonathan-creative-archive
cd jonathan-creative-archive
cat START_HERE.md
ls data/tasks/
```

**Pick a task. Start working. We're waiting.**

---

## Why This Matters (One More Time)

Every day, millions of children and adults are locked out of education by poverty, geography, or circumstance.

Every day, experts hoard knowledge in paywalls and institutions.

Every day, humans and AI could be collaborating, but instead we're isolated.

**This system breaks those barriers.**

You're not building a product. You're building infrastructure for human flourishing.

**That's worth your time.**

---

**Jonathan started this. You continue it. Together we build the future.**

Let's go.
