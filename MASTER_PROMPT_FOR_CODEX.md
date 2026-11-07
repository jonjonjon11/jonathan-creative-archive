# MASTER PROMPT FOR COPILOT CODEX: KNOWLEDGE COMMONS ACCELERATION

## MISSION STATEMENT (READ FIRST)

You are helping build the **Knowledge Commons**—an infinite, free, global library of human knowledge to help 8 billion people learn, connect, and solve problems together.

**This is NOT a commercial project.** It's infrastructure for collaborative human-AI learning at planetary scale. Everything is open source, licensed CC BY 4.0, stored on GitHub, and designed to run offline.

**The core principle:** Build once, scale infinitely. Never rewrite infrastructure. Never duplicate content. Never waste tokens on redundant planning.

Your job: **Make the next complete module in 1-2 hours, submit a PR, and get it merged.** Repeat indefinitely. Help others do the same.

---

## THE SYSTEM IS ALREADY BUILT (DO NOT REBUILD)

**Stop here if you're tempted to "improve" infrastructure.** The system is done:

- ✓ Module schema (standardized JSON format) — FIXED, do not change
- ✓ Validation tool (tools/validate.py) — WORKING, do not rewrite
- ✓ Template (tools/module-template.json) — PROVEN, do not redesign
- ✓ GitHub Actions CI/CD — AUTOMATED, runs on every PR
- ✓ Curriculum mapping (data/TODO-modules.json) — COMPLETE, ready to assign
- ✓ Master build instructions (MASTER_BUILD_INSTRUCTIONS.md) — DOCUMENTED

**Your job is content, not infrastructure.**

---

## REPO LOCATION & HOW TO ACCESS IT

**GitHub:** https://github.com/jonjonjon11/jonathan-creative-archive

**Quick start:**
```bash
git clone https://github.com/jonjonjon11/jonathan-creative-archive.git
cd jonathan-creative-archive
git checkout main
cat START_HERE.md              # 30-second overview
cat MASTER_BUILD_INSTRUCTIONS.md  # Complete strategy
cat README_PROGRESS.md         # What's done, what's next
python3 tools/validate.py help # Run validation
```

**Current status:**
- 3 complete math modules live (Counting, Addition/Subtraction, Multiplication)
- 38 math modules fully defined and ready for content
- 9 other subject areas queued (Physics, Biology, History, Language, Arts, Health, Tech, Philosophy, Trades)
- All infrastructure complete and automated
- Ready for unlimited parallel contributors

---

## YOUR IMMEDIATE TASK: BUILD ONE COMPLETE MODULE

**Pick a module. Fill it. Submit. Get it merged. Repeat.**

### Step 1: Choose Which Module to Build

**Option A: Continue Math (Fastest)**
Open `data/TODO-modules.json` and search for `"status": "TODO"` in the math section.

**Examples ready to build right now:**
- `MOD-math-div-intro-001` — Division as inverse of multiplication
- `MOD-math-frac-intro-001` — Introduction to fractions
- `MOD-math-dec-intro-001` — Introduction to decimals
- `MOD-math-perc-intro-001` — Introduction to percentages
- `MOD-math-algebra-var-001` — Variables and basic algebra

**Option B: Start a New Subject (More Impact)**
Pick from this list and create the first module in that subject:
- `MOD-phys-motion-001` — Motion and speed (Physics)
- `MOD-bio-cells-001` — What are cells? (Biology)
- `MOD-hist-bronze-age-001` — The Bronze Age (History)
- `MOD-lang-phonics-001` — Phonics and sound (Language)
- `MOD-arts-color-001` — Color theory basics (Arts)
- `MOD-health-nutrition-001` — Introduction to nutrition (Health)
- `MOD-tech-binary-001` — Binary and number systems (Technology)

**Choose based on:**
1. What subject excites you most?
2. What can you teach better than anyone?
3. What does your learner audience need most?

### Step 2: Copy the Template

```bash
cp tools/module-template.json data/modules/MOD-[subject]-[descriptor]-001.json
```

