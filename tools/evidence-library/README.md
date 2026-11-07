# Evidence Library 0.1

A small offline Python tool for inspecting a bounded, versioned evidence pack. It validates record consistency, searches original summaries, and prints claims together with population limits and source references. It does not discover cures, rank treatments, recommend care, or turn a cited statement into a verified scientific result.

The initial [ALS pack](../../data/health/als-evidence.json) embeds factual summaries and scoped numerical findings rather than requiring a live API to read the evidence notes. The pack is a selected research and learning snapshot, not a full literature database or patient record. Its scope, inspection dates, rights notes, and limitations travel with the data.

## Run offline

Requires Python 3.10 or later and no third-party packages. From the repository root:

```sh
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json validate
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json report
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json report --topic tofersen
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json search "endpoint biomarker"
python3 tools/evidence-library/evidence_library.py data/health/als-evidence.json search "SOD1" --json
python3 -m unittest discover -s tools/evidence-library/tests -p 'test_*.py' -v
```

Use `--json` after the command for machine-readable output. The path is explicit; the program does not scan directories for medical files. It reads only that local pack and writes results to the terminal. To save a report, use ordinary shell redirection to a destination outside the archive. Redirection can overwrite a file, so choose the destination deliberately.

Search splits the query on whitespace and returns a claim when **any** term is a case-insensitive substring of its topic, statement, population, or limitations. `--topic` adds a topic substring filter. Source order is preserved; there is no relevance score or treatment ranking. Search output includes pack limits and claim limitations. A full report also includes any quantitative fields and the referenced source records. Queries and topics consisting only of whitespace are rejected.

Exit codes: **0** means the requested inspection succeeded, **1** means a pack could not be read or failed structural checks, and **2** means command syntax was invalid. Empty search results are valid and exit 0. A zero result does not establish scientific correctness, safety, licensing clearance, or review approval.

## Supported record format

The top-level object contains `schema_version: "1.0"`, one `pack` object, a nonempty `sources` list, and a nonempty `claims` list. See the included ALS pack and the entirely synthetic fixtures in [the tests](tests/test_evidence_library.py).

A pack carries:

- `id`, `title`, `version`, `scope`, and `license` as nonempty strings.
- `review_status: "draft_pending_qualified_review"`. This initial format only supports drafts; passing validation cannot grant qualified review.
- `as_of`, an ISO `YYYY-MM-DD` snapshot boundary.
- A nonempty `limits` list of nonempty strings.

Each source carries:

- Unique `id`, `title`, and an absolute `url` using HTTPS, without credentials or whitespace. URLs are displayed and never opened by the tool.
- `source_type`: `primary_trial`, `regulatory`, `government_education`, `registry`, `methods`, or `sponsor_report`.
- `published`: an ISO date, a four-digit year string, an integer year, or `null` when unknown.
- `checked`: an ISO date no later than `pack.as_of`.
- `rights_note` and `inspection`, describing the source's rights boundary and what was actually inspected.

Each claim carries:

- Unique `id`, `topic`, `statement`, and `population` strings.
- `evidence_type`: `randomized_trial`, `regulatory_decision`, `established_background`, `methodological`, `open_question`, `open_label_followup`, `trial_design`, `study_safety`, or `sponsor_report`.
- A nonempty `source_ids` list resolving to included source records; repeated references are rejected.
- A nonempty `limitations` list.
- Optional `quantitative`: an object containing `outcome`, `unit`, `timepoint`, `interpretation`, and finite numerical `estimate`, `ci95_low`, and `ci95_high` fields. The interval must contain the estimate, including its endpoints. Boolean values are not numbers for this format.

All pack, source, and claim IDs must be distinct. A `randomized_trial`, `open_label_followup`, `trial_design`, or `study_safety` claim must cite at least one `primary_trial` source; a `regulatory_decision` claim must cite at least one `regulatory` source. A `sponsor_report` claim must cite at least one source explicitly classified as `sponsor_report`.

Keep these distinctions visible. A sponsor's press release is not an independently peer-reviewed trial report. An open-label extension or delayed-start follow-up is not equivalent to a continuing randomized placebo comparison. A trial-design paper describes intended methods, not a demonstrated treatment effect. `primary_trial` identifies an original trial-related publication, including its design and follow-up papers; the claim's evidence type distinguishes their roles. These labels remain authored declarations, not independent assessments of study design or regulatory status. Numerical interval checks do not recalculate a trial analysis, establish its assumptions, or validate an endpoint.

The loader rejects malformed UTF-8 JSON, duplicate JSON keys, non-finite or overflowing JSON numbers, unsupported schema versions, malformed record shapes, and dangling source IDs. It accepts files up to 2 MiB and rejects symlink inputs and nonregular files. Publication dates and years are checked against the pack snapshot date. The tool uses no system clock to certify currentness; a plausible date can still be false or stale.

Unknown extra fields are allowed for editorial context and treated as data. They cannot authorize actions or cause imports, file reads, commands, URL requests, or tool execution. Plain-text reports escape terminal control characters. JSON output uses JSON string escaping and retains declared data.

## Review and extension

To add another topic, copy the record structure into a new local pack and write original summaries of inspected sources. Include the actual population, outcome, timepoint, uncertainty, and limitations rather than describing every result as a cure. A primary endpoint that did not meet its prespecified threshold must remain visible even when other endpoints or biomarkers look promising. Distinguish an historical regulatory decision from a current prescribing determination.

Keep source licenses separate from the license on original pack summaries. A URL, abstract record, or government database listing does not establish permission to copy journal text, trial narratives, illustrations, or datasets. Do not add identifiable patient information to a public pack. This tool has no patient-data de-identification or comprehensive secret detection.

A qualified reviewer should examine source-to-claim support, study design, numerical transcription, endpoint meaning, harms, population scope, and omitted evidence. Code tests cannot supply that review. Fresh source inspections require a new pack revision and honest dates; the program has no updater or scheduled background process.

The implementation is read-only and dependency-free. Its limits include trusting a stationary local file, declared metadata, and the accuracy of authored summaries. The file checks are not an operating-system security boundary. The program does not assess risk of bias, do a systematic review or meta-analysis, check for retractions, authenticate sources, evaluate clinical appropriateness, or connect to clinical systems. Qualified care decisions remain outside its role.

## License

This original helper, documentation, and synthetic tests use the archive's existing [CC BY 4.0 license](../../LICENSE). The helper does not change the rights of sources described in evidence packs or of separately licensed repository artifacts.
