# Learn, check, change and share

Start with a lesson below. You do not need Git, programming experience, an account or a subscription to read these public lessons. After downloading them, you can learn and work on your own copies offline. Opening external references or sending feedback online needs a connection.

These are AI-assisted learning drafts. Mathematical and software checks have been performed for specific examples and tools; human learner, educator and accessibility acceptance remain pending. The archive is a growing collection, not a complete curriculum.

## 1. Choose something to learn

- [Introduction to division](lessons/introduction-to-division.md): share objects, make equal groups and check leftovers. Read the three examples, then try the five exercises before their hints and solutions. Paper or imagined objects are enough.
- [Motion, traces and shape](lessons/motion-trace-shape.md): predict lines, circles and figure-eights from two repeating motions. Coordinate tables and written explanations work without animation. The optional browser lab is described below.
- [One press, one star](lessons/one-press-one-star.md): follow an invented input trace and predict a small game's score. Read it on paper, or run and change the finished Python example if you already have Python. Its lesson explains that extra setup; it is not a live game or assistive device.

Choose your own pace. Read one example, explain it in your own words, try a question, then compare your reasoning with the solution. You do not need to read a schema or edit JSON to begin.

## 2. Keep a copy without Git

**For the whole archive:** open the [repository home](https://github.com/jonjonjon11/jonathan-creative-archive), select **Code**, then **Download ZIP**. Extract the ZIP before opening files. Keep its folders together so relative file locations remain valid. Downloading needs a connection; the included lesson text and standalone labs do not need one afterward.

The readable lessons are in `docs/lessons/`. Files ending in `.md` are plain text: open them in a text editor you already have. Markdown punctuation will be visible in a plain-text editor, but the explanations and solutions are included. A Markdown viewer may make them easier to read; none is required. The optional reference websites are not included in the download.

**For one file:** on its GitHub file page, use **Download raw file** if available, or open **Raw** and save that file. Save the actual file rather than GitHub's surrounding preview page. Keep the applicable license and attribution when copying or sharing; the whole ZIP already contains the license files. A single lesson can be read alone, but its local links need the other files.

The GitHub download interface can differ by device. If downloading or opening HTML is not supported by your device's file viewer, use the readable lesson on GitHub or its plain-text copy instead. Actual phone, touch and assistive-technology behavior remains unverified.

### Optional motion lab

1. Download [Motion-Trace-Shape.html](../tools/motion-trace-shape/Motion-Trace-Shape.html), or find it in `tools/motion-trace-shape/` in the extracted ZIP.
2. Open that file in a full browser. GitHub's source preview does not run it. No server or package installation is needed.
3. Start with **Line**. The lab starts paused. Use the time slider or **Step +⅛ s**, or choose **Play one cycle** if animation is comfortable.
4. Predict what will change before choosing **Circle** or **Figure-eight**. Compare the positions with the [paper-first lesson](lessons/motion-trace-shape.md).
5. **Save experiment JSON** requests a local download of the settings and samples. Check your downloads to see whether it saved. The current lab cannot import that JSON or remember your settings after closing; it is an inspectable record, not a restore file.

The [lab guide](../tools/motion-trace-shape/README.md) explains controls, offline use, reuse and scoped Chromium/Firefox checks. A narrow browser window test is not a physical-phone test.

## 3. Check one example and change one thing

Here is an author-written example of a small contribution, not a report from a real learner:

- **Source:** [Introduction to division](lessons/introduction-to-division.md), module `MOD-math-div-intro-001`, version 1.0.0, worked example 1, “Sharing Twelve Pencils.”
- **Check the original:** twelve pencils shared equally among three tables gives four pencils per table. The check is 3 × 4 = 12.
- **Change:** use fifteen pencils, keeping three tables.
- **Prediction:** five pencils per table, with none left over.
- **Check the changed example:** 3 × 5 = 15. Five rounds of giving one pencil to each of three tables uses all fifteen.
- **What stays the same:** the answer counts pencils per table. It does not count the number of tables.
- **Review limits:** this arithmetic check does not show that the explanation teaches effectively. No learner observation, browser test or educator approval is claimed.

Now choose an example you understand. Change one value or explain one confusing step, keep the original for comparison, and write down your prediction before checking. If you cannot resolve a difference, record it as a question rather than marking your version correct. Do not replace the published lesson or turn a mathematical model into a claim about a real device or person.

Copy the [short verification and adaptation report](task-templates/verification-report-template.md) into your own notes. It records the source/version, change, reasoning, result, uncertainties and attribution. You can fill it in on paper or in plain text. Keep personal practice files outside the downloaded archive if you later run its integrity checks: those checks deliberately report unregistered files.

## 4. Share only if you want to

You can keep your work private, show someone your copy, or share a permitted adaptation by a method you choose. No contribution or account is required to learn here.

New archive lessons and these guides use [CC BY 4.0](../LICENSE). When sharing an adaptation, credit the original, provide the source and license links, say what you changed, and retain supplied attribution and notices. Do not imply endorsement. Separately licensed recovered tools keep their own licenses, and linked external articles are not automatically covered. See [rights and attribution](rights-and-publication.md).

For the changed division example above, a starting attribution is: “Adapted from Introduction to Division, Jonathan's Creative Archive Contributors, 2026, version 1.0.0, https://github.com/jonjonjon11/jonathan-creative-archive/blob/main/docs/lessons/introduction-to-division.md. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Changed twelve pencils to fifteen and added the multiplication check. No endorsement implied.” Preserve any other supplied notices with the copy.

### Optional feedback to this repository

- **Without Git:** use the [repository's Issues page](https://github.com/jonjonjon11/jonathan-creative-archive/issues), check for a matching report, then choose **New issue** or add relevant findings to an existing one. Posting requires a GitHub account and a connection. Paste the short report as text; an issue is a proposal, not an accepted correction. GitHub Discussions are not enabled as checked on 2026-11-08.
- **Without a GitHub account:** keep the report locally or share it with a person you choose. This archive has no anonymous submission service; nothing is sent automatically, and no one is obliged to submit on your behalf.
- **With Git experience:** fork the repository, create a branch in your fork, make a focused change and open a pull request back to this repository. Do not assume you can push to the original repository. Follow [CONTRIBUTING.md](../CONTRIBUTING.md) and the [contributor brief](../MASTER_PROMPT_FOR_CODEX.md) for tests and review. A fork or pull request also needs a GitHub account and connection.

Do not include learner names, ages, school details, patient information, private messages or account data. A contributor name is optional; never put someone else's personal information in a report. Screenshots are optional and should show only the relevant tool, with private information removed. Do not upload the archive or reports to unrelated services just to test them.

### Have only one browser or device?

One specific observation is useful. Use the [browser report](task-templates/browser-test-template.md), note the browser/version and device type if known, and mark anything you did not try as **not tested**. A second browser is optional for a contribution. Stop if a test requires payment, new accounts, unfamiliar permissions or anything you are not comfortable doing.

The [cross-browser task](../data/tasks/task-motion-browser-test.json) remains open until its remaining coverage and review needs are addressed. A report from one setup does not establish cross-browser compatibility, accessibility or learning effectiveness, and should not close that task by itself.

## For lesson authors and maintainers

Use the existing [authoring guide](knowledge-module-schema.md), [worked motion example](task-templates/new-example-template.md), [collaboration workflow](collaboration-workflow.md) and [contributor brief](../MASTER_PROMPT_FOR_CODEX.md). These are optional next steps for people changing repository content, not prerequisites for reading lessons. Check current files and open work before starting; earlier status documents may be historical.

From the repository root, with Python 3.10 or newer installed for the archive tools, the existing checks include:

```sh
python3 tools/validate.py module data/modules.json data/modules/*.json
python3 tools/validate.py project data/projects/*.json
python3 tools/validate.py task data/tasks/*.json
python3 -B -m unittest discover -s tools/tests -p 'test_*.py'
python3 scripts/validate_archive.py
python3 tools/archive-steward/archive_steward.py .
```

These examples use a Unix-like shell; the contributor brief covers relevant tool requirements. They are not needed for the paper-first path. Run the additional relevant checks listed in [.github/workflows/knowledge-commons-status.yml](../.github/workflows/knowledge-commons-status.yml) before proposing a repository change. Passing checks does not replace mathematical, educator, learner or accessibility review.
