---
name: design-local-review
description: >-
  Enforces local-first design review for any UI or visual change in any
  frontend app of the project. Use when the task involves new components,
  redesigns, color schemes, layouts, animations, copy with visual emphasis,
  hero sections, buttons, cards, modals, drawers, sheets, theme changes, or
  anything else that has a visible representation in the browser. Never push
  UI changes straight to production. Build variants locally, let the user
  pick, then ship.
---

# Local-First Design Review Workflow

## Hard rule

No UI/design change goes to production until the user has reviewed it locally
in a browser and explicitly approved the final look.

Applies to: new or redesigned components, color, spacing, typography,
animations, copy with visual weight (hero text, status badges, error states),
icons, drawers/sheets, modals, floating widgets, theme switching.

Does NOT apply to: typo-only copy fixes, dependency bumps, backend-only work,
unit-test-only changes.

## Workflow

### Step 1: Identify variants worth building

For each visual decision, draft 2-5 distinct variants. Variants must be:

- visually different enough that a side-by-side comparison is meaningful
- equally functional (same props, same i18n keys, same a11y contract)
- realistic, with mock data matching the production payload shape

Do not build "draft + polished" pairs. All variants are production quality.

### Step 2: Build a dev-only preview surface

Each frontend app gets a dev-only preview route, e.g. `/preview/<component>`.
Its location follows the app's router convention (document it in `project.mdc`).

The preview surface MUST:

- refuse to render in production builds (environment check returning 404)
- never be linked from any user-facing navigation
- be blocked at the CDN/hosting layer for production (rewrite to 404)
- render all variants on one page, labelled (Variant A, Variant B, ...)
- cover with mock data: short text, long text, missing optional fields, RTL
  locale if supported, dark mode if supported, terminal/edge states
- show a viewport hint at the top (test at 375px / 768px / 1280px)

### Step 3: Run locally

Start the dev server yourself so the user gets a working URL immediately.
Prefer mock data over live API calls so the preview works without auth or VPN.
If a backend is required, start it locally or port-forward it.

### Step 4: Hand off to the user

Tell the user:

1. The exact local URL
2. The variants on the page and how they differ
3. Which viewport widths to check (at least 375px and 1024px)
4. Known caveats (e.g. a variant needs an env var)

Then STOP. Do not push, build for production, or refactor further until the
user picks a variant.

### Step 5: Apply the choice and clean up

1. Move the chosen variant into the production component path.
2. Delete the other variants and preview-only mock data.
3. Keep the preview route only if other variants for that family are pending.
4. Run typecheck and lint for the affected app.
5. Run visual regression / unit tests if they exist.

### Step 6: Re-verify before push

1. Confirm the preview route returns 404 in a production build run locally.
2. Re-check the chosen variant on the real page where it will appear.
3. Confirm with the user: "Pushing variant <X> to prod, OK?"

Only after explicit confirmation, proceed with the normal deployment flow.

## Mock data conventions

Mock data lives next to the app in a `preview-mocks/<component>` module that
exports named scenarios (fresh, cancelled, long name, RTL, ...). Preview pages
iterate scenarios per variant so every variant is tested against every input.

## Anti-patterns

- Pushing to prod and "iterating in production" while the user watches the live site.
- Screenshots only, asking the user to imagine interaction (hover, focus, scroll, animation).
- One variant and "looks good?" when the user asked for variants.
- Deleting variants before the user has picked.
- Variants behind a query param on the real page (pollutes the prod bundle).

## Coordination with browser-testing

For verifying the deployed result, use `.cursor/skills/browser-testing/SKILL.md`.
This skill covers only the local pre-prod review loop.
