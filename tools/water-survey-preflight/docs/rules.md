# Rule decisions and reconciliation

Ruleset **0.1.0**, reviewed **2026-11-07**. This is a local review profile, not the WPdx ingestion engine. Sources and verified URLs are in [sources.md](sources.md).

## Reconciling the two publications

The currently linked January 2021 standard and December 2023 MEAL annex agree on `lat_deg`, `lon_deg`, `report_date`, `status_id`, and `source`, plus at least one of `water_source` or `water_tech`. This implementation requires mappings for those parameters, not seven nonempty fields. Either type description suffices.

MEAL offers preferred responses to reduce misinterpretation, but source/technology descriptions are open text. This prototype does not enforce its suggestions as a closed vocabulary. Likewise, the standard permits binary equivalents and describes unknown/blank presence values as empty. Accordingly, absent `status_id` mapping is an error; a mapped blank, unknown, or unfamiliar response is a **warning requiring interpretation**, not automatic rejection or a silently inferred Yes/No.

The coordinate guidance recommends four or more decimals. Lower displayed precision is a warning; padding zeros cannot improve a measurement. Water presence describes the visit, not potability, service reliability, or current conditions. The app makes no inference from presence to those outcomes.

## Severity and rule basis

Each finding includes a machine-readable code and basis. “Error” is this tool's inability to proceed reliably or missing minimum information, not a promise that WPdx will reject it. “Warning” is a review question and may be legitimate.

| Basis | Implemented decision |
| --- | --- |
| `parser-profile` | Broken quoting, empty/duplicate headers, inconsistent widths, limits, ambiguous mappings, unsupported decimal or date syntax are errors. |
| `wpdx-required` | Missing required mappings/values are errors, with the presence-value exception above. Both type descriptions blank is an error. |
| `coordinate-bounds` | Latitude outside ±90 or longitude outside ±180 is an error. Boundary values are accepted. |
| `wpdx-guidance` | Low precision, unmapped presence responses, or malformed optional years are warnings. |
| `local-review` | Future dates/years, suspicious placeholders, year order, `(0,0)`, exact duplicate rows, and repeated visit IDs are warnings. These heuristics are not official WPdx rejection rules. |

An optional single `#` header prefix, case, and surrounding whitespace are ignored for matching. No geographic meaning is guessed from custom names. Mapped values are trimmed for checks, but never rewritten. Required presence of a header does not establish that its meaning is correct.

## CSV profile

UTF-8 input. Commas separate fields; CRLF, LF, and CR separate physical lines. Double-quoted fields may contain commas, newlines, and escaped doubled quotes. Quotes in unquoted fields and extra characters, including spaces, after closing quotes are errors. A UTF-8 BOM is accepted; NULs are rejected. Only truly empty physical records are skipped, not comma-filled rows or quoted empty values.

Logical CSV record numbers count the header and empty records; physical line numbers identify the start of the record. A multiline field therefore can make these differ. The first nonblank record is the header. There is no separate HXL hashtag-row support; place recognized names in the header or map actual columns manually.

## Date and number profile

Supported dates are valid Gregorian calendar dates `YYYY-MM-DD` in years 0001–9999. Optional time uses `T` followed by `HH:mm`, optional `:ss` and fractional seconds with dot or comma, and optional `Z` or signed `HH`, `HHmm`, or `HH:mm` offset. Hours are 00–23; minutes/seconds 00–59. Offset hours/minutes are syntax-checked, not verified against a real timezone. ISO week/ordinal dates, reduced dates, expanded years, `24:00`, and leap seconds are outside this checker’s profile. An error says the checker cannot assess them, not that every such representation violates ISO 8601 or WPdx requirements.

Calendar validity is checked directly, including the 100/400-year leap-year rule, without browser-dependent `Date.parse`. The future-date warning compares the date written in the field to the UTC review date. It does not shift the date by the timestamp offset. Near-midnight timezones and a wrong device clock therefore require human review.

Coordinates use plain decimal strings with a dot and optional sign. Bounds and zero checks compare the supplied decimal strings exactly, without floating-point rounding or underflow. DMS, comma decimals, scientific notation, hex, NaN, and infinity are outside the profile. `(0,0)` and decimal precision are warnings, not location verification. The code cannot establish WGS 84 or whether columns were switched when both numbers are within bounds.

## Duplicates and optional fields

Exact duplicates compare every raw cell, including unmapped columns. A second rule compares trimmed organization, trimmed ID, and calendar visit date; it skips an already exact-duplicate row. Both are warnings. A point may legitimately be visited more than once, and matching IDs across organizations may identify different points. No rows are merged, removed, geospatially clustered, or compared against remote records.

Only installation and rehabilitation years receive optional value checks. IDs are used only in the duplicate heuristic. Other optional parameters are not validated. Reports contain bounded excerpts of findings only when the user explicitly selects that option; aggregate counts include findings omitted by the output cap.
