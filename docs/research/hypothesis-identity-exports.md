# Hypothesis identity and complete exports

Review date: 2026-11-08 (UTC). Draft stacked on PR #8 at
`4b032958d88074af1f1cfd2e0d364a70f5819203`, not a merge into main.

## Reproduced failures

- Mechanistic IDs hashed only the gap description. Reusing a gap in a different
  pathway or with another proposed mechanism silently replaced the first record.
- Combination IDs concatenated intervention IDs without boundaries. For example,
  `["A", "BC"]` and `["AB", "C"]` shared an ID. The interaction description was
  ignored; distinct proposed interactions also overwrote each other.
- Combination generation silently omitted unknown IDs while retaining them in
  its reference list, and retained the caller's mutable list by reference.
- Research export ranked only 100 records before building `all_hypotheses`, but
  `hypothesis_count` still reported the full number. The standalone export's
  ranking list also silently stopped at 50. Research records after the 30-record
  top view lost predictions, evidence references, and other details.

## Correction and compatibility

Mechanistic identity now hashes structured pathway/gap/proposed-mechanism
context; combination identity hashes the ordered intervention list and proposed
interaction. Both use SHA-256-derived IDs with explicit field boundaries. The
three text-context fields are preserved in the records. Leading/trailing context
whitespace is trimmed; intervention IDs are exact, and their supplied order is
retained. Identical normalized questions update the same record. Mechanistic
confidence is updateable metadata, not a new question identity.

Unknown, duplicate, or insufficient combination members and blank descriptions
are rejected before storing a record. Input lists are copied. The interaction
description is preserved as an unvalidated proposal; the template asks whether
it occurs rather than asserting synergy, and uses `open_question` confidence.
Caller context is not source appraisal or evidence of an effect.

Both JSON export paths now contain all registered records and complete ranking
lists. Research `all_hypotheses` holds full records; `top_hypotheses` holds the
first 30 of those records, with count, limit and truncation metadata. The Markdown
report remains a 10-record preview, states how many of the total are shown, and
links to the complete JSON. Direct ranking calls still default to 20; `None`
means all, and invalid or negative limits are rejected.

Hypothesis export version is **1.2**. Mechanistic/combination IDs change, while
the 1.1 therapeutic IDs and all numeric scores remain unchanged. Regenerate and
review dependent references. Previously overwritten records cannot be recovered
from the old output alone; recover them from original inputs. Pathway exports
remain version 1.0. Output is still assembled in memory, not streamed.

## Verification

The 18 new synthetic regressions exposed the failures against the unchanged base,
then passed after the correction. They exercise context identity, delimiter
ambiguity, idempotence, confidence updates, malformed inputs, unknown references,
caller-list mutation, and both export paths at 0, 1, 10, 11, 30, 31, 50, 51, 100,
101 and 125 records. Complete exports retain prediction, mechanism, supporting
and contradicting references, and experimental-approach fields beyond previews.
Existing therapeutic and committed-output parity tests remain in the same suite.

All 182 local Python tests passed on Python 3.12.14: 41 hypothesis, 31
evidence-library, 14 sampled-switch, seven health-integration, 57 Archive Steward,
and 32 Idea Finder. Module/project/task and both evidence-pack validators,
structural/link checks, and diff whitespace checks passed. Comparing against the
pinned base confirmed all eight therapeutic records retain every existing field,
ID, and rank; all 16 numeric scores and ordering positions are unchanged.

Archive Steward still exits 1 with 43 findings: 41 inherited from the pinned
base plus the two new unlisted test/review files. No checksum entry was refreshed
to conceal a finding. These shared-baseline entries require explicit review and
reconciliation before merge. Python 3.10/3.11 and other operating systems were
not tested locally.

A clean staged-file export reproduced all 182 tests, the validators, and the
same 43 checksum findings. Independent AI review found no blocking defect,
reran the 41 hypothesis tests, verified therapeutic-ID compatibility across 12
additional contexts, and confirmed both exports retain 10,000 records in the
same ranking order, including ties. This is a bounded software check, not a
large-dataset performance guarantee or scientific review.

Run from the repository root:

```sh
python3 -m unittest discover -s tools/hypothesis-engine/tests -p 'test_*.py' -v
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
git diff --check
```

The existing workflow discovers all hypothesis tests. The full validator and
regression commands are listed in the [prior review record](hypothesis-outcome-safety.md).
Tests check program behavior, not scientific correctness, clinical efficacy or
safety. No registry coefficients, raw evidence inputs, enriched pathways,
workflow, or shared checksum baseline are changed in this correction.

## Remaining boundaries

Registry coefficients, literature counts, default timelines, heuristic rankings,
and mechanistic proposals still require source-level review. Stored evidence is
not yet connected to generated questions. Population labels are not validated
indications. Neither complete export nor unique contextual IDs makes a question
scientifically sound. The mutable in-memory dataclasses and registries are not an
immutable audit log, and concurrent modification is unsupported.
IDs retain 64 bits of SHA-256 without a collision-detection layer. Structured
context fixes the demonstrated collisions, but truncated hashes are not an
absolute mathematical uniqueness guarantee.

No source articles, third-party code, restricted data, or patient records were
added. Original contributions follow the archive's existing
[CC BY 4.0 license](../../LICENSE). This is a reviewable draft, not a deployment.
