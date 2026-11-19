---
name: browser-testing
description: >-
  Browser-based E2E testing of the project's web apps using the Cursor IDE
  browser MCP. Use when the user asks to test a UI, verify a page after a
  deployment, log into an app, check console errors, collect network logs,
  take screenshots, or perform any browser-based verification.
---

# Browser-Based E2E Testing

## When to use

- logging into a deployed or local app
- verifying UI after a deployment
- checking the browser console for errors or warnings
- collecting network request logs
- testing a specific frontend feature
- taking screenshots for visual verification

## Target apps

Keep the list in `project.mdc` (Tech Stack). For each app: URL, auth type
(none, password, password + MFA, token link), and which test account to use.

## Credentials

- Test credentials live in the project's secret manager, never in code, skills,
  docs or chat messages.
- Fetch them into shell variables right before use; never print passwords.
- Document the secret IDs (not the values) in `docs/CONFIGURATION.md`.
- If MFA is required and no automated OTP source is documented, ask the user
  for the code instead of guessing or retrying.

## Login workflow

1. Fetch credentials from the secret manager into shell variables.
2. `browser_navigate` to the login page, then `browser_snapshot` to confirm the form.
3. `browser_fill` email/username and password, `browser_click` submit.
4. MFA: snapshot for the code field, fill the code, submit.
5. Snapshot again; confirm the URL left the login page. Report failure otherwise.

## Diagnostics

| Need | Tool |
| --- | --- |
| Page structure and refs | `browser_snapshot` |
| Visual check | `browser_take_screenshot` |
| Console errors | `browser_cdp` with `Runtime.evaluate` / `Log.enable` |
| Network requests | `browser_cdp` with `Network.enable` |
| Performance | `browser_cdp` `Profiler.start` -> reproduce -> `Profiler.stop` |

Look for: console errors and warnings, failed or slow requests, CORS errors,
unhandled promise rejections.

## Quick health check (no login)

1. `browser_navigate` to the URL
2. `browser_snapshot` and `browser_take_screenshot`
3. Check console and network for errors
4. Report findings

## Rules

- Lock the tab (`browser_lock`) for longer sequences, unlock when done.
- Take a fresh snapshot before acting when a ref is not found.
- Stop after repeated failures with no new evidence and report what blocked progress.
- Watch server logs while testing against a deployed environment.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Blank page after navigate | Wait briefly, snapshot again |
| Ref not found | Fresh snapshot for updated refs |
| Login fails | Re-fetch credentials from the secret manager |
| MFA form missing | Check whether MFA is enabled for the test user |
| CORS errors | Check the API's allowed origins config |
