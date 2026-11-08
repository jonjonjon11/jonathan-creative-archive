# Knowledge Module format 1.0: authoring guide

This is a structural record format, not a claim that every lesson is correct, complete, accessible or accepted by educators. Unknown fields are preserved; the checker covers only the rules below. This guide replaces an outdated copied motion lesson that could reintroduce incorrect examples and unsupported accessibility claims.

## Start with the actual teaching record

- [Canonical motion module](../data/modules.json): full structured lesson with corrected mathematics, examples, exercises, sources and limitations.
- [Paper-first motion lesson](lessons/motion-trace-shape.md): readable worked examples and coordinate tables.
- [Authoring template](../tools/module-template.json): a scaffold containing placeholders, **not a finished or verified lesson**.
- [Contribution workflow](collaboration-workflow.md): review and collaboration steps.

The guide deliberately links to the canonical lesson instead of maintaining another copy. Update the canonical teaching record and its numerical tests together when changing the mathematics. A change to prose can still be wrong even when JSON validation passes.

## Shape and required fields

The outer JSON object has `schema_version: "1.0"` and a `module` object.

The module requires non-empty text for `id`, `version`, `title` and `license`; a non-empty array of non-empty `learning_objectives`; an array of prerequisite objects (empty is permitted); and a `content` object.

The content contains:

- `worked_examples`: at least three objects, each with non-empty `id` or `title`.
- `exercises`: at least five objects, each with non-empty `prompt` or `problem_statement`, and non-empty `solution_guidance` or `solution`.

The two exercise conventions support the motion and arithmetic records already present. A final `answer` alone is not an explanation. Example and exercise IDs, when supplied, must be non-empty and unique **within their own list**. The same local ID may occur in another module or the other list. Module IDs must be unique across files supplied in one invocation.

For compatibility, examples and exercises may still reside directly under `module` when absent from `content`. New records should put them inside `content`. A malformed content field is rejected rather than silently replaced by a second copy at module level.

## What authors should include beyond the structural minimum

- Defined terms, prerequisites, objectives and learner level.
- Intuition followed by precise statements, assumptions, units and derivations.
- Worked examples with reasoning, counterexamples and common misconceptions.
- Exercises with solutions and checks for understanding.
- Source identifiers, inspected locations, dates, attribution and redistribution limits.
- Clear model-versus-reality distinctions, uncertainty and unresolved questions.
- A readable text-only path and specific accessibility evidence or gaps.
- Review status and bounded contribution opportunities.

These are editorial review requirements. The current checker does **not** verify their substance, source validity or completeness. It also does not enforce a full JSON Schema, semantic version syntax, all optional field types, prerequisite links, license validity, review-status truth, or the absence of every placeholder. Do not treat its output as publication approval.

## Run offline checks

From the repository root, using Python 3.11 or later and no additional packages:

```sh
python3 tools/validate.py module data/modules.json data/modules/*.json
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 -B -m unittest discover -s tools/tests -p 'test_*.py'
```

The command reports every supplied file and returns 1 if any file fails. Missing files, invalid UTF-8, malformed JSON, duplicate JSON keys and non-finite JSON constants are reported as failures rather than successful checks. It continues to later files after a failed file. Duplicate IDs are checked only within one invocation and record type, not across the entire repository automatically. An invocation without arguments or with `--help` prints usage and returns 0.

## Project and task checks

Projects require non-empty `project_id`, `version`, `title`, `purpose`, `status` and `license`. Supported statuses are `planning`, `in_progress`, `first_pathway_complete_validation_pending`, `complete`, `paused` and `archived`. Accepting the status string `complete` does not establish completion.

Tasks require non-empty `task_id`, `project_id`, `title`, `objective` and `status`; a non-empty array of scope strings; and a non-empty deliverables array. Deliverables may be non-empty text or objects with non-empty `name` and `format`. Task status must be `open`, `in_progress`, `pending_review`, `approved`, `blocked` or `cancelled`. Time estimates must be positive finite numbers (booleans are not numbers here), and difficulty must be `beginner`, `intermediate` or `advanced`.

## Review before integrating

1. Replace placeholders and state what is actually implemented.
2. Check mathematical or scientific claims independently; use numerical regression tests where appropriate.
3. Preserve source rights and avoid private records.
4. Run structural checks, relevant lesson/tool tests and archive integrity checks.
5. Describe actual accessibility, educator and learner review; do not infer them from a template.
6. Merge only under the repository's authorized review process, then verify main and CI.

New material in this guide and the validator follows the repository's CC BY 4.0 license. Citing a source does not relicense it.
