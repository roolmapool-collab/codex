# Hermes Healthcheck Sync - 2026-05-25

## Context

Codex synchronized with `roolmapool-collab/codex` before continuing Hermes cleanup.

Important correction after sync:

- Named agents now run as separate Docker Compose containers.
- They should not be checked only from inside `hermes-agent-1`.
- Reference report already present in this repository: `reports/hermes-agents-online-2026-05-25.md`.

## Server Corrections Applied

Hermes memory healthcheck was reduced from:

```text
Critical=0 Warnings=12
```

to:

```text
Critical=0 Warnings=1
```

Actions:

- Added missing governance files for active mission `MISSION-PREMENOPAUSE-2026-05-22`:
  - `TASKS.md`
  - `DELIVERABLES.md`
  - `DECISIONS.md`
  - `RISKS.md`
  - `VALIDATIONS.md`
  - `EVENTS.jsonl`
- Refreshed agent `_current_state.md` files.
- Corrected agent state notes to reflect Compose container deployment:
  - `hermes-ariane`
  - `hermes-vulcain`
  - `hermes-argus`
  - `hermes-atlas`
- Updated Ariane validation note to state that current liveness must be checked via Docker Compose and agent-container logs.

## Verification

Docker Compose global state showed:

```text
hermes-agent-1   Up
hermes-ariane    Up
hermes-vulcain   Up
hermes-argus     Up
hermes-atlas     Up
hermes-dashboard Up
```

Latest healthcheck after corrections:

```text
Critical=0 Warnings=1
Decision=VALIDÉ AVEC RÉSERVES
```

Remaining warning:

- Secret scan: requires separate review and redaction/classification. Do not publish raw internal files before this is resolved.

## Git Safety

Do not push server workspace dumps to GitHub.

Only sanitized reports and runbooks should be committed.
