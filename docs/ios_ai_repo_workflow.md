# iOS Workflow: Gemini + ChatGPT for This Repo

This workflow is reliable on iPhone and does not require direct write integration.

## 1) Put this folder on GitHub once

```bash
cd /root/peace_execution_kit
git init
git add .
git commit -m "Initialize peace execution kit"
gh repo create YOURNAME/peace-execution-kit --private --source=. --remote=origin --push
```

## 2) View from Gemini/ChatGPT iOS

- Share the repo URL in the app prompt.
- Ask for file-by-file analysis with explicit file paths.
- Prefer targeted prompts ("review these 3 files") over broad prompts.

## 3) Safest way to add changes from iOS AI apps

1. Ask for a **unified diff patch** only.
2. Apply patch in terminal:
   ```bash
   git apply changes.patch
   ```
   or paste changes manually.
3. Run checks/scripts.
4. Commit and push.

## 4) Prompt template (copy/paste)

```text
You are my repo copilot.
Repo: https://github.com/YOURNAME/peace-execution-kit
Modify only these files:
- [file path 1]
- [file path 2]

Output format:
1) 5-line plan
2) unified diff only
3) commit message

Constraints:
- do not create extra files
- do not modify unrelated files
```

## 5) Direct mobile editing options

- GitHub web editor in mobile browser
- Codespaces in browser
- GitHub mobile app for quick file edits

Patch-based workflow remains the most predictable way to keep scope controlled.

