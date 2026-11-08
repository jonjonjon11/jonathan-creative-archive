# Contributing to this archive

The newly written archive is CC BY 4.0; the included Reality Atlas tool retains CC0. Check [rights and attribution](docs/rights-and-publication.md) before reusing or adding material. Propose focused corrections with a source ID and supporting evidence.

## Start with one observation

You can check or adapt an example without Git or JSON. The [learner quick start](docs/QUICKSTART.md) provides download steps, a short report, attribution guidance, and optional issue submission. One browser or device is enough for a partial observation; report untested parts explicitly. Posting to GitHub requires an account and connection, while keeping or sharing a permitted local copy does not require GitHub. Do not collect learner-identifying information.

An issue or adaptation is a proposal, not an approved correction. The repository-editing checks below apply when preparing files for integration; they are not prerequisites for asking a question or reporting an observation.

## Improve evidence before expanding claims

- Choose one concept or source ID.
- Explain whether you are recovering history, correcting a claim, proposing new work, or contributing an artifact.
- Preserve the distinction between the original person's idea and a later editor's addition.
- Give sources and state what you actually inspected or tested.
- State uncertainties and dissent fairly.
- Do not infer functionality from a name, branch, screenshot, or generated plan.

## Adding a concept

Include a stable ID, descriptive title, domain tags, concise summary, source IDs, artifact status, scientific standing, known limitations, safety/rights considerations, and a small next step. Use the vocabulary in [evidence and status](docs/evidence-and-status.md).

## Adding an artifact

Do not include private material or third-party assets merely because they occur in an existing repository. Confirm authorship, license, permissions, dependency rights, and absence of secrets. Keep runtime claims tied to an exact version and test record. Do not make claims about educational, medical, or safety efficacy without appropriate evidence.

## Respect people

Do not submit personal records, medical details, credentials, identifying information about minors, or private conversations. Community and training concepts should support informed participation, accessibility, and respectful differences among traditions and disciplines.

## Review

Run the structural validator and [Archive Steward](tools/archive-steward/README.md), then review the prose. When adding a recovered artifact, update `data/artifacts.json` with the exact rights scope and verification limits. Review all new and changed files before refreshing `data/checksums.json`; the read-only helper deliberately cannot bless a new baseline. Automated checks cannot establish truth, license compatibility, safety, or completeness. Corrections should preserve the source history of the claim rather than silently rewriting a proposal as an accomplished result.

## Add a learning module

Start with the [authoring guide](docs/knowledge-module-schema.md) and the [corrected worked-example specimen](docs/task-templates/new-example-template.md). The generic template is unreviewed scaffolding, not an accessible or complete lesson. Run `python3 tools/validate.py module data/modules.json data/modules/*.json` and `python3 -B -m unittest discover -s tools/tests -p 'test_*.py'`. These detect structural defects and selected regressions; they do not certify correctness or pedagogy. Include independent mathematical/source review and report which browser or learner checks were not performed.
