"use strict";
// Test-only HTML-like content. Correct CSV quoting is essential: the DOM test
// must reach mapping/rendering rather than stop at malformed CSV syntax.
const escapeCell = value => /[",\r\n]/.test(value) ? '"' + value.replaceAll('"', '""') + '"' : value;
function makeInjectionFixture(clean) {
  return clean.replace("#lat_deg", escapeCell('<img src=x onerror="window.pwned=1">'))
    .replace("2024-02-29", escapeCell('<script>window.pwned=1</script>'));
}
module.exports = { escapeCell, makeInjectionFixture };
