---
name: review-checklist
description: Review a branch or PR in the team order (correctness, tests, readability, security, scope). Use before approving or merging any PR, or when asked to review a diff.
---

Review the diff against its ticket (KAN-N in the branch, commits or PR description).
If no ticket is given, ask for it before reviewing scope.

Get the diff with `git diff main...HEAD` (or the PR diff), then report findings under
each heading, in this order:

1. **Correctness**: does it do what the ticket asks? Check edge cases: empty input,
   week boundaries (Monday to Sunday), zero and negative numbers.
2. **Tests**: is there a test that failed before the fix and passes now? Run
   `python -m pytest -q` and paste the result line.
3. **Readability**: names, function size, dead code, comments that explain why.
4. **Basic security**: input validation, secrets, injection, unsafe defaults.
5. **Scope**: anything changed that the ticket did not ask for?

Rules for findings:

- Each finding names the file and line and says exactly what to change. No vague comments.
- Mark each one `must fix`, `should fix` or `nit`.
- If a section has nothing, write "No findings".
- Before reporting a finding as a bug, check it (read the code or run it). Note any
  false positive in `docs/review-false-positives.md` so the next review can skip it.

End with a one-line verdict: approve, approve with nits, or request changes.
