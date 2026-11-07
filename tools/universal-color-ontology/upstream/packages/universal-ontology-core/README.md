# Universal Ontology Core v1

Finite core seed registry plus procedural generators for infinite/large address spaces.

The locally generated v1 registry contains **593 explicit finite core nodes**, comprising:

- all 118 periodic elements
- 30 Standard Model particle/antiparticle/gauge/Higgs species-label entries
- 7 SI base dimensions and 7 SI base units
- 19 selected SI derived quantities and 19 corresponding units
- 52 geometry concepts
- 105 mathematics concepts/operations/relations/structures
- 71 music/acoustics/theory concepts
- 61 color/color-science concepts
- 38 universal visual channels
- 52 relation types
- 14 epistemic-status nodes

The registry intentionally does not claim to finitely enumerate all of mathematics, biology, history, medicine, species, continuous physical states, colors at arbitrary precision, or future discoveries. Those families are represented through stable generators or future authoritative import adapters.

## Open/large family generators

- `integerNode(n)`
- `rationalNode(p,q)`
- `complexNode(re,im)`
- `regularPolygonNode(n)`
- `srgba8Node(r,g,b,a)`
- `midiNoteNode(note,a4Hz)`
- `chordNode(notes,a4Hz)`
- `unorderedSelfInclusivePairs(items)`
- `orderedPairs(items)`

## Connectivity principle

Every registered/generated node is candidate-connectable to itself and every other node in the active working set. Candidate connectivity is not equivalent to asserting a factual relationship. Edges become asserted only through a definition, rule, validated model, evaluated data, evidence, or explicitly labeled semantic/pedagogical/artistic mapping.

The generated snapshot `UNIVERSAL_ONTOLOGY_CORE_v1.zip` is also preserved from the ChatGPT build session and contains the 593-node JSON snapshot and manifest used to verify these counts.
