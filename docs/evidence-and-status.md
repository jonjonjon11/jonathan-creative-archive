# Evidence, status and scientific boundaries

## Artifact status vocabulary

Use the most specific supported label. The labels do not form a guarantee of quality or a universal maturity score.

- `idea`: a proposal or wish is recorded; no implementation evidence is required.
- `documented_design`: a substantial design or specification was recovered.
- `artifact_delivery_record`: a message records that a file was delivered; the file bytes may not have been inspected.
- `source_inspected`: relevant source text was inspected; no successful execution is implied.
- `historical_test_report`: an earlier source reports tests; this review did not rerun them.
- `runtime_verified`: a stated build and behavior were directly checked in a named environment, with date and evidence.
- `review_gap`: evidence is missing or insufficient to assign a more informative status.
- `editorial_proposal`: a new recommendation made while assembling this archive, not historical user work.

No complete source application in this compilation is newly assigned `runtime_verified` by the archive review. The included Reality Atlas HTML has 46 focused calculation-layer/syntax checks, documented separately; its fresh browser launch was blocked before loading. The cooperation/rescue authoring kit has 25 freshly rerun passing tests and a passing four-mission validator. That is scoped verification of offline authoring/reference logic, not a completed game or certified system. Lumen Commons passed 24 fresh Node tests and static build/source-parity checks; its fresh browser run was blocked before page load, so it is not newly browser-verified.

## Evidence classes

- `direct_user_request`: direct evidence of intent, not of feasibility or completion.
- `direct_source_document`: a recovered specification or document that was read.
- `repository_inspection`: source or metadata inspected at a particular reference.
- `historical_delivery_receipt`: a claim that an artifact was produced or sent.
- `secondary_summary`: an earlier synthesis; useful but weaker than the underlying source.
- `new_editorial_synthesis`: current organization or implementation suggestion.

Where a source itself reports a result, preserve that attribution. Do not silently convert “the status file reports tests passed” into “tests passed in this review.”

## Scientific standing

Use separate fields for scientific standing and implementation maturity. A correctly implemented simulation can model an unsupported theory; a scientifically conventional equation can be implemented incorrectly.

- `established_model_scoped`: conventional mathematics or science, limited by stated assumptions and still requiring citations for the actual lesson.
- `design_mapping`: an interpretive visualization, audio mapping, or interface choice.
- `speculative_unvalidated`: a hypothesis or framework without adequate validation in the reviewed evidence.
- `not_a_scientific_claim`: creative, organizational, or community design intent.
- `insufficient_evidence`: the review cannot classify the claim reliably.

## Required reporting practice

For every meaningful claim, record what is asserted, its source IDs, scope, known limits, and any next verification step. Record a test with the exact artifact, command or procedure, environment, result, and date. Record a failure accurately without guessing its cause.

Branch titles, repository descriptions, file existence, generated previews, and screenshots do not alone demonstrate functionality, safety, learning efficacy, or originality.
