# Machine-readable concept records

`concepts.json` is UTF-8 JSON. Each concept has a stable ID, title, tags, concise summary, source IDs, artifact status, scientific standing, limitations, and a concrete next step. `sources/manifest.json` resolves those source IDs.

Stable IDs identify editorial records, not a universal ontology. Do not interpret a source count or an artifact status as a scientific confidence score. See `docs/evidence-and-status.md` for the vocabulary.

The edition is a documentation dataset, not a model benchmark or an exhaustive account export. Newly written records are covered by the compilation’s CC BY 4.0 license; referenced upstream material retains its own rights. No inclusion in AI training or search indexes is promised.

## Included-artifact registry

`artifacts.json` records four recovered artifact families and four newly built tool families included in the archive. It adds stable artifact IDs, local paths, source IDs, declared license scope, license/review file locations, verification status/limits, and preserved manifest or pinned-file references. It does not certify rights, change any license, enumerate every support script, or upgrade a historical test claim.

[Archive Steward](../tools/archive-steward/README.md) reads this registry together with concepts, sources and checksums to produce an offline review report. The registry and checker are new editorial tools, not newly recovered historical sources. New implementations are identified explicitly rather than presented as historical recoveries. Keep checksum updates separate from the read-only check so changed files require deliberate review.

## Embedded health evidence

The `health/` directory contains original ALS and cancer evidence packs and selected published ALS trial facts, including measurements, populations, source links, field provenance, and source-response hashes. The [research entry point](../docs/research/README.md) connects the data to complete lessons and executable offline code. Pack validation checks record consistency; source and qualified scientific reviews remain distinct. These datasets contain no participant-level records or copied full articles.
