# Idea Finder 0.1

Find a useful starting point in Jonathan's Creative Archive without manually searching several JSON files. This small offline helper returns matching concepts together with their next steps, source records, known limits and related included artifacts. It preserves the distinction between an idea, inspected source code and verified behavior.

It is a deterministic metadata search tool, not a language model, web search engine or autonomous agent. It requires Python 3.10 or later, no packages, account or credentials.

## Try it

From the repository root:

```sh
python3 tools/idea-finder/idea_finder.py . "rescue"
python3 tools/idea-finder/idea_finder.py . "music" --limit 3
python3 tools/idea-finder/idea_finder.py . --tag physics --status source_inspected
python3 tools/idea-finder/idea_finder.py . "CON-021" --format json
python3 tools/idea-finder/idea_finder.py . --tag education --tag browser
python3 -m unittest discover -s tools/idea-finder/tests -p 'test_*.py' -v
```

The root directory is always explicit. Omit the query to browse by stable concept ID. Use the exact tags shown at the end of the text report, including underscores in tags such as `martial_arts` or `health_education`. Repeated `--tag` filters require **all** selected tags. A status filter uses the archive's [evidence vocabulary](../../docs/evidence-and-status.md).

Default output is five results. `--limit` accepts 1 through 20. Total matches, returned results and omissions are always stated. If more than 20 records match, narrow your query or filters; there is no pagination in this version. Zero matches is a successful search, not an error.

For a reusable structured result, use `--format json`. If you save the output with shell redirection, keep it outside the archive and choose a new filename so the shell does not overwrite an existing report. The helper itself never saves or edits a file.

## What a result tells you

- The original concept ID, title, tags, summary, artifact status, scientific standing, next step and limitations.
- The fields that matched your terms. JSON also supplies the text-match score.
- Resolved source IDs with their evidence class, access declaration, recorded finding and source limitations. A private source remains described as private.
- Related included artifacts with shared source IDs, declared license and exact scope, local license/review paths, and the recorded verification limits.

Artifact relationships are inferred **only from shared source IDs**. A source may discuss several ideas. A related artifact is therefore a lead to inspect, not evidence that it implements that particular concept. If none is linked, that does not prove no implementation exists elsewhere. Licenses are copied declarations, not legal clearance.

For example, searching `rescue` in the current archive finds both the preserved cooperation mission kit's concept and the separate Sanctuary restoration idea. The output keeps their different implementation states visible rather than presenting both as playable games.

## Matching and ranking

All whitespace-separated query terms must occur as literal substrings in at least one indexed field. Terms may match different fields. Search is case-insensitive and applies Unicode NFKC normalization and whitespace normalization. It uses no regular expressions, phrase syntax, stemming, synonyms, embeddings or semantic inference. Shell quotation keeps a multiword query together; the words are still separate required terms.

Indexed fields: concept ID, title, tags, summary and next step. Source findings, limitations, entire documents and source code are **not** indexed. An unrecorded feature can exist without matching this search. Searching an exact concept ID is a convenient way to retrieve its complete local context.

Each distinct term contributes only its strongest field weight: ID/title 5, tags 4, summary 2, next step 1. Results sort by descending total, then stable ID. Duplicate terms do not increase the score. This is text relevance, not scientific confidence, usefulness, urgency or evidence strength. Empty-query browsing sorts by ID.

## Boundaries

The helper reads exactly these local inputs:

- `data/concepts.json`
- `sources/manifest.json`
- `data/artifacts.json`

It validates required record fields, IDs, source references, status/scientific-standing labels and schema versions. Each JSON input is limited to 4 MiB, queries to 500 characters and 16 distinct terms, and returned concept count to 20. Input-file and metadata-directory symlinks, nonregular files, duplicate JSON keys and malformed data are rejected. The explicitly selected root is resolved before reading it.

It does not open artifact paths, URLs or any path copied from metadata. It performs no network requests, credential lookup, source execution, filesystem edits, publication or scheduling. Tests create and clean up temporary synthetic fixtures. Output neutralizes terminal control characters; unexpected metadata fields are not exported.

It does not check file integrity, verify actual artifact presence, test apps, establish rights, evaluate science, retrieve private originals or certify safety, accessibility or educational efficacy. Run [Archive Steward](../archive-steward/README.md) and the relevant artifact tests separately. Selected metadata itself could contain private information if used on a private archive; review any output before sharing. This is intended for a trusted, stationary checkout, not as an operating-system sandbox for hostile or concurrently changing files.

Exit codes: **0** for a completed search, including no matches; **2** for invalid arguments or unreadable/invalid input. There is no automatic publication or action triggered by a match.

## Verification and license

The synthetic test suite covers matching, filters, ordering, omissions, source attribution, artifact relationship limits, malformed records, bounded inputs, symlinks, inert paths, controlled errors, output escaping and unchanged archive files. See [the archive validation record](../../docs/validation-report.md) for the current test count and real-archive checks.

This newly written helper and tests use the archive's existing [CC BY 4.0 license](../../LICENSE). They do not change the licenses or status of recovered artifacts.