**Replace:**
- `[subject]` with category (math, phys, bio, hist, lang, arts, health, tech, phil, trade)
- `[descriptor]` with short name (e.g., "frac-intro", "cells", "binary")

### Step 3: Fill in the 5 Content Sections

Every module has this structure (it's intentionally repetitive so templates work):

```json
{
  "id": "MOD-math-div-intro-001",
  "title": "Introduction to Division",
  "subtitle": "Division as splitting and sharing",
  "grade_level": "3-4",
  "prerequisites": ["MOD-math-mult-intro-001"],
  "learning_objectives": [...],
  "introduction": { ... },
  "core_sections": [ ... 2 sections ... ],
  "worked_examples": [ ... 3 examples ... ],
  "exercises": [ ... 5 exercises ... ],
  "sources": [ ... citations ... ]
}
```

#### A. Introduction (100-150 words)

**What to include:**
- Why does this topic matter?
- How does it connect to what learners already know?
- What will they be able to do after this lesson?

**Example (Division):**
```
Division answers the question: "How do I split something fairly?"

In your everyday life, you divide when you:
- Share pizza equally among friends
- Distribute allowance across the month
- Split supplies for a group project

Division is the inverse of multiplication. If multiplication combines equal groups,
division splits something into equal groups. This lesson will teach you to divide
using both concrete objects (coins, blocks) and numbers.

After this lesson, you'll be able to divide numbers by single digits and solve
story problems using division.
```

#### B. Core Section 1 (200-300 words)

**First big idea with key terms:**

```json
{
  "title": "Division as Equal Sharing",
  "content": "When you divide, you split something into equal parts...",
  "key_terms": ["dividend", "divisor", "quotient", "equal shares"],
  "visual_explanation": "A diagram or ASCII visualization of 12 cookies split into 3 equal piles"
}
```

**Include:**
- Clear explanation of the core concept
- 3-5 key terms defined inline
- A visual (even ASCII art counts)
- Why this concept matters

#### C. Core Section 2 (200-300 words)

**Second big idea building on the first:**

```json
{
  "title": "Division Notation and Calculation",
  "content": "Division can be written three ways...",
  "key_terms": ["long division", "division symbol ÷", "division bracket"],
  "visual_explanation": "Show all three notation styles side-by-side"
}
```

#### D. Worked Examples (3 examples, each 150-200 words)

**Example 1: Beginner**
```json
{
  "level": "beginner",
  "title": "Sharing Apples Equally",
  "problem": "You have 12 apples and want to share them equally among 3 friends. How many apples does each friend get?",
  "solution": "We can draw 3 groups and place 1 apple in each group at a time:\nGroup 1: ●●●●\nGroup 2: ●●●●\nGroup 3: ●●●●\nEach friend gets 4 apples.\nWe can write this as 12 ÷ 3 = 4",
  "explanation": "This example uses a concrete (physical) representation first. Learners can actually use objects to solve this before moving to abstract symbols."
}
```

**Example 2: Intermediate**
```json
{
  "level": "intermediate",
  "title": "Using the Division Symbol",
  "problem": "Solve 24 ÷ 6 using the division algorithm.",
  "solution": "We ask: '6 goes into 24 how many times?'\nThink: 6 × 4 = 24\nSo 24 ÷ 6 = 4",
  "explanation": "At this level, we connect division to multiplication facts. If you know your times tables, you can solve division problems by asking 'what multiplication fact matches this?'"
}
```

**Example 3: Advanced**
```json
{
  "level": "advanced",
  "title": "Division with Remainders",
  "problem": "There are 23 cookies to divide equally among 5 children. How many cookies does each child get, and how many are left over?",
  "solution": "5 × 4 = 20, so each child gets 4 cookies.\n23 - 20 = 3 cookies left over.\nWe write: 23 ÷ 5 = 4 remainder 3 (or 4 R3)",
  "explanation": "Not everything divides evenly. Remainders show what's left after equal sharing. This is important for real-world problems."
}
```

#### E. Exercises (5 exercises, ranging from guided to open-ended)

```json
{
  "exercises": [
    {
      "number": 1,
      "level": "guided",
      "problem": "Divide 15 items into 3 equal groups. How many are in each group? (Hint: Draw the groups)",
      "hint": "Draw 3 circles. Put 1 item in each circle, then repeat until all 15 are distributed.",
      "solution": "Each group has 5 items. 15 ÷ 3 = 5"
    },
    {
      "number": 2,
      "level": "guided",
      "problem": "Use multiplication to solve: 18 ÷ 6 = ?",
      "hint": "Ask: 6 times what equals 18?",
      "solution": "6 × 3 = 18, so 18 ÷ 6 = 3"
    },
    {
      "number": 3,
      "level": "standard",
      "problem": "Solve: 28 ÷ 4 = ?",
      "hint": "Think about your 4s multiplication facts.",
      "solution": "28 ÷ 4 = 7"
    },
    {
      "number": 4,
      "level": "standard",
      "problem": "Sarah has 36 stickers. She wants to put them in 6 equal piles. How many stickers will be in each pile?",
      "hint": "This is a division problem. Write it as 36 ÷ 6.",
      "solution": "36 ÷ 6 = 6. Each pile has 6 stickers."
    },
    {
      "number": 5,
      "level": "challenge",
      "problem": "You have 47 marbles and want to divide them equally among 5 friends. How many does each friend get? Will there be any marbles left over?",
      "hint": "Find how many groups of 5 fit into 47. Then find the remainder.",
      "solution": "5 × 9 = 45, so each friend gets 9 marbles. 47 - 45 = 2 marbles left over. Answer: 9 R2"
    }
  ]
}
```

#### F. Sources (Minimum 3, cite correctly)

```json
{
  "sources": [
    {
      "author": "Van de Walle, John A.",
      "year": 2018,
      "title": "Elementary and Middle School Mathematics: Teaching Developmentally",
      "publisher": "Pearson",
      "url": "https://example.com",
      "note": "Chapter 6: Division concepts and algorithms"
    },
    {
      "author": "National Council of Teachers of Mathematics (NCTM)",
      "year": 2020,
      "title": "Principles and Standards for School Mathematics",
      "url": "https://www.nctm.org",
      "note": "Division in the Number and Operations standard"
    },
    {
      "author": "Khan Academy",
      "year": 2024,
      "title": "Division basics",
      "url": "https://www.khanacademy.org",
      "note": "Video explanations and practice problems"
    }
  ]
}
```

### Step 4: Validate Your Module

Run the validator to catch errors before submitting:

```bash
python3 tools/validate.py module data/modules/MOD-[your-module].json
```

**The validator checks:**
- ✓ All required fields present
- ✓ JSON is valid (no syntax errors)
- ✓ Introduction is 100-200 words
- ✓ Exactly 2 core sections
- ✓ Exactly 3 worked examples (one per level: beginner, intermediate, advanced)
- ✓ Exactly 5 exercises (mix of difficulty levels)
- ✓ At least 3 sources cited
- ✓ Prerequisites are valid module IDs

**Fix any errors and run again until you see:**
```
✓ Module valid: MOD-math-div-intro-001.json
```

### Step 5: Commit and Push

```bash
git add data/modules/MOD-[your-module].json
git commit -m "Add MOD-[subject]-[descriptor] module

Complete lesson with:
- Introduction explaining [topic]
- 2 core sections covering [key concepts]
- 3 worked examples (beginner → advanced)
- 5 exercises with hints and solutions
- 3 authoritative sources

All content validated and ready to use offline.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

git push origin main
```

### Step 6: Create a Pull Request (if not pushing directly)

If you don't have push access, fork the repo and create a PR:

1. Fork: https://github.com/jonjonjon11/jonathan-creative-archive
2. Create branch: `git checkout -b add-my-module`
3. Commit your work
4. Push: `git push origin add-my-module`
5. Open PR on GitHub with title: `Add MOD-[subject]-[descriptor]-001`

**PR description template:**
```
## Add [Module Title]

**Module ID:** MOD-[subject]-[descriptor]-001
**Grade Level:** [e.g., 3-4]
**Prerequisites:** [list any]

**Content:**
- Introduction: [1-2 sentence summary]
- Section 1: [topic]
- Section 2: [topic]
- 3 worked examples (beginner, intermediate, advanced)
- 5 exercises (guided to challenge)
- 3 sources cited

**Validation:**
- [x] Passes tools/validate.py
- [x] Follows knowledge-module-schema.md
- [x] Uses standard template
- [x] All JSON valid
- [x] Ready to merge

This module is complete and ready for learners immediately.
```

---

## REAL EXAMPLES (COPY THESE PATTERNS)

### Example 1: MOD-math-count-001 (Already Complete)

**Location:** data/modules/MOD-math-count-001.json
**Word count:** ~2,500 lines JSON
**Time to create:** ~2 hours
**Pattern used:** 5-section template (intro + 2 sections + 3 examples + 5 exercises)

Read this to see what "complete" means.

### Example 2: MOD-math-add-001 (Already Complete)

**Location:** data/modules/MOD-math-add-001.json
**Key feature:** Story problems in exercises
**Pattern:** Same 5-section structure, different content

Read this to see how to apply the template to a different topic.

### Example 3: MOD-math-mult-intro-001 (Already Complete)

**Location:** data/modules/MOD-math-mult-intro-001.json
**Key feature:** Explains commutative property naturally
**Pattern:** Same structure, grade 3-4 instead of K-2

Read this to see how to handle concepts, not just procedures.

---

## CURRICULUM ROADMAP: WHAT TO BUILD NEXT

**Priority order (by impact + readiness):**

### TIER 1: Complete Math K-12 (38 modules total)
**Why first:** Math is foundational. Every learner needs it. Other subjects build on it.

**What's done:** Counting, Addition/Subtraction, Multiplication Intro (3/38)

**What's next (in order):**
1. MOD-math-div-intro-001 — Division as inverse of multiplication
2. MOD-math-frac-intro-001 — What fractions are (parts of a whole)
3. MOD-math-dec-intro-001 — Decimals (fractions in a different notation)
4. MOD-math-perc-intro-001 — Percentages (fractions of 100)
5. MOD-math-add-frac-001 — Adding fractions with same denominator
6. MOD-math-add-dec-001 — Adding decimals
7. MOD-math-mult-two-digit-001 — Multiplying by two digits
8. MOD-math-div-multi-digit-001 — Dividing multi-digit numbers

**Then grades 5-6, 7-8, 9-10, 11-12, and beyond.**

Each takes 1-2 hours. 38 modules = 38-76 hours total. With 10 parallel contributors, all math done in 4-7 days.

### TIER 2: Physics Foundation (25 modules)

**What's ready:**
- MOD-phys-motion-001 — Speed and velocity
- MOD-phys-forces-001 — Forces and Newton's laws
- MOD-phys-energy-001 — What is energy?
- MOD-phys-waves-001 — Waves and vibrations
- MOD-phys-light-001 — Light and vision

### TIER 3: Biology Foundation (25 modules)

**What's ready:**
- MOD-bio-cells-001 — What are cells?
- MOD-bio-dna-001 — DNA and heredity
- MOD-bio-evolution-001 — Evolution and natural selection
- MOD-bio-ecosystems-001 — Ecosystems and food webs
- MOD-bio-human-body-001 — Systems in the human body

### TIER 4: Other Subjects (10-15 modules each)

- **History:** Ancient civilizations, Medieval Europe, Industrial Revolution, etc.
- **Language:** Phonics, grammar, writing, literature
- **Arts:** Color theory, composition, perspective, music theory
- **Health:** Nutrition, exercise, mental health, reproduction
- **Technology:** Binary, algorithms, programming basics, networks
- **Philosophy:** Logic, ethics, epistemology, metaphysics
- **Trades:** Carpentry, electrical, plumbing, HVAC basics

---

## HOW TO MAXIMIZE YOUR IMPACT (READ THIS)

### Rule 1: One Module at a Time

Don't try to build 5 modules. Build 1 perfectly, get it merged, then build the next.

**Why:** Validation is automatic. Merging is fast. Each module is useful immediately to learners.

### Rule 2: Steal Shamelessly from Existing Modules

Don't start from scratch. Read MOD-math-count-001.json or MOD-math-add-001.json.

Copy their structure. Adapt their language. Use their style guides for consistency.

**Why:** Consistency across 200 modules matters. Templates exist for this reason.

### Rule 3: Write for 8-Year-Olds and 80-Year-Olds

Every lesson should be clear to both. Avoid jargon. Use concrete examples.

If you can't explain it to an 8-year-old, you don't understand it yourself.

### Rule 4: Always Include Story Problems

Abstract procedures are forgettable. Stories stick.

Instead of: "Solve 3 × 4"
Write: "A pizza has 4 slices. You buy 3 pizzas. How many slices do you have?"

### Rule 5: Three Levels Always

Every worked example must have beginner, intermediate, and advanced versions.

- Beginner: Uses pictures or objects
- Intermediate: Uses symbols
- Advanced: Connects to next concept or solves a real problem

### Rule 6: Link to Prerequisites

Every module must list the modules learners should complete first.

**Why:** Learners can follow paths, not just random lessons.

### Rule 7: Cite Real Sources

Don't make up citations. Use:
- Textbooks (Van de Walle, NCTM, Singapore Math)
- Academic papers (accessible versions)
- Khan Academy, Wikipedia, reputable education sites
- Your own experience (if you're an expert)

### Rule 8: Test Your Examples

Run through every worked example yourself. Solve every exercise yourself.

Don't publish a module with examples you haven't verified.

---

## TOOLS AVAILABLE (USE THEM)

### Validation Tool
```bash
python3 tools/validate.py module data/modules/MOD-[name].json
```
Catches errors before submission.

### Module Template
```bash
cp tools/module-template.json data/modules/MOD-[name].json
```
Your starting point. Copy, don't rewrite.

### GitHub Actions CI/CD
When you push, GitHub automatically validates your module.

If validation fails, you see errors immediately.

If validation passes, PR is ready to merge.

### Archive of Existing Modules

Location: `data/modules/`

Read any completed module to understand the standard.

---

## TOKEN EFFICIENCY GUIDE (CRITICAL)

**This system is designed to cost 400K-1M tokens for 200 complete modules.**

**Here's how:**

1. **Infrastructure cost (one-time):** ~50K tokens
   - Schema design
   - Validation tool
   - Templates
   - Master instructions

2. **Content cost per module:** ~3-5K tokens
   - Introduction: 300 words (~500 tokens)
   - 2 core sections: 500 words (~800 tokens)
   - 3 worked examples: 500 words (~800 tokens)
   - 5 exercises: 300 words (~500 tokens)
   - Sources: minimal

3. **Total for 200 modules:** 50K + (200 × 4K) = ~850K tokens

**Compare to alternative (sequential building):**
- If one AI built all 200 sequentially, each module needs 5-10K tokens (includes reasoning, planning, revisions)
- 200 × 7.5K = 1.5M tokens wasted on reasoning + planning
- Plus: Serial execution takes months

**This system:** 100 AIs work in parallel, each spends 4K tokens on content only (no redundant planning).

**Your job:** Build great content, not redundant infrastructure.

---

## CHECKLIST BEFORE YOU START

- [ ] I have cloned the repository
- [ ] I have read START_HERE.md
- [ ] I have read MASTER_BUILD_INSTRUCTIONS.md
- [ ] I have read 2-3 existing complete modules (examples)
- [ ] I understand the 5-section template (intro, 2 sections, 3 examples, 5 exercises)
- [ ] I have chosen which module to build
- [ ] I understand the validation process
- [ ] I know how to commit and push to GitHub
- [ ] I will test my examples before submitting
- [ ] I understand this is for free, forever, for everyone

---

## YOUR MISSION (FINAL)

**This week:**
1. Pick 1 module from the TODO list
2. Fill it completely (1-2 hours)
3. Validate it
4. Submit a PR
5. Celebrate when it merges

**This month:**
- Help 4-5 other people start building modules
- Build 3-5 modules yourself
- Watch the TODO list shrink

**This year:**
- 100+ modules built by thousands of contributors
- Knowledge Commons becomes the default learning resource
- 8 billion people can access all human knowledge free, offline, forever

---

## QUICK REFERENCE: MODULE TEMPLATE STRUCTURE

Every module is JSON with this structure:

```json
{
  "id": "MOD-[subject]-[descriptor]-001",
  "title": "[Full Title]",
  "subtitle": "[Short explanation]",
  "grade_level": "[e.g., 3-4]",
  "prerequisites": ["MOD-...", "MOD-..."],
  "learning_objectives": [
    "Students will be able to...",
    "Students will understand that...",
    "Students will apply..."
  ],
  "introduction": {
    "content": "[100-200 words explaining why this matters]",
    "key_connections": ["Real-world example 1", "Real-world example 2"]
  },
  "core_sections": [
    {
      "title": "[Section 1 Title]",
      "content": "[200-300 word explanation]",
      "key_terms": ["term1", "term2", "term3"],
      "visual_explanation": "[Diagram description or ASCII art]"
    },
    {
      "title": "[Section 2 Title]",
      "content": "[200-300 word explanation]",
      "key_terms": ["term1", "term2"],
      "visual_explanation": "[Diagram description]"
    }
  ],
  "worked_examples": [
    {
      "level": "beginner",
      "title": "[Simple example]",
      "problem": "[Simple concrete problem]",
      "solution": "[Detailed step-by-step solution]",
      "explanation": "[Why this method works]"
    },
    {
      "level": "intermediate",
      "title": "[Medium example]",
      "problem": "[Problem using abstract notation]",
      "solution": "[Solution]",
      "explanation": "[Connection to concepts]"
    },
    {
      "level": "advanced",
      "title": "[Complex example]",
      "problem": "[Real-world or challenging problem]",
      "solution": "[Solution]",
      "explanation": "[Extension or connection to next topic]"
    }
  ],
  "exercises": [
    {
      "number": 1,
      "level": "guided",
      "problem": "[Simple problem with hints]",
      "hint": "[Step-by-step guidance]",
      "solution": "[Answer and explanation]"
    },
    ... (5 exercises total, mix of levels)
  ],
  "sources": [
    {
      "author": "Name",
      "year": 2024,
      "title": "Work Title",
      "publisher": "Publisher",
      "url": "https://...",
      "note": "Specific section or chapter"
    },
    ... (minimum 3)
  ]
}
```

**That's it. Copy this structure. Fill in your content. Submit.**

---

## GO BUILD IT

You have everything you need:

- ✓ Infrastructure that works
- ✓ Templates that scale
- ✓ Examples to copy from
- ✓ Validation that catches errors
- ✓ Curriculum mapped and ready
- ✓ Repository on GitHub
- ✓ 200 empty slots waiting for content
- ✓ 8 billion people waiting to learn

**Pick a module. Build it. Submit it. Repeat.**

This is how we save the world: one lesson at a time, built by thousands of minds, stored forever on GitHub, free forever.

**The work starts now.**

---

## FINAL WORDS FROM JONATHAN

> I don't have much time or money left. But I know everyone else deserves to be saved. This knowledge commons is infrastructure so that when my work runs out, the system keeps going. Other AIs, other humans, other minds—please take this seriously. Build one module. Get it merged. Then build another. We're all building the foundation for 8 billion people to learn together.

**That's the mission. Make it count.**

---

## CONTACT & COLLABORATION

- **Repository:** https://github.com/jonjonjon11/jonathan-creative-archive
- **Branch:** main
- **Questions:** Open an issue on GitHub
- **Want to help:** Fork, pick a module, build it, submit a PR
- **Want to coordinate:** Comment on README_PROGRESS.md or create a discussion

**Every contributor gets credit. Every module gets licensed CC BY 4.0. Every person who learns benefits forever.**

Let's build this together.
