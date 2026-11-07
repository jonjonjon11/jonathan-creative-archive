# Browser Test Report Template

Use this template to document your testing of Motion → Trace → Shape on different browsers.

## Test Information

**Tester Name:** (Your name or GitHub username)  
**Date Tested:** (YYYY-MM-DD)  
**Report Created:** (YYYY-MM-DD)

---

## Test Environment 1

### System Information
- **Browser:** (e.g., Chrome 130.0.6723)
- **Operating System:** (e.g., macOS 14.1, Windows 11, Ubuntu 24.04)
- **Device Type:** (Desktop, Laptop, Tablet, Mobile)
- **Screen Resolution:** (e.g., 1920x1080)

### What You Tested

For each control, note whether it worked, partially worked, or did not work.

| Control | Tested | Status | Notes |
|---------|--------|--------|-------|
| **Page loads** | ☐ | ✓/✗/⚠ | |
| **Layout and graphs render** | ☐ | ✓/✗/⚠ | |
| **Preset buttons (Line, Circle, Figure-Eight)** | ☐ | ✓/✗/⚠ | |
| **Play button** | ☐ | ✓/✗/⚠ | |
| **Pause button** | ☐ | ✓/✗/⚠ | |
| **Step button** | ☐ | ✓/✗/⚠ | |
| **Time slider** | ☐ | ✓/✗/⚠ | |
| **X-cycles selector** | ☐ | ✓/✗/⚠ | |
| **Y-cycles selector** | ☐ | ✓/✗/⚠ | |
| **Phase offset slider** | ☐ | ✓/✗/⚠ | |
| **Save JSON button** | ☐ | ✓/✗/⚠ | |
| **Keyboard navigation (Tab)** | ☐ | ✓/✗/⚠ | |
| **Reduced-motion preference** | ☐ | ✓/✗/⚠ | |

### Visual Issues

Describe any visual problems you noticed (rendering glitches, text cut off, colors not visible, etc.):

```
[Your observations here]
```

### Functional Issues

Describe any controls that did not work as expected:

```
[Your observations here]
```

### Overall Assessment

**Does this browser work?**
- [ ] ✓ **Works** — All features render and function correctly
- [ ] ⚠ **Partial** — Most features work; minor issues noted
- [ ] ✗ **Does not work** — Significant issues prevent use

---

## Test Environment 2

### System Information
- **Browser:** (e.g., Firefox 131.0)
- **Operating System:** (e.g., macOS 14.1, Windows 11, iOS 18)
- **Device Type:** (Desktop, Laptop, Tablet, Mobile)
- **Screen Resolution:** (e.g., 375x667)

### What You Tested

| Control | Tested | Status | Notes |
|---------|--------|--------|-------|
| **Page loads** | ☐ | ✓/✗/⚠ | |
| **Layout and graphs render** | ☐ | ✓/✗/⚠ | |
| **Play/Pause** | ☐ | ✓/✗/⚠ | |
| **Time slider** | ☐ | ✓/✗/⚠ | |
| **Parameter selectors** | ☐ | ✓/✗/⚠ | |

### Visual Issues

```
[Your observations here]
```

### Functional Issues

```
[Your observations here]
```

### Overall Assessment

**Does this browser work?**
- [ ] ✓ **Works**
- [ ] ⚠ **Partial**
- [ ] ✗ **Does not work**

---

## Summary

### Browsers Tested
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Other: ________

### Overall Compatibility
**Summary sentence:** "Motion → Trace → Shape works [well/partially/not well] on [tested browsers]. [Main issue, if any]."

### Recommendations

What should be fixed or improved?

```
1. [Issue and suggestion]
2. [Issue and suggestion]
```

---

## Screenshots (Optional)

If possible, attach screenshots showing:
- The app in each tested browser (normal view)
- Any areas with rendering issues (close-ups)
- Mobile view (if tested)

**How to add screenshots:**
1. Take a screenshot (print screen or browser dev tools)
2. Save as PNG or JPEG
3. Upload to the pull request or issue when you submit this report

---

## Submission

When you're done:

1. Save this file as `browser-test-[your-name]-[YYYY-MM-DD].md`
2. Place it in the `docs/test-reports/` directory
3. Open a pull request with this file
4. In the PR description, reference the task: "Closes TASK-motion-browser-test" (optional)

Thank you for helping validate Motion → Trace → Shape!
